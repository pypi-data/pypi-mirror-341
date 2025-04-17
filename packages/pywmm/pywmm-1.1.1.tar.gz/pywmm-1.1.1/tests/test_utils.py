import unittest
from datetime import datetime, timedelta
import calendar

from pywmm.date_utils import date_range, decimal_year

class TestUtils(unittest.TestCase):
    """Test suite for utility functions in the PyWMM package"""
    
    def test_date_range_normal(self):
        """Test date_range with normal inputs"""
        # Test with 2-day steps
        dates = date_range("2024-01-01", "2024-01-10", 2)
        expected = ["2024-01-01", "2024-01-03", "2024-01-05", "2024-01-07", "2024-01-09"]
        self.assertEqual(dates, expected)
        
        # Test with 1-day steps
        dates = date_range("2024-03-29", "2024-04-02", 1)
        expected = ["2024-03-29", "2024-03-30", "2024-03-31", "2024-04-01", "2024-04-02"]
        self.assertEqual(dates, expected)
        
        # Test with monthly steps (30 days)
        dates = date_range("2024-01-15", "2024-06-15", 30)
        expected = ["2024-01-15", "2024-02-14", "2024-03-15", "2024-04-14", "2024-05-14", "2024-06-13"]
        self.assertEqual(dates, expected)
    
    def test_date_range_edge_cases(self):
        """Test date_range with edge cases"""
        # Single day (start == end)
        dates = date_range("2024-05-01", "2024-05-01", 1)
        self.assertEqual(dates, ["2024-05-01"])
        
        # No days in range due to step size
        dates = date_range("2024-05-01", "2024-05-02", 3)
        self.assertEqual(dates, ["2024-05-01"])
        
        # Leap year crossing
        dates = date_range("2024-02-28", "2024-03-02", 1)
        expected = ["2024-02-28", "2024-02-29", "2024-03-01", "2024-03-02"]
        self.assertEqual(dates, expected)
        
        # Year boundary crossing
        dates = date_range("2023-12-30", "2024-01-03", 2)
        expected = ["2023-12-30", "2024-01-01", "2024-01-03"]
        self.assertEqual(dates, expected)
    
    def test_date_range_invalid_inputs(self):
        """Test date_range with invalid inputs"""
        # Invalid date formats
        with self.assertRaises(ValueError):
            date_range("invalid-date", "2024-01-10", 1)
        
        with self.assertRaises(ValueError):
            date_range("2024-01-01", "not-a-date", 1)
        
        with self.assertRaises(ValueError):
            date_range("2024/01/01", "2024/01/10", 1)  # Wrong format
        
        # End date before start date
        dates = date_range("2024-02-10", "2024-02-05", 1)
        self.assertEqual(dates, ["2024-02-10"])  # Just the start date
        
        # Invalid step sizes
        with self.assertRaises(ValueError):
            date_range("2024-01-01", "2024-01-10", 0)
        
        with self.assertRaises(ValueError):
            date_range("2024-01-01", "2024-01-10", -1)
    
    def test_decimal_year_non_leap_year(self):
        """Test decimal_year for non-leap years (365 days)"""
        # Start of year
        year = decimal_year("2023-01-01")
        self.assertEqual(year, 2023.0)
        
        # End of year
        year = decimal_year("2023-12-31")
        self.assertAlmostEqual(year, 2024.0, delta=0.0028)  # 1/365 accuracy
        
        # Middle of year
        year = decimal_year("2023-07-02")
        days_passed = 31 + 28 + 31 + 30 + 31 + 30 + 1  # 182 days (approximate mid-year)
        expected = 2023.0 + (days_passed / 365.0)
        self.assertAlmostEqual(year, expected, delta=0.0028)
        
        # Quarter year
        year = decimal_year("2023-04-01")
        days_passed = 31 + 28 + 31  # 90 days
        expected = 2023.0 + (days_passed / 365.0)
        self.assertAlmostEqual(year, expected, delta=0.0028)
    
    def test_decimal_year_leap_year(self):
        """Test decimal_year for leap years (366 days)"""
        # Start of leap year
        year = decimal_year("2024-01-01")
        self.assertEqual(year, 2024.0)
        
        # End of leap year
        year = decimal_year("2024-12-31")
        self.assertAlmostEqual(year, 2025.0, delta=0.0028)  # 1/366 accuracy
        
        # Leap day
        year = decimal_year("2024-02-29")
        days_passed = 31 + 29
        expected = 2024.0 + (days_passed / 366.0)
        self.assertAlmostEqual(year, expected, delta=0.0028)
        
        # Middle of leap year (day 183)
        year = decimal_year("2024-07-01")
        days_passed = 31 + 29 + 31 + 30 + 31 + 30  # 182 days
        expected = 2024.0 + (days_passed / 366.0)
        self.assertAlmostEqual(year, expected, delta=0.0028)
    
    def test_decimal_year_invalid_inputs(self):
        """Test decimal_year with invalid inputs"""
        # Invalid date formats
        with self.assertRaises(ValueError):
            decimal_year("not-a-date")
        
        with self.assertRaises(ValueError):
            decimal_year("2024/01/01")  # Wrong format
        
        with self.assertRaises(ValueError):
            decimal_year("2024-13-01")  # Invalid month
        
        with self.assertRaises(ValueError):
            decimal_year("2024-02-30")  # Invalid day

    def test_against_manual_calculation(self):
        """Test decimal_year against manual calculations"""
        # Test a few dates with manually calculated values
        
        # Non-leap year: 2023-03-15
        # Day of year: 31 (Jan) + 28 (Feb) + 15 = 74
        # Decimal: 2023 + (74 / 365) = 2023.2027...
        self.assertAlmostEqual(decimal_year("2023-03-15"), 2023.0 + 74/365, delta=0.0001)
        
        # Leap year: 2024-03-15
        # Day of year: 31 (Jan) + 29 (Feb) + 15 = 75
        # Decimal: 2024 + (75 / 366) = 2024.2049...
        self.assertAlmostEqual(decimal_year("2024-03-15"), 2024.0 + 75/366, delta=0.0001)
        
        # Test implementation matches expected algorithm
        test_date_str = "2024-09-15"
        test_date = datetime.strptime(test_date_str, "%Y-%m-%d").date()
        days_in_year = 366 if calendar.isleap(test_date.year) else 365
        day_of_year = test_date.timetuple().tm_yday
        expected_decimal = test_date.year + (day_of_year / days_in_year)
        self.assertAlmostEqual(decimal_year(test_date_str), expected_decimal, delta=0.0001)


if __name__ == "__main__":
    unittest.main()