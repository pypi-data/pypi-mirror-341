import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_interpretation.tables import analyze_table, compare_data_points
from data_interpretation.graphs import analyze_line_graph, find_growth_rate
from data_interpretation.charts import analyze_pie_chart, find_largest_segment

class TestTables:
    def test_analyze_table(self):
        # Sample table data (2D list)
        table_data = [
            ["Product", "Q1", "Q2", "Q3", "Q4"],
            ["Product A", 100, 120, 140, 160],
            ["Product B", 200, 180, 160, 140],
            ["Product C", 150, 150, 150, 150]
        ]
        
        question = "Which product showed consistent sales throughout the year?"
        
        result = analyze_table(table_data, question)
        assert isinstance(result, dict)
        assert "answer" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result
    
    def test_compare_data_points(self):
        # Sample table data
        table_data = [
            ["Product", "Q1", "Q2", "Q3", "Q4"],
            ["Product A", 100, 120, 140, 160],
            ["Product B", 200, 180, 160, 140],
            ["Product C", 150, 150, 150, 150]
        ]
        
        categories = ["Product A", "Product B", "Product C"]
        metric = "Q1"
        
        result = compare_data_points(table_data, categories, metric)
        assert isinstance(result, dict)
        assert "result" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result

class TestGraphs:
    def test_analyze_line_graph(self):
        x_values = [2018, 2019, 2020, 2021, 2022]
        y_values = [100, 120, 110, 130, 150]
        question = "What was the trend of values from 2018 to 2022?"
        
        result = analyze_line_graph(x_values, y_values, question)
        assert isinstance(result, dict)
        assert "answer" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result
    
    def test_find_growth_rate(self):
        x_values = [2018, 2019, 2020, 2021, 2022]
        y_values = [100, 120, 110, 130, 150]
        
        # Test valid indices
        result = find_growth_rate(x_values, y_values, 0, 4)
        assert isinstance(result, dict)
        assert "growth_rate" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result
        
        # Test invalid indices
        result = find_growth_rate(x_values, y_values, 0, 10)
        assert isinstance(result, dict)
        assert "growth_rate" in result
        assert result["growth_rate"] == "Error: Index out of range"

class TestCharts:
    def test_analyze_pie_chart(self):
        categories = ["Category A", "Category B", "Category C", "Category D"]
        values = [30, 20, 15, 35]
        question = "Which category has the largest share?"
        
        result = analyze_pie_chart(categories, values, question)
        assert isinstance(result, dict)
        assert "answer" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result
    
    def test_find_largest_segment(self):
        categories = ["Category A", "Category B", "Category C", "Category D"]
        values = [30, 20, 15, 35]
        
        result = find_largest_segment(categories, values)
        assert isinstance(result, dict)
        assert "largest_segment" in result
        assert result["largest_segment"] == "Category D"
        assert result["value"] == 35
        assert result["percentage"] == 35
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "practice_tip" in result
        
        # Test empty input
        result = find_largest_segment([], [])
        assert isinstance(result, dict)
        assert "largest_segment" in result
        assert result["largest_segment"] == "Error: Invalid input data"