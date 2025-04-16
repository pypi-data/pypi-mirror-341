import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from numerical_aptitude.profit_loss import (
    calculate_profit_loss,
    calculate_cost_price,
    calculate_selling_price,
    calculate_marked_price,
    calculate_successive_discounts
)

class TestProfitLoss:
    def test_calculate_profit_loss(self):
        # Test profit case
        result = calculate_profit_loss(100, 120)
        assert isinstance(result, dict)
        assert "result" in result
        assert "percentage" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert "Profit" in result["result"]
        assert result["percentage"] == 20.0
        
        # Test loss case
        result = calculate_profit_loss(100, 80)
        assert "Loss" in result["result"]
        assert result["percentage"] == 20.0
        
        # Test no profit no loss case
        result = calculate_profit_loss(100, 100)
        assert result["result"] == "No Profit No Loss"
        assert result["percentage"] == 0
        
        # Test error case
        result = calculate_profit_loss(-100, 80)
        assert "Error" in result["result"]
    
    def test_calculate_cost_price(self):
        # Test profit case
        result = calculate_cost_price(120, 20, True)
        assert isinstance(result, dict)
        assert "cost_price" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert abs(result["cost_price"] - 100) < 0.01
        
        # Test loss case
        result = calculate_cost_price(80, 20, False)
        assert abs(result["cost_price"] - 100) < 0.01
        
        # Test error case
        result = calculate_cost_price(-120, 20, True)
        assert "Error" in str(result["cost_price"])
    
    def test_calculate_selling_price(self):
        # Test profit case
        result = calculate_selling_price(100, 20, True)
        assert isinstance(result, dict)
        assert "selling_price" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert abs(result["selling_price"] - 120) < 0.01
        
        # Test loss case
        result = calculate_selling_price(100, 20, False)
        assert abs(result["selling_price"] - 80) < 0.01
        
        # Test error case
        result = calculate_selling_price(-100, 20, True)
        assert "Error" in str(result["selling_price"])
    
    def test_calculate_marked_price(self):
        # Test normal case
        result = calculate_marked_price(100, 20, 10)
        assert isinstance(result, dict)
        assert "marked_price" in result
        assert "selling_price" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert abs(result["selling_price"] - 120) < 0.01
        assert abs(result["marked_price"] - 133.33) < 0.01
        
        # Test error case
        result = calculate_marked_price(100, 20, 100)
        assert "Error" in str(result["marked_price"])
    
    def test_calculate_successive_discounts(self):
        # Test single discount
        result = calculate_successive_discounts(1000, [10])
        assert isinstance(result, dict)
        assert "final_price" in result
        assert "equivalent_discount_percentage" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert abs(result["final_price"] - 900) < 0.01
        assert abs(result["equivalent_discount_percentage"] - 10) < 0.01
        
        # Test multiple discounts
        result = calculate_successive_discounts(1000, [10, 20])
        assert abs(result["final_price"] - 720) < 0.01
        assert abs(result["equivalent_discount_percentage"] - 28) < 0.01
        
        # Test error case
        result = calculate_successive_discounts(1000, [10, 110])
        assert "Error" in str(result["final_price"])