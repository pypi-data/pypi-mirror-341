"""
Hypertrial: Bitcoin Dollar-Cost Averaging (DCA) Backtest Framework

A Python-based backtesting framework for evaluating Bitcoin DCA strategy 
performance across multiple market cycles.

The framework provides tools to:
- Develop and test custom DCA strategies
- Backtest strategies against historical Bitcoin price data
- Compare performance metrics using Sats Per Dollar (SPD)
- Visualize results across different market cycles

Installation:
    pip install hypertrial

Official repository: https://github.com/mattfaltyn/hypertrial
PyPI package: https://pypi.org/project/hypertrial/
"""

__version__ = "0.1.13"

# Make the security module available at the package level
from core import security

# Import and expose key functions
from core.main import main
from core.strategies import register_strategy, load_strategies, get_strategy, list_strategies
from core.spd import backtest_dynamic_dca, compute_cycle_spd
from core.data import load_data
from core.plots import plot_price_vs_lookback_avg, plot_final_weights, plot_weight_sums_by_cycle

# Define public API
__all__ = [
    'main',
    'register_strategy',
    'load_strategies',
    'get_strategy',
    'list_strategies',
    'backtest_dynamic_dca',
    'compute_cycle_spd',
    'load_data',
    'plot_price_vs_lookback_avg',
    'plot_final_weights',
    'plot_weight_sums_by_cycle',
    'security'
] 