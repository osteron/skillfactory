import pytest
from app.calculator import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculate_correctly(self):
        assert self.calc.multiplication(self, 2, 2) == 4

    def test_division_calculate_correctly(self):
        assert self.calc.division(self, 4, 2) == 2

    def test_addition_calculate_correctly(self):
        assert self.calc.addition(self, 5, 6) == 11

    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(self, 10, 4) == 6
        