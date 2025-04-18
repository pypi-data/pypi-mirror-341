# CVQP: A Python implementation of the CVQP solver

__version__ = "0.1.0"

from .solver import CVQP, CVQPParams, CVQPResults, CVQPConfig
from .projection import proj_sum_largest

__all__ = ["CVQP", "CVQPParams", "CVQPResults", "CVQPConfig", "proj_sum_largest"]
