# Data Interpretation module for AptiSolve package

from .tables import (
    analyze_table,
    compare_data_points,
    find_trends,
    calculate_percentage_change,
    summarize_data
)

from .graphs import (
    analyze_line_graph,
    find_growth_rate,
    analyze_bar_graph,
    compare_trends,
    find_intersection_points,
    calculate_slope
)

from .charts import (
    analyze_pie_chart,
    find_largest_segment,
    compare_segments,
    calculate_sector_angles,
    analyze_donut_chart,
    find_percentage_distribution
)

__all__ = [
    # Table Analysis
    'analyze_table',
    'compare_data_points',
    'find_trends',
    'calculate_percentage_change',
    'summarize_data',
    
    # Graph Analysis
    'analyze_line_graph',
    'find_growth_rate',
    'analyze_bar_graph',
    'compare_trends',
    'find_intersection_points',
    'calculate_slope',
    
    # Chart Analysis
    'analyze_pie_chart',
    'find_largest_segment',
    'compare_segments',
    'calculate_sector_angles',
    'analyze_donut_chart',
    'find_percentage_distribution'
]

__version__ = "0.2.0"