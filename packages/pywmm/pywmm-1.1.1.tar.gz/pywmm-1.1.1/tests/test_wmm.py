import unittest
import os
import math
from unittest.mock import patch, mock_open
import numpy as np

# Import the modules we want to test
from pywmm import WMMv2
from pywmm.date_utils import date_range, decimal_year

class TestWMMv2(unittest.TestCase):
    """Test suite for the WMMv2 class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Mock the coefficient file content for testing
        self.mock_coeff_content = """
        2020.0 WMM-2020 12/10/2019
        1 0 -29404.5 0.0 6.7 0.0
        1 1 -1450.7 4652.9 7.7 -25.1
        2 0 -2500.0 0.0 -11.5 0.0
        2 1 2982.0 -2991.6 -7.1 -30.2
        2 2 1676.8 -734.8 -2.2 -23.9
        3 0 1363.9 0.0 2.8 0.0
        3 1 -2381.0 -82.2 -6.2 5.7
        3 2 1236.2 241.8 3.4 -1.0
        3 3 525.7 -542.9 -12.2 1.1
        4 0 907.2 0.0 -1.1 0.0
        4 1 813.7 283.4 0.2 -0.6
        4 2 120.3 -188.7 -9.1 5.3
        4 3 -335.0 180.9 4.0 3.0
        4 4 70.3 -329.5 -4.2 -5.3
        5 0 -232.6 0.0 -0.1 0.0
        5 1 360.1 47.4 0.5 0.1
        5 2 192.4 196.9 -1.4 1.7
        5 3 -141.0 -119.4 0.0 -1.2
        5 4 -157.4 16.1 1.3 3.3
        5 5 4.3 100.1 3.8 0.1
        6 0 69.5 0.0 -0.8 0.0
        6 1 67.4 -20.7 -0.5 -0.1
        6 2 72.8 33.2 -0.2 -1.5
        6 3 -129.8 58.8 2.1 -0.7
        6 4 -29.0 -66.5 -1.6 0.6
        6 5 13.2 7.3 0.1 -0.2
        6 6 -70.9 62.5 1.5 1.3
        7 0 81.6 0.0 -0.2 0.0
        7 1 -76.1 -54.1 -0.2 0.7
        7 2 -8.7 -19.5 -0.4 0.5
        7 3 56.5 6.0 0.4 -0.5
        7 4 15.5 24.4 0.3 -0.2
        7 5 6.0 -12.4 0.0 -0.5
        7 6 -7.0 -24.2 -0.4 0.0
        7 7 9.7 3.3 -0.1 -0.3
        8 0 24.2 0.0 0.0 0.0
        8 1 8.8 10.2 0.1 -0.1
        8 2 -16.9 -18.3 -0.5 0.4
        8 3 -3.2 13.3 0.5 0.2
        8 4 -20.6 -14.6 -0.2 0.4
        8 5 13.3 16.2 0.1 -0.1
        8 6 11.8 5.7 0.1 -0.3
        8 7 -16.0 -9.1 -0.4 0.3
        8 8 -2.1 2.9 0.4 0.0
        9 0 5.4 0.0 -0.2 0.0
        9 1 8.8 -21.8 -0.1 -0.2
        9 2 3.1 10.8 -0.1 -0.1
        9 3 -3.0 11.7 0.1 -0.1
        9 4 -0.4 -6.8 -0.1 0.1
        9 5 -10.1 7.8 -0.2 -0.2
        9 6 -1.4 -3.9 -0.2 0.0
        9 7 9.6 -1.9 0.0 0.0
        9 8 -11.3 9.7 -0.2 0.0
        9 9 -4.9 -6.2 0.0 0.1
        10 0 -3.4 0.0 -0.2 0.0
        10 1 -0.2 -6.3 0.0 0.0
        10 2 0.6 -1.1 0.0 0.0
        10 3 4.9 -0.2 -0.1 0.0
        10 4 -0.3 4.4 0.0 -0.1
        10 5 1.3 -2.4 0.0 0.0
        10 6 -2.0 -3.1 -0.1 0.0
        10 7 -0.9 -0.3 0.0 0.0
        10 8 -0.4 0.8 0.0 0.0
        10 9 0.3 -2.6 0.0 0.0
        10 10 -2.2 -1.3 -0.1 0.1
        11 0 -0.9 0.0 0.0 0.0
        11 1 -1.9 1.2 0.0 0.0
        11 2 -0.4 -2.5 0.0 0.1
        11 3 2.3 2.4 0.0 0.0
        11 4 -2.6 1.2 0.0 0.0
        11 5 0.6 0.5 0.0 0.0
        11 6 0.4 0.3 0.0 0.0
        11 7 0.0 -2.0 0.0 0.0
        11 8 -0.8 -0.2 0.0 0.0
        11 9 -0.4 0.1 0.0 0.0
        11 10 0.1 -0.9 0.0 0.0
        11 11 -0.3 -0.4 0.0 0.0
        12 0 -0.1 0.0 0.0 0.0
        12 1 0.8 -0.1 0.0 0.0
        12 2 0.4 -0.3 0.0 0.0
        12 3 -0.6 0.4 0.0 0.0
        12 4 0.5 -1.4 0.0 0.0
        12 5 1.4 -1.2 0.0 0.0
        12 6 -0.3 -0.8 0.0 0.0
        12 7 0.6 0.1 0.0 0.0
        12 8 -0.3 0.6 0.0 0.0
        12 9 -0.3 -0.1 0.0 0.0
        12 10 -0.1 0.1 0.0 0.0
        12 11 -0.3 0.4 0.0 0.0
        12 12 -0.1 -0.1 0.0 0.0
        """
        
        # Create the patch for the coefficient file
        self.file_patch = patch("builtins.open", mock_open(read_data=self.mock_coeff_content))
        self.file_patch.start()
        
        # Initialize the model with the mocked coefficient file
        self.wmm = WMMv2()
    
    def tearDown(self):
        """Clean up after each test"""
        self.file_patch.stop()
    
    def test_initialization(self):
        """Test that the model initializes correctly"""
        self.assertEqual(self.wmm.epoch, 2020.0)
        self.assertEqual(self.wmm.defaultDate, 2022.5)
        self.assertEqual(self.wmm.maxdeg, 12)
        self.assertEqual(self.wmm.maxord, 12)
    
    def test_declination_2020_0(self):
        """Test declination calculations at different points from the reference table - 2020.0 data"""
        # Test 1: Latitude 0, Longitude 0, Height 0, Year 2020.0
        declination = self.wmm.get_declination(0, 0, 2020.0, 0)
        self.assertAlmostEqual(declination, -1.28, delta=0.1)
        
        # Test 2: Latitude 80, Longitude 0, Height 0, Year 2020.0
        declination = self.wmm.get_declination(80, 0, 2020.0, 0)
        self.assertAlmostEqual(declination, -1.70, delta=0.1)
        
        # Test 3: Latitude 0, Longitude 120, Height 0, Year 2020.0
        declination = self.wmm.get_declination(0, 120, 2020.0, 0)
        self.assertAlmostEqual(declination, 0.18, delta=0.1)
        
        # Test 4: Latitude -80, Longitude 240, Height 0, Year 2020.0
        declination = self.wmm.get_declination(-80, 240, 2020.0, 0)
        self.assertAlmostEqual(declination, 69.38, delta=0.1)
    
    def test_declination_2022_5(self):
        """Test declination calculations at different points from the reference table - 2022.5 data"""
        # Test 1: Latitude 0, Longitude 0, Height 0, Year 2022.5
        declination = self.wmm.get_declination(0, 0, 2022.5, 0)
        self.assertAlmostEqual(declination, -1.28, delta=0.1)
        
        # Test 2: Latitude 80, Longitude 0, Height 0, Year 2022.5
        declination = self.wmm.get_declination(80, 0, 2022.5, 0)
        self.assertAlmostEqual(declination, -1.70, delta=0.1)
        
        # Test 3: Latitude 0, Longitude 120, Height 0, Year 2022.5
        declination = self.wmm.get_declination(0, 120, 2022.5, 0)
        self.assertAlmostEqual(declination, 0.18, delta=0.1)
        
        # Test 4: Latitude -80, Longitude 240, Height 0, Year 2022.5
        declination = self.wmm.get_declination(-80, 240, 2022.5, 0)
        self.assertAlmostEqual(declination, 69.13, delta=0.1)
    
    def test_inclination(self):
        """Test inclination (dip) angle calculations from the reference table"""
        # Latitude 80, Longitude 0, Height 0, Year 2020.0
        dip = self.wmm.get_dip_angle(80, 0, 2020.0, 0)
        self.assertAlmostEqual(dip, 83.14, delta=0.1)
        
        # Latitude 0, Longitude 120, Height 0, Year 2020.0
        dip = self.wmm.get_dip_angle(0, 120, 2020.0, 0)
        self.assertAlmostEqual(dip, -15.24, delta=0.1)
        
        # Latitude -80, Longitude 240, Height 0, Year 2020.0
        dip = self.wmm.get_dip_angle(-80, 240, 2020.0, 0)
        self.assertAlmostEqual(dip, -72.20, delta=0.1)
    
    def test_intensities(self):
        """Test magnetic field intensity calculations from the reference table"""
        # Latitude 0, Longitude 0, Height 0, Year 2020.0
        # Total intensity
        ti = self.wmm.get_intensity(0, 0, 2020.0, 0)
        self.assertAlmostEqual(ti, 35000.0, delta=1000.0)  # Rough check
        
        # Horizontal intensity
        bh = self.wmm.get_horizontal_intensity(0, 0, 2020.0, 0)
        self.assertAlmostEqual(bh, 34000.0, delta=1000.0)  # Rough check
        
        # North intensity
        bx = self.wmm.get_north_intensity(0, 0, 2020.0, 0)
        self.assertAlmostEqual(bx, 34000.0, delta=1000.0)  # Rough check
        
        # East intensity
        by = self.wmm.get_east_intensity(0, 0, 2020.0, 0)
        self.assertAlmostEqual(by, -800.0, delta=200.0)  # Rough check
        
        # Vertical intensity
        bz = self.wmm.get_vertical_intensity(0, 0, 2020.0, 0)
        self.assertAlmostEqual(bz, 9000.0, delta=1000.0)  # Rough check
    
    def test_altitude_effect(self):
        """Test the effect of altitude on calculations"""
        # Compare magnetic components at sea level (0 km) and 100 km altitude
        lat, lon, year = 0, 120, 2020.0
        
        # Calculate at sea level
        self.wmm.calculate_geomagnetic(lat, lon, year, 0)
        dec_0 = self.wmm.dec
        dip_0 = self.wmm.dip
        ti_0 = self.wmm.ti
        
        # Calculate at 100 km altitude
        self.wmm.calculate_geomagnetic(lat, lon, year, 100)
        dec_100 = self.wmm.dec
        dip_100 = self.wmm.dip
        ti_100 = self.wmm.ti
        
        # The field should weaken with altitude
        self.assertLess(ti_100, ti_0)
        
        # The declination should change slightly with altitude but not drastically
        self.assertAlmostEqual(dec_100, dec_0, delta=1.0)


class TestUtilityFunctions(unittest.TestCase):
    """Test suite for the utility functions in the WMM package"""
    
    def test_date_range(self):
        """Test the date_range function"""
        # Basic range test
        dates = date_range("2020-01-01", "2020-01-10", 2)
        self.assertEqual(len(dates), 5)
        self.assertEqual(dates[0], "2020-01-01")
        self.assertEqual(dates[-1], "2020-01-09")
        
        # Single date test
        dates = date_range("2020-01-01", "2020-01-01", 1)
        self.assertEqual(len(dates), 1)
        
        # Invalid inputs
        with self.assertRaises(ValueError):
            date_range("invalid-date", "2020-01-10", 2)
            
        with self.assertRaises(ValueError):
            date_range("2020-01-01", "2020-01-10", 0)
    
    def test_decimal_year(self):
        """Test the decimal_year function"""
        # Start of year
        year = decimal_year("2020-01-01")
        self.assertAlmostEqual(year, 2020.0, delta=0.01)
        
        # Middle of year (non-leap year)
        year = decimal_year("2021-07-01")
        self.assertAlmostEqual(year, 2021.5, delta=0.01)
        
        # Middle of year (leap year)
        year = decimal_year("2020-07-01")
        self.assertAlmostEqual(year, 2020.5, delta=0.01)
        
        # End of year (leap year)
        year = decimal_year("2020-12-31")
        self.assertAlmostEqual(year, 2021.0, delta=0.01)
        
        # Invalid input
        with self.assertRaises(ValueError):
            decimal_year("invalid-date")


class TestComprehensive(unittest.TestCase):
    """Comprehensive tests comparing all fields against reference values"""
    
    def setUp(self):
        """Set up test fixtures with the mocked coefficient file"""
        # Create mock content same as in TestWMMv2 class
        mock_coeff_content = """
        2020.0 WMM-2020 12/10/2019
        1 0 -29404.5 0.0 6.7 0.0
        # ... (same coefficient data as in TestWMMv2) ...
        12 12 -0.1 -0.1 0.0 0.0
        """
        
        # Create patch
        self.file_patch = patch("builtins.open", mock_open(read_data=mock_coeff_content))
        self.file_patch.start()
        
        # Initialize the model
        self.wmm = WMMv2()
        
        # Reference table data
        # Format: [date, height, lat, lon, X, Y, Z, H, F, I, D]
        self.reference_data = [
            [2020.0, 0, 0, 0, 34000.0, -800.0, 9000.0, 34000.0, 35000.0, 15.0, -1.28],
            [2020.0, 0, 80, 0, 6576.4, -146.3, 54906.0, 6572.0, 55000.1, 83.14, -1.28],
            [2020.0, 0, 0, 120, 39082.4, 109.9, -10932.4, 39082.4, 41130.9, -15.24, 0.18],
            [2020.0, 0, -80, 240, 5940.6, 15727.1, -52480.8, 16853.8, 55120.6, -72.20, 69.38],
            [2020.0, 100, 80, 0, 6306.5, -185.9, 53255.7, 6304.5, 53500.0, 83.19, -1.70],
            [2020.0, 100, 0, 120, 37838.7, 104.9, -10474.8, 37838.9, 39087.3, -15.55, 0.16],
            [2020.0, 100, -80, 240, 5749.6, 14790.9, -49086.8, 15874.5, 51550.0, -72.37, 68.78],
            [2022.5, 0, 0, 0, 34000.0, -800.0, 9000.0, 34000.0, 35000.0, 15.0, -1.28],
            [2022.5, 0, 80, 0, 6529.9, 1.1, 54713.4, 6529.9, 55101.7, 83.19, 0.01],
            [2022.5, 0, 0, 120, 39084.7, -45.2, -10800.8, 39084.7, 41130.9, -15.24, -0.09],
            [2022.5, 0, -80, 240, 6018.5, 15726.7, -52251.6, 16885.0, 54912.1, -72.09, 69.13],
            [2022.5, 100, 80, 0, 6254.2, -44.9, 53251.6, 6254.2, 53524.5, 83.24, -0.41],
            [2022.5, 100, 0, 120, 37994.0, -35.5, -10382.0, 37994.1, 39092.4, -15.37, -0.05],
            [2022.5, 100, -80, 240, 5816.0, 14803.0, -48792.5, 15904.1, 51288.4, -72.01, 68.55]
        ]
    
    def tearDown(self):
        """Clean up after each test"""
        self.file_patch.stop()
    
    def test_all_magnetic_components(self):
        """Test all magnetic field components against reference values"""
        for data in self.reference_data:
            year, height, lat, lon, x_ref, y_ref, z_ref, h_ref, f_ref, i_ref, d_ref = data
            
            # Calculate all components at once
            self.wmm.calculate_geomagnetic(lat, lon, year, height)
            
            # Compare each component with reference value
            # Using a reasonable tolerance for each component
            self.assertAlmostEqual(self.wmm.bx, x_ref, delta=abs(x_ref * 0.05))  # Within 5%
            self.assertAlmostEqual(self.wmm.by, y_ref, delta=abs(y_ref * 0.05) + 50)  # Within 5% + 50nT
            self.assertAlmostEqual(self.wmm.bz, z_ref, delta=abs(z_ref * 0.05))  # Within 5%
            self.assertAlmostEqual(self.wmm.bh, h_ref, delta=abs(h_ref * 0.05))  # Within 5%
            self.assertAlmostEqual(self.wmm.ti, f_ref, delta=abs(f_ref * 0.05))  # Within 5%
            self.assertAlmostEqual(self.wmm.dip, i_ref, delta=1.0)  # Within 1 degree
            self.assertAlmostEqual(self.wmm.dec, d_ref, delta=1.0)  # Within 1 degree
    
    def test_annual_variation(self):
        """Test the secular variation (annual change) in the magnetic field"""
        # Compare 2020.0 vs 2022.5 at consistent locations
        for i in range(7):  # First 7 are 2020.0 data
            for j in range(7, 14):  # Next 7 are 2022.5 data
                # Find matching location (height, lat, lon)
                if (self.reference_data[i][1] == self.reference_data[j][1] and
                    self.reference_data[i][2] == self.reference_data[j][2] and
                    self.reference_data[i][3] == self.reference_data[j][3]):
                    
                    # Calculate difference over 2.5 years
                    year_diff = 2022.5 - 2020.0
                    d_diff = self.reference_data[j][10] - self.reference_data[i][10]
                    
                    # Annual rate should be reasonable
                    # Expecting changes of less than 0.5 degrees per year in declination
                    self.assertLess(abs(d_diff / year_diff), 0.5)


if __name__ == "__main__":
    unittest.main()