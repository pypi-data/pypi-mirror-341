"""
CVQP: A solver for Conditional Value-at-Risk (CVaR) constrained quadratic programs.
"""

import logging
import time
import numpy as np
import scipy as sp

from .types import CVQPParams, CVQPConfig, CVQPResults
from .projection import proj_sum_largest

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(message)s", datefmt="%b %d %H:%M:%S"
)


class CVQP:
    """
    CVQP solver.
    """

    def __init__(self, params: CVQPParams, options: CVQPConfig = CVQPConfig()):
        self.params = params
        self.options = options
        self.initialize_problem()

    def initialize_problem(self):
        """
        Initialize problem by scaling data and precomputing frequently used matrices.
        """
        self.scale_problem()
        self.setup_cvar_params()
        self.precompute_matrices()

    def scale_problem(self):
        """Scale problem data to improve numerical conditioning."""
        self.scale = max(-self.params.A.min(), self.params.A.max())
        self.params.A /= self.scale
        self.params.q /= self.scale
        if self.params.P is not None:
            if sp.sparse.issparse(self.params.P):
                self.params.P = self.params.P / self.scale
            else:
                self.params.P /= self.scale

    def setup_cvar_params(self):
        """Initialize CVaR-specific parameters based on problem dimensions."""
        self.m = self.params.A.shape[0]
        self.k = int((1 - self.params.beta) * self.m)
        self.alpha = self.params.kappa * self.k / self.scale

    def precompute_matrices(self):
        """Precompute and cache frequently used matrix products."""
        self.AtA = self.params.A.T @ self.params.A
        self.BtB = self.params.B.T @ self.params.B
        self.update_M_factor(self.options.rho)

    def update_M_factor(self, rho: float):
        """
        Update and factorize the matrix M used in the linear system solve.

        Args:
            rho: Current penalty parameter value
        """
        if self.params.P is None:
            BtB_dense = self.BtB.toarray() if sp.sparse.issparse(self.BtB) else self.BtB
            self.M = rho * (self.AtA + BtB_dense)
        else:
            P_dense = (
                self.params.P.toarray()
                if sp.sparse.issparse(self.params.P)
                else self.params.P
            )
            BtB_dense = self.BtB.toarray() if sp.sparse.issparse(self.BtB) else self.BtB
            self.M = P_dense + rho * (self.AtA + BtB_dense)

        self.factor = sp.linalg.lu_factor(self.M)

    def initialize_variables(self, warm_start: np.ndarray | None) -> tuple:
        """
        Initialize optimization variables and results structure.

        Args:
            warm_start: Initial guess for x, if provided

        Returns:
            Tuple of (z, u, z_tilde, u_tilde, results) containing initial values
        """
        if warm_start is None:
            x = np.zeros(self.params.q.shape[0])
            z = np.zeros(self.m)
            z_tilde = np.zeros(self.params.B.shape[0])
        else:
            x = warm_start.copy()
            z = self.params.A @ warm_start
            # B @ warm_start might be sparse and needs conversion
            z_tilde = self.params.B @ warm_start
            if sp.sparse.issparse(z_tilde):
                z_tilde = z_tilde.toarray().ravel()

        u = np.zeros(self.m)
        u_tilde = np.zeros(self.params.B.shape[0])

        results = CVQPResults(
            x=x,
            iter_count=0,
            solve_time=0,
            objval=[],
            r_norm=[],
            s_norm=[],
            eps_pri=[],
            eps_dual=[],
            rho=[],
        )

        return z, u, z_tilde, u_tilde, results

    def x_update(
        self,
        z: np.ndarray,
        u: np.ndarray,
        z_tilde: np.ndarray,
        u_tilde: np.ndarray,
        rho: float,
    ) -> np.ndarray:
        """
        Perform x-minimization step of ADMM.

        Args:
            z: First auxiliary variable
            u: First dual variable
            z_tilde: Second auxiliary variable
            u_tilde: Second dual variable
            rho: Current penalty parameter

        Returns:
            Updated x variable
        """
        rhs = (
            -self.params.q
            + rho * (self.params.A.T @ (z - u))
            + rho * (self.params.B.T @ (z_tilde - u_tilde))
        )
        return sp.linalg.lu_solve(self.factor, rhs)

    def z_update(
        self, x: np.ndarray, z: np.ndarray, u: np.ndarray, alpha_over: float
    ) -> np.ndarray:
        """
        Perform z-minimization step of ADMM with over-relaxation.

        Args:
            x: Current primal variable
            z: Current z variable
            u: Current dual variable
            alpha_over: Over-relaxation parameter

        Returns:
            Updated z variable after projection
        """
        z_hat = alpha_over * (self.params.A @ x) + (1 - alpha_over) * z + u
        return proj_sum_largest(z_hat, self.k, self.alpha)

    def z_tilde_update(
        self, x: np.ndarray, z_tilde: np.ndarray, u_tilde: np.ndarray, alpha_over: float
    ) -> np.ndarray:
        """
        Perform z_tilde-minimization step of ADMM with over-relaxation.

        Args:
            x: Current primal variable
            z_tilde: Current z_tilde variable
            u_tilde: Current dual variable
            alpha_over: Over-relaxation parameter

        Returns:
            Updated z_tilde variable after projection
        """
        # If B is sparse, Bx will be a sparse matrix result that needs to be converted to dense
        Bx = self.params.B @ x
        if sp.sparse.issparse(Bx):
            Bx = Bx.toarray().ravel()

        z_hat_tilde = alpha_over * Bx + (1 - alpha_over) * z_tilde + u_tilde
        return np.clip(z_hat_tilde, self.params.l, self.params.u)

    def compute_residuals(
        self,
        x: np.ndarray,
        z: np.ndarray,
        z_tilde: np.ndarray,
        z_old: np.ndarray,
        z_tilde_old: np.ndarray,
        rho: float,
    ) -> tuple:
        """
        Compute primal and dual residuals for convergence checking.

        Args:
            x: Current primal variable
            z, z_tilde: Current auxiliary variables
            z_old, z_tilde_old: Previous auxiliary variables
            rho: Current penalty parameter

        Returns:
            Tuple of (r_norm, s_norm, Ax, At_z) containing residual norms and intermediate products
        """
        Ax = self.params.A @ x
        Bx = self.params.B @ x

        # Need to convert sparse Bx to dense before concatenation
        if sp.sparse.issparse(Bx):
            Bx = Bx.toarray().ravel()

        r = np.concatenate([Ax - z, Bx - z_tilde])
        r_norm = np.linalg.norm(r)

        z_diff = z - z_old
        z_tilde_diff = z_tilde - z_tilde_old

        # Handle sparse transpose operation
        Bt_z = self.params.B.T @ z_tilde_diff
        if sp.sparse.issparse(Bt_z):
            At_z = self.params.A.T @ z_diff + Bt_z.toarray().ravel()
        else:
            At_z = self.params.A.T @ z_diff + Bt_z

        s_norm = np.linalg.norm(rho * At_z)

        return r_norm, s_norm, Ax, At_z

    def compute_tolerances(
        self,
        Ax: np.ndarray,
        z: np.ndarray,
        z_tilde: np.ndarray,
        At_z: np.ndarray,
        rho: float,
    ) -> tuple:
        """
        Compute primal and dual feasibility tolerances.

        Args:
            Ax: Product of A and x
            z, z_tilde: Current auxiliary variables
            At_z: Transposed product
            rho: Current penalty parameter

        Returns:
            Tuple of (eps_pri, eps_dual) containing primal and dual tolerances
        """
        d0 = self.params.A.shape[0] + self.params.B.shape[0]
        d1 = self.params.A.shape[1]

        # If B is sparse, At_z might be sparse
        if sp.sparse.issparse(At_z):
            At_z = At_z.toarray().ravel()

        eps_pri = (d0**0.5) * self.options.abstol + self.options.reltol * max(
            np.linalg.norm(Ax), np.linalg.norm(np.concatenate([z, z_tilde]))
        )
        eps_dual = (
            d1**0.5
        ) * self.options.abstol + self.options.reltol * np.linalg.norm(rho * At_z)

        return eps_pri, eps_dual

    def check_convergence(
        self, r_norm: float, s_norm: float, eps_pri: float, eps_dual: float
    ) -> bool:
        """
        Check if convergence criteria are satisfied.

        Args:
            r_norm: Primal residual norm
            s_norm: Dual residual norm
            eps_pri: Primal feasibility tolerance
            eps_dual: Dual feasibility tolerance

        Returns:
            True if both primal and dual residuals are within tolerances
        """
        return r_norm <= eps_pri and s_norm <= eps_dual

    def update_rho(
        self,
        rho: float,
        r_norm: float,
        s_norm: float,
        u: np.ndarray,
        u_tilde: np.ndarray,
    ) -> tuple:
        """
        Update penalty parameter using adaptive scheme.

        Args:
            rho: Current penalty parameter
            r_norm: Primal residual norm
            s_norm: Dual residual norm
            u, u_tilde: Current dual variables

        Returns:
            Tuple of (rho, u, u_tilde) containing updated values
        """
        if r_norm > self.options.mu * s_norm:
            rho *= self.options.rho_incr
            u /= self.options.rho_incr
            u_tilde /= self.options.rho_incr
            self.update_M_factor(rho)
        elif s_norm > self.options.mu * r_norm:
            rho /= self.options.rho_decr
            u *= self.options.rho_decr
            u_tilde *= self.options.rho_decr
            self.update_M_factor(rho)
        return rho, u, u_tilde

    def setup_progress_display(self):
        """Initialize progress display formatting and headers."""
        self.header_titles = [
            "iter",
            "r_norm",
            "eps_pri",
            "s_norm",
            "eps_dual",
            "rho",
            "obj_val",
        ]
        self.header_format = "{:<6} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}"
        self.row_format = (
            "{:<6} {:<12.3e} {:<12.3e} {:<12.3e} {:<12.3e} {:<12.2e} {:<12.3e}"
        )
        self.separator = "=" * 83

        logging.info(self.separator)
        title = "CVQP solver"
        logging.info(title.center(len(self.separator)))
        logging.info(self.separator)
        logging.info(self.header_format.format(*self.header_titles))
        logging.info("-" * 83)

    def print_iteration(
        self,
        iteration: int,
        r_norm: float,
        eps_pri: float,
        s_norm: float,
        eps_dual: float,
        rho: float,
        objval: float,
    ):
        """
        Print iteration results in formatted output.

        Args:
            iteration: Current iteration number
            r_norm: Primal residual norm
            eps_pri: Primal feasibility tolerance
            s_norm: Dual residual norm
            eps_dual: Dual feasibility tolerance
            rho: Current penalty parameter
            objval: Current objective value
        """
        logging.info(
            self.row_format.format(
                iteration, r_norm, eps_pri, s_norm, eps_dual, rho, objval
            )
        )

    def print_final_results(self, results: CVQPResults):
        """
        Print final optimization results summary.

        Args:
            results: Optimization results containing final values and statistics
        """
        logging.info(self.separator)
        logging.info(f"Optimal value: {results.objval[-1]:.3e}")
        logging.info(f"Solver took {results.solve_time:.2f} seconds")
        logging.info(f"Problem status: {results.problem_status}")

    def record_iteration(
        self,
        results: CVQPResults,
        x: np.ndarray,
        r_norm: float,
        s_norm: float,
        eps_pri: float,
        eps_dual: float,
        rho: float,
    ):
        """
        Record the results of the current iteration for convergence analysis.

        Args:
            results: Results object to store iteration data
            x: Current primal variable
            r_norm: Primal residual norm
            s_norm: Dual residual norm
            eps_pri: Primal feasibility tolerance
            eps_dual: Dual feasibility tolerance
            rho: Current penalty parameter
        """
        if self.params.P is not None:
            if sp.sparse.issparse(self.params.P):
                Px = self.params.P @ x
                objval = (0.5 * x.T @ Px + self.params.q @ x) * self.scale
            else:
                objval = (
                    0.5 * np.dot(x, self.params.P @ x) + self.params.q @ x
                ) * self.scale
        else:
            objval = (self.params.q @ x) * self.scale
        results.objval.append(objval)
        results.r_norm.append(r_norm)
        results.s_norm.append(s_norm)
        results.eps_pri.append(eps_pri)
        results.eps_dual.append(eps_dual)
        results.rho.append(rho)

    def unscale_problem(self):
        """Restore original problem scaling for final results."""
        self.params.A *= self.scale
        self.params.q *= self.scale
        if self.params.P is not None:
            if sp.sparse.issparse(self.params.P):
                self.params.P = self.params.P * self.scale
            else:
                self.params.P *= self.scale

    def solve(self, warm_start: np.ndarray | None = None) -> CVQPResults:
        """
        Solve the optimization problem using ADMM algorithm.

        Args:
            warm_start: Optional initial guess for x variable

        Returns:
            CVQPResults object containing optimal solution and convergence information
        """
        start_time = time.time()

        # Initialize variables and results
        z, u, z_tilde, u_tilde, results = self.initialize_variables(warm_start)
        rho = self.options.rho

        # Setup progress display if verbose
        if self.options.verbose:
            self.setup_progress_display()

        # Main iteration loop
        for i in range(self.options.max_iter):
            # Store previous values
            z_old, z_tilde_old = z.copy(), z_tilde.copy()

            # Update primal and dual variables
            x = self.x_update(z, u, z_tilde, u_tilde, rho)
            z = self.z_update(x, z, u, self.options.alpha_over)
            z_tilde = self.z_tilde_update(x, z_tilde, u_tilde, self.options.alpha_over)

            # Update dual variables
            u += (
                self.options.alpha_over * (self.params.A @ x)
                + (1 - self.options.alpha_over) * z_old
                - z
            )
            Bx = self.params.B @ x  # For sparse B, need to convert result to dense
            if sp.sparse.issparse(Bx):
                Bx = Bx.toarray().ravel()

            u_tilde += (
                self.options.alpha_over * Bx
                + (1 - self.options.alpha_over) * z_tilde_old
                - z_tilde
            )

            # Check convergence periodically
            if i % self.options.print_freq == 0:
                # Compute residuals and tolerances
                r_norm, s_norm, Ax, At_z = self.compute_residuals(
                    x, z, z_tilde, z_old, z_tilde_old, rho
                )
                eps_pri, eps_dual = self.compute_tolerances(Ax, z, z_tilde, At_z, rho)

                # Record iteration
                self.record_iteration(
                    results, x, r_norm, s_norm, eps_pri, eps_dual, rho
                )

                # Print progress if verbose
                if self.options.verbose:
                    self.print_iteration(
                        i, r_norm, eps_pri, s_norm, eps_dual, rho, results.objval[-1]
                    )

                # Check time limit
                if time.time() - start_time > self.options.time_limit:
                    results.problem_status = "timeout"
                    break

                # Check convergence
                if self.check_convergence(r_norm, s_norm, eps_pri, eps_dual):
                    results.problem_status = "optimal"
                    break

                # Update penalty parameter
                if self.options.dynamic_rho:
                    rho, u, u_tilde = self.update_rho(rho, r_norm, s_norm, u, u_tilde)

        # Finalize results
        self.unscale_problem()
        results.x = x
        results.iter_count = i + 1
        results.solve_time = time.time() - start_time

        if self.options.verbose:
            self.print_final_results(results)

        return results