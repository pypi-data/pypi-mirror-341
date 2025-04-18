"""
Random Allocation for Differential Privacy

This package provides tools for analyzing and comparing different random allocation schemes
in the context of differential privacy.
"""

def check_dependencies():
    """Check that all dependencies are properly installed and compatible."""
    try:
        import numpy
        import scipy
        import matplotlib
        import pandas
        import numba
        import dp_accounting
        
        # Optional: Add version checks
        np_version = numpy.__version__.split('.')
        major, minor = int(np_version[0]), int(np_version[1])
        
        if major < 1 or (major == 1 and minor < 21):
            print(f"Warning: NumPy version {numpy.__version__} is older than recommended (1.21.0)")
            
        # Test critical NumPy functionality
        try:
            import numpy.random
            numpy.random.RandomState()
        except Exception as e:
            print(f"NumPy functionality issue detected: {e}")
            print("This might cause issues when using random_allocation")
            print("Try: pip install numpy==1.21.6 dp_accounting==0.4.4 random_allocation")
        
        return True
    except ImportError as e:
        print(f"Warning: Dependency issue detected: {e}")
        print("Try: pip install numpy==1.21.6 dp_accounting==0.4.4 random_allocation")
        return False

# Run check on import
dependency_check = check_dependencies()

# Original imports
from random_allocation.comparisons.experiments import run_experiment, PlotType
from random_allocation.comparisons.visualization import plot_comparison, plot_combined_data, plot_as_table
from random_allocation.comparisons.definitions import (
    ALLOCATION, ALLOCATION_ANALYTIC, ALLOCATION_RDP, ALLOCATION_DECOMPOSITION,
    EPSILON, DELTA, VARIABLES, methods_dict, names_dict, colors_dict
)
from random_allocation.random_allocation_scheme import (
    allocation_epsilon_analytic, allocation_delta_analytic,
    allocation_epsilon_rdp, allocation_delta_rdp,
    allocation_epsilon_rdp_loose, allocation_delta_rdp_loose,
    allocation_epsilon_decomposition, allocation_delta_decomposition
)

__all__ = [
    # Experiment functions
    'run_experiment',
    'PlotType',
    
    # Plotting functions
    'plot_comparison',
    'plot_combined_data',
    'plot_as_table',
    
    # Constants and configurations
    'ALLOCATION',
    'ALLOCATION_ANALYTIC',
    'ALLOCATION_RDP',
    'ALLOCATION_DECOMPOSITION',
    'EPSILON',
    'DELTA',
    'VARIABLES',
    'methods_dict',
    'names_dict',
    'colors_dict',
    
    # Core allocation functions
    'allocation_epsilon_analytic',
    'allocation_delta_analytic',
    'allocation_epsilon_rdp',
    'allocation_delta_rdp',
    'allocation_epsilon_rdp_loose',
    'allocation_delta_rdp_loose',
    'allocation_epsilon_decomposition',
    'allocation_delta_decomposition'
]