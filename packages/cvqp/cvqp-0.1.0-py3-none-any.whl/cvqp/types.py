"""
Type definitions for the CVQP solver.
"""

from dataclasses import dataclass
import numpy as np
import scipy as sp


@dataclass
class CVQPParams:
    """
    Parameters defining a CVQP instance.

    Args:
        P: Quadratic cost matrix in objective (can be np.ndarray, scipy.sparse.spmatrix, or None)
        q: Linear cost vector in objective
        A: Matrix for CVaR constraint
        B: Linear constraint matrix (can be np.ndarray or scipy.sparse.spmatrix)
        l: Lower bounds for Bx
        u: Upper bounds for Bx
        beta: Probability level for CVaR constraint
        kappa: CVaR limit for CVaR constraint
    """

    P: np.ndarray | sp.sparse.spmatrix | None
    q: np.ndarray
    A: np.ndarray
    B: np.ndarray | sp.sparse.spmatrix
    l: np.ndarray
    u: np.ndarray
    beta: float
    kappa: float


@dataclass
class CVQPConfig:
    """
    Configuration parameters for the CVQP solver.

    Args:
        max_iter: Maximum number of iterations before termination
        rho: Initial penalty parameter for augmented Lagrangian
        abstol: Absolute tolerance for primal and dual residuals
        reltol: Relative tolerance for primal and dual residuals
        alpha_over: Over-relaxation parameter for improved convergence (typically in [1.5, 1.8])
        print_freq: Frequency of iteration status updates
        mu: Threshold parameter for adaptive rho updates
        rho_incr: Multiplicative factor for increasing rho
        rho_decr: Multiplicative factor for decreasing rho
        verbose: If True, prints detailed convergence information
        time_limit: Maximum time in seconds before termination (default: 3600s = 1h)
        dynamic_rho: If True, adaptively updates the penalty parameter rho during optimization
    """

    max_iter: int = int(1e5)
    rho: float = 1e-2
    abstol: float = 1e-4
    reltol: float = 1e-3
    alpha_over: float = 1.7
    print_freq: int = 50
    mu: float = 10
    rho_incr: float = 2.0
    rho_decr: float = 2.0
    verbose: bool = False
    time_limit: float = 7200
    dynamic_rho: bool = True


@dataclass
class CVQPResults:
    """
    Results from the CVQP solver.

    Attributes:
        x: Optimal solution vector
        iter_count: Number of iterations performed
        solve_time: Total solve time in seconds
        objval: List of objective values at each iteration
        r_norm: List of primal residual norms
        s_norm: List of dual residual norms
        eps_pri: List of primal feasibility tolerances
        eps_dual: List of dual feasibility tolerances
        rho: List of penalty parameter values
        problem_status: Final status of the solve ("optimal", "unknown", etc.)
    """

    x: np.ndarray
    iter_count: int
    solve_time: float
    objval: list[float]
    r_norm: list[float]
    s_norm: list[float]
    eps_pri: list[float]
    eps_dual: list[float]
    rho: list[float]
    problem_status: str = "unknown"