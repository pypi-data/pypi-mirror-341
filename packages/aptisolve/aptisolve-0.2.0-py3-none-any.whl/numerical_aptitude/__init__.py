from .number_system import convert_base, find_lcm_hcf
from .probability import (
    calculate_probability,
    calculate_compound_probability,
    calculate_conditional_probability,
    calculate_bayes_theorem
)
from .permutations_combinations import (
    calculate_factorial,
    calculate_permutation,
    calculate_combination,
    permutation_with_repetition,
    combination_with_repetition
)
from .profit_loss import (
    calculate_profit_loss,
    calculate_cost_price,
    calculate_selling_price,
    calculate_marked_price,
    calculate_successive_discounts
)
from .percentages import calculate_percentage, percentage_change
from .simple_interest import calculate_simple_interest
from .compound_interest import calculate_compound_interest
from .time_work import calculate_time_work, work_efficiency
from .time_speed_distance import calculate_tsd, average_speed
from .ratios_proportions import calculate_ratio, find_proportion
from .averages import calculate_mean, calculate_median, calculate_mode
from .mixtures_alligations import calculate_mixture_ratio, calculate_mean_price
from .algebra import solve_linear_equation, solve_quadratic_equation

__all__ = [
    # Number Systems
    'convert_base',
    'find_lcm_hcf',
    
    # Probability
    'calculate_probability',
    'calculate_compound_probability',
    'calculate_conditional_probability',
    'calculate_bayes_theorem',
    
    # Permutations & Combinations
    'calculate_factorial',
    'calculate_permutation',
    'calculate_combination',
    'permutation_with_repetition',
    'combination_with_repetition',
    
    # Profit & Loss
    'calculate_profit_loss',
    'calculate_cost_price',
    'calculate_selling_price',
    'calculate_marked_price',
    'calculate_successive_discounts',
    
    # Percentages
    'calculate_percentage',
    'percentage_change',
    
    # Interest
    'calculate_simple_interest',
    'calculate_compound_interest',
    
    # Time & Work
    'calculate_time_work',
    'work_efficiency',
    
    # Time, Speed & Distance
    'calculate_tsd',
    'average_speed',
    
    # Ratios & Proportions
    'calculate_ratio',
    'find_proportion',
    
    # Averages
    'calculate_mean',
    'calculate_median',
    'calculate_mode',
    
    # Mixtures & Alligations
    'calculate_mixture_ratio',
    'calculate_mean_price',
    
    # Algebra
    'solve_linear_equation',
    'solve_quadratic_equation'
]


__version__ = "0.2.0"
