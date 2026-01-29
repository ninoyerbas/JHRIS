"""Validation utilities for JHRIS."""

import re
from datetime import datetime
from constants import EMAIL_PATTERN, DATE_PATTERN, ALLOWED_STATUSES


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required."
    
    if not re.match(EMAIL_PATTERN, email):
        return False, "Invalid email format."
    
    return True, None


def validate_date(date_str):
    """
    Validate date format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not date_str:
        return False, "Date is required."
    
    if not re.match(DATE_PATTERN, date_str):
        return False, "Invalid date format. Use YYYY-MM-DD."
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, "Invalid date value."


def validate_salary(salary):
    """
    Validate salary value.
    
    Args:
        salary: Salary value to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        salary_float = float(salary)
        if salary_float < 0:
            return False, "Salary cannot be negative."
        return True, None
    except (ValueError, TypeError):
        return False, "Invalid salary value."


def validate_status(status):
    """
    Validate employee status.
    
    Args:
        status: Status value to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if status not in ALLOWED_STATUSES:
        return False, f"Status must be one of: {', '.join(ALLOWED_STATUSES)}"
    return True, None


def validate_positive_int(value, field_name="Value"):
    """
    Validate that a value is a positive integer.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        tuple: (is_valid, parsed_value, error_message)
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            return False, None, f"{field_name} must be a positive number."
        return True, int_value, None
    except (ValueError, TypeError):
        return False, None, f"{field_name} must be a valid number."
