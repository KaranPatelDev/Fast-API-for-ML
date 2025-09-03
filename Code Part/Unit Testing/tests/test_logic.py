import pytest
from app.logic import is_eligible_for_loan

def test_eligible_user():
    assert is_eligible_for_loan(60000, 25, 'employed') == True
    assert is_eligible_for_loan(40000, 25, 'employed') == False

def test_underage_user():
    assert is_eligible_for_loan(70000, 18, 'employed') == False

def test_low_income():
    assert is_eligible_for_loan(30000, 30, 'employed') == False

def test_unemployed_user():
    assert is_eligible_for_loan(80000, 28, 'unemployed') == False

def test_boundary_conditions():
    assert is_eligible_for_loan(50000, 21, 'employed') == True
    assert is_eligible_for_loan(49999, 21, 'employed') == False
    assert is_eligible_for_loan(50000, 20, 'employed') == False
    assert is_eligible_for_loan(50000, 21, 'unemployed') == False

