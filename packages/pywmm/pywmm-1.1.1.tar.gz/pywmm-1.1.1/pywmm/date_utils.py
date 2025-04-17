import calendar
from datetime import datetime, timedelta

def date_range(start_date: str, end_date: str, step_days: int):
    """
    Generate a list of dates between start_date and end_date with a specified interval.
    
    Parameters:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        step_days (int): The interval between dates in days. Must be a positive integer.
    
    Returns:
        list: A list of date strings in 'YYYY-MM-DD' format.
        
    Raises:
        ValueError: If the date format is invalid or step_days is not positive.
    
    Example:
        >>> date_range("2024-01-01", "2024-01-10", 2)
        ['2024-01-01', '2024-01-03', '2024-01-05', '2024-01-07', '2024-01-09']
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

    if step_days <= 0:
        raise ValueError("step_days must be a positive integer")

    step = timedelta(days=step_days)
    dates = []
    current_date = start
    while current_date <= end:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += step
    return dates

def decimal_year(date_str: str) -> float:
    """
    Convert a date string to a decimal year representation.
    
    The decimal portion represents the fraction of the year that has elapsed.
    Accounts for leap years when calculating the fraction.
    
    Parameters:
        date_str (str): The date in 'YYYY-MM-DD' format.
        
    Returns:
        float: The date as a decimal year (e.g., 2024.5 for July 1, 2024 in a leap year).
        
    Raises:
        ValueError: If the date format is invalid.
        
    Example:
        >>> decimal_year("2024-07-01")
        2024.5
    """
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

    days_in_year = 366 if calendar.isleap(date_object.year) else 365
    return date_object.year + (date_object.timetuple().tm_yday / days_in_year)


if __name__ == "__main__":
    try:
        print(date_range("2024-01-01", "2024-01-10", 2))
        print(decimal_year("2024-07-01"))
    except ValueError as e:
        print(e)