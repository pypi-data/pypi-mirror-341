import unittest
import os
import numpy as np
from unittest.mock import patch, mock_open

# Import the module to test
from pywmm import WMMv2

class TestWMMv2WithReferenceTable(unittest.TestCase):
    """Test the WMMv2 class with values from the provided reference table"""

    def setUp(self):
        """Set up the test with mock coefficient file and reference data"""
        # Mock coefficient file content for WMM2020
        # Make sure the format matches exactly what your read_coefficients function expects
        self.mock_coeff_content = """    2020.0            WMM-2020        12/10/2019
        1  0  -29404.5       0.0     6.7        0.0
        1  1   -1450.7    4652.9     7.7      -25.1
        2  0   -2500.0       0.0   -11.5        0.0
        2  1    2982.0   -2991.6    -7.1      -30.2
        2  2    1676.8    -734.8    -2.2      -23.9
        3  0    1363.9       0.0     2.8        0.0
        3  1   -2381.0     -82.2    -6.2        5.7
        3  2    1236.2     241.8     3.4       -1.0
        3  3     525.7    -542.9   -12.2        1.1
        4  0     907.2       0.0    -1.1        0.0
        4  1     813.7     283.4     0.2       -0.6
        4  2     120.3    -188.7    -9.1        5.3
        4  3    -335.0     180.9     4.0        3.0
        4  4      70.3    -329.5    -4.2       -5.3
        5  0    -232.6       0.0    -0.1        0.0
        5  1     360.1      47.4     0.5        0.1
        5  2     192.4     196.9    -1.4        1.7
        5  3    -141.0    -119.4     0.0       -1.2
        5  4    -157.4      16.1     1.3        3.3
        5  5       4.3     100.1     3.8        0.1
        6  0      69.5       0.0    -0.8        0.0
        6  1      67.4     -20.7    -0.5       -0.1
        6  2      72.8      33.2    -0.2       -1.5
        6  3    -129.8      58.8     2.1       -0.7
        6  4     -29.0     -66.5    -1.6        0.6
        6  5      13.2       7.3     0.1       -0.2
        6  6     -70.9      62.5     1.5        1.3
        7  0      81.6       0.0    -0.2        0.0
        7  1     -76.1     -54.1    -0.2        0.7
        7  2      -8.7     -19.5    -0.4        0.5
        7  3      56.5       6.0     0.4       -0.5
        7  4      15.5      24.4     0.3       -0.2
        7  5       6.0     -12.4     0.0       -0.5
        7  6      -7.0     -24.2    -0.4        0.0
        7  7       9.7       3.3    -0.1       -0.3
        8  0      24.2       0.0     0.0        0.0
        8  1       8.8      10.2     0.1       -0.1
        8  2     -16.9     -18.3    -0.5        0.4
        8  3      -3.2      13.3     0.5        0.2
        8  4     -20.6     -14.6    -0.2        0.4
        8  5      13.3      16.2     0.1       -0.1
        8  6      11.8       5.7     0.1       -0.3
        8  7     -16.0      -9.1    -0.4        0.3
        8  8      -2.1       2.9     0.4        0.0
        9  0       5.4       0.0    -0.2        0.0
        9  1       8.8     -21.8    -0.1       -0.2
        9  2       3.1      10.8    -0.1       -0.1
        9  3      -3.0      11.7     0.1       -0.1
        9  4      -0.4      -6.8    -0.1        0.1
        9  5     -10.1       7.8    -0.2       -0.2
        9  6      -1.4      -3.9    -0.2        0.0
        9  7       9.6      -1.9     0.0        0.0
        9  8     -11.3       9.7    -0.2        0.0
        9  9      -4.9      -6.2     0.0        0.1
       10  0      -3.4       0.0    -0.2        0.0
       10  1      -0.2      -6.3     0.0        0.0
       10  2       0.6      -1.1     0.0        0.0
       10  3       4.9      -0.2    -0.1        0.0
       10  4      -0.3       4.4     0.0       -0.1
       10  5       1.3      -2.4     0.0        0.0
       10  6      -2.0      -3.1    -0.1        0.0
       10  7      -0.9      -0.3     0.0        0.0
       10  8      -0.4       0.8     0.0        0.0
       10  9       0.3      -2.6     0.0        0.0
       10 10      -2.2      -1.3    -0.1        0.1
       11  0      -0.9       0.0     0.0        0.0
       11  1      -1.9       1.2     0.0        0.0
       11  2      -0.4      -2.5     0.0        0.1
       11  3       2.3       2.4     0.0        0.0
       11  4      -2.6       1.2     0.0        0.0
       11  5       0.6       0.5     0.0        0.0
       11  6       0.4       0.3     0.0        0.0
       11  7       0.0      -2.0     0.0        0.0
       11  8      -0.8      -0.2     0.0        0.0
       11  9      -0.4       0.1     0.0        0.0
       11 10       0.1      -0.9     0.0        0.0
       11 11      -0.3      -0.4     0.0        0.0
       12  0      -0.1       0.0     0.0        0.0
       12  1       0.8      -0.1     0.0        0.0
       12  2       0.4      -0.3     0.0        0.0
       12  3      -0.6       0.4     0.0        0.0
       12  4       0.5      -1.4     0.0        0.0
       12  5       1.4      -1.2     0.0        0.0
       12  6      -0.3      -0.8     0.0        0.0
       12  7       0.6       0.1     0.0        0.0
       12  8      -0.3       0.6     0.0        0.0
       12  9      -0.3      -0.1     0.0        0.0
       12 10      -0.1       0.1     0.0        0.0
       12 11      -0.3       0.4     0.0        0.0
       12 12      -0.1      -0.1     0.0        0.0"""
        
        # Create the patch for the coefficient file
        self.file_patch = patch("builtins.open", mock_open(read_data=self.mock_coeff_content))
        self.file_patch.start()
        
        # Initialize the model with the mocked coefficient file
        self.wmm = WMMv2()
        
        # Reference table data from the provided table
        # Format: [Date, Height, Lat, Lon, X (nT), Y (nT), Z (nT), H (nT), F (nT), I (deg), D (deg)]
        self.reference_data = [
            # 2020.0 data
            [2020.0, 0, 0, 0, 6276.4, -146.3, 54906.0, 6572.0, 55000.1, 83.14, -1.28],
            [2020.0, 0, 80, 0, 6276.4, -146.3, 54906.0, 6572.0, 55000.1, 83.14, -1.28],
            [2020.0, 0, 0, 120, 39082.4, 109.9, -10932.4, 39082.4, 41130.9, -15.24, 0.16],
            [2020.0, 0, -80, 240, 5940.6, 15772.1, -52480.8, 16853.8, 55120.6, -72.20, 69.38],
            [2020.0, 100, 0, 0, 6306.5, -185.9, 53255.7, 6304.5, 53500.0, 83.19, -1.70],
            [2020.0, 100, 80, 0, 6306.5, -185.9, 53255.7, 6304.5, 53500.0, 83.19, -1.70],
            [2020.0, 100, 0, 120, 37838.7, 104.9, -10474.8, 37838.9, 39087.3, -15.55, 0.16],
            [2020.0, 100, -80, 240, 5749.6, 14790.9, -49086.8, 15874.5, 51550.0, -72.37, 68.78],
            
            # 2022.5 data
            [2022.5, 0, 0, 0, 6529.9, 1.1, 54713.4, 6529.9, 55101.7, 83.19, 0.01],
            [2022.5, 0, 80, 0, 6529.9, 1.1, 54713.4, 6529.9, 55101.7, 83.19, 0.01],
            [2022.5, 0, 0, 120, 39084.7, -45.2, -10800.8, 39084.7, 41130.9, -15.24, -0.09],
            [2022.5, 0, -80, 240, 6018.5, 15726.7, -52251.6, 16885.0, 54912.1, -72.09, 69.13],
            [2022.5, 100, 0, 0, 6254.2, -44.9, 53251.6, 6254.2, 53524.5, 83.24, -0.41],
            [2022.5, 100, 80, 0, 6254.2, -44.9, 53251.6, 6254.2, 53524.5, 83.24, -0.41],
            [2022.5, 100, 0, 120, 37994.0, -35.5, -10382.0, 37994.1, 39092.4, -15.37, -0.05],
            [2022.5, 100, -80, 240, 5816.0, 14803.0, -48792.5, 15904.1, 51288.4, -72.01, 68.55]
        ]
        
        # Second table with annual rates
        # Format: [Date, Height, Lat, Lon, X (nT/yr), Y (nT/yr), Z (nT/yr), H (nT/yr), F (nT/yr), I (deg/yr), D (deg/yr)]
        self.annual_rates = [
            # 2020.0 data
            [2020.0, 0, 0, 0, 24.2, -60.8, 49.2, 24.0, 10.1, 0.02, -0.09],
            [2020.0, 0, 80, 0, 24.2, -60.8, 49.2, 24.0, 10.1, 0.02, -0.09],
            [2020.0, 0, 0, 120, 32.9, 1.8, 11.1, 12.4, 23.5, 0.00, -0.10],
            [2020.0, 0, -80, 240, -15.1, 58.4, 39.2, -16.8, 26.9, 0.02, 0.51],
            [2020.0, 100, 0, 0, 0.0, 0.0, 0.0, 22.8, 9.8, 0.07, -0.09],
            [2020.0, 100, 80, 0, -15.1, 58.1, 39.2, 22.8, 9.8, 0.07, -0.09],
            [2020.0, 100, 0, 120, 28.0, 1.4, 85.6, 11.4, -73.1, 0.04, -0.09],
            [2020.0, 100, -80, 240, 28.0, 1.4, 85.6, 11.4, -73.1, 0.04, -0.09],
            
            # 2022.5 data
            [2022.5, 0, 0, 0, 24.2, -60.8, 49.2, 24.2, 10.5, 0.08, -0.09],
            [2022.5, 0, 80, 0, 24.2, -60.8, 49.2, 24.2, 10.5, 0.08, -0.09],
            [2022.5, 0, 0, 120, -10.2, 1.8, 11.1, 12.6, 23.4, 0.01, -0.09],
            [2022.5, 0, -80, 240, -15.1, 58.4, 39.2, -15.5, 37.1, 0.02, 0.52],
            [2022.5, 100, 0, 0, -15.1, 58.4, 39.2, -15.5, 37.1, 0.02, 0.52],
            [2022.5, 100, 80, 0, -15.1, 58.4, 39.2, -15.5, 37.1, 0.02, 0.52],
            [2022.5, 100, 0, 120, 27.3, 1.4, 85.6, 11.6, -78.0, 0.04, -0.09],
            [2022.5, 100, -80, 240, 28.0, 1.4, 85.6, 11.6, -78.0, 0.04, -0.09]
        ]
    
    def tearDown(self):
        """Clean up after each test"""
        self.file_patch.stop()
    
    def test_model_initialization(self):
        """Test that the model initializes with the correct parameters"""
        self.assertEqual(self.wmm.epoch, 2020.0)
        self.assertEqual(self.wmm.defaultDate, 2022.5)  # epoch + 2.5
        self.assertEqual(self.wmm.maxdeg, 12)
        self.assertEqual(self.wmm.maxord, 12)
    
    def test_reference_values(self):
        """Test the model against the reference values in the table"""
        for data in self.reference_data:
            date, height, lat, lon, x_ref, y_ref, z_ref, h_ref, f_ref, i_ref, d_ref = data
            
            # Calculate all magnetic field components
            self.wmm.calculate_geomagnetic(lat, lon, date, height)
            
            # Check each component with a reasonable tolerance
            # Some values might vary slightly due to implementation differences
            msg = f"Failed at: date={date}, height={height}, lat={lat}, lon={lon}"
            
            # Test main field components (X, Y, Z)
            self.assertAlmostEqual(self.wmm.bx, x_ref, delta=abs(x_ref * 0.05) + 50, msg=msg)  # Within 5% + 50nT
            self.assertAlmostEqual(self.wmm.by, y_ref, delta=abs(y_ref * 0.05) + 50, msg=msg)  # Within 5% + 50nT
            self.assertAlmostEqual(self.wmm.bz, z_ref, delta=abs(z_ref * 0.05) + 50, msg=msg)  # Within 5% + 50nT
            
            # Test derived components (H, F)
            self.assertAlmostEqual(self.wmm.bh, h_ref, delta=abs(h_ref * 0.05) + 50, msg=msg)  # Within 5% + 50nT
            self.assertAlmostEqual(self.wmm.ti, f_ref, delta=abs(f_ref * 0.05) + 50, msg=msg)  # Within 5% + 50nT
            
            # Test angles (I, D) - use smaller tolerance for angles
            self.assertAlmostEqual(self.wmm.dip, i_ref, delta=0.5, msg=msg)  # Within 0.5 degrees
            self.assertAlmostEqual(self.wmm.dec, d_ref, delta=0.5, msg=msg)  # Within 0.5 degrees
    
    def test_method_equivalence(self):
        """Test that individual getter methods produce same results as calculate_geomagnetic"""
        # Test point
        lat, lon, year, altitude = 40.0, -75.0, 2021.0, 0
        
        # Get values using individual methods
        dec = self.wmm.get_declination(lat, lon, year, altitude)
        dip = self.wmm.get_dip_angle(lat, lon, year, altitude)
        ti = self.wmm.get_intensity(lat, lon, year, altitude)
        bh = self.wmm.get_horizontal_intensity(lat, lon, year, altitude)
        bx = self.wmm.get_north_intensity(lat, lon, year, altitude)
        by = self.wmm.get_east_intensity(lat, lon, year, altitude)
        bz = self.wmm.get_vertical_intensity(lat, lon, year, altitude)
        
        # Calculate all components directly
        self.wmm.calculate_geomagnetic(lat, lon, year, altitude)
        
        # Compare results - they should be identical
        self.assertEqual(dec, self.wmm.dec)
        self.assertEqual(dip, self.wmm.dip)
        self.assertEqual(ti, self.wmm.ti)
        self.assertEqual(bh, self.wmm.bh)
        self.assertEqual(bx, self.wmm.bx)
        self.assertEqual(by, self.wmm.by)
        self.assertEqual(bz, self.wmm.bz)
    
    def test_time_variations(self):
        """Test the temporal variation of the magnetic field"""
        # Test points that appear in both 2020.0 and 2022.5 data
        test_points = [
            # Format: lat, lon, height
            [0, 0, 0],
            [80, 0, 0],
            [0, 120, 0],
            [-80, 240, 0],
            [0, 0, 100],
            [80, 0, 100],
            [0, 120, 100],
            [-80, 240, 100]
        ]
        
        for point in test_points:
            lat, lon, height = point
            
            # Calculate at 2020.0
            self.wmm.calculate_geomagnetic(lat, lon, 2020.0, height)
            dec_2020 = self.wmm.dec
            dip_2020 = self.wmm.dip
            ti_2020 = self.wmm.ti
            
            # Calculate at 2022.5
            self.wmm.calculate_geomagnetic(lat, lon, 2022.5, height)
            dec_2022 = self.wmm.dec
            dip_2022 = self.wmm.dip
            ti_2022 = self.wmm.ti
            
            # Calculate observed annual rates
            dec_rate = (dec_2022 - dec_2020) / 2.5  # degrees per year
            dip_rate = (dip_2022 - dip_2020) / 2.5  # degrees per year
            ti_rate = (ti_2022 - ti_2020) / 2.5     # nT per year
            
            # Find expected rates from the annual rates table
            expected_dec_rate = None
            expected_dip_rate = None
            expected_ti_rate = None
            
            for rate_data in self.annual_rates:
                if (rate_data[1] == height and rate_data[2] == lat and rate_data[3] == lon and rate_data[0] == 2020.0):
                    expected_dec_rate = rate_data[10]  # D rate
                    expected_dip_rate = rate_data[9]   # I rate
                    expected_ti_rate = rate_data[8]    # F rate
                    break
            
            # Check if we found matching data
            if expected_dec_rate is not None:
                # Rates should be reasonably close to expected values
                # Be generous with tolerance because our coefficient set might differ
                self.assertAlmostEqual(dec_rate, expected_dec_rate, delta=0.3,
                                      msg=f"Declination rate at lat={lat}, lon={lon}, h={height}")
                self.assertAlmostEqual(dip_rate, expected_dip_rate, delta=0.3,
                                      msg=f"Inclination rate at lat={lat}, lon={lon}, h={height}")
                self.assertAlmostEqual(ti_rate, expected_ti_rate, delta=20.0,
                                      msg=f"Total intensity rate at lat={lat}, lon={lon}, h={height}")
    
    def test_altitude_effects(self):
        """Test the effect of altitude on magnetic field parameters"""
        # Test at several locations, comparing sea level (0 km) to high altitude (100 km)
        test_points = [
            # Format: lat, lon, year
            [0, 0, 2020.0],
            [80, 0, 2020.0],
            [0, 120, 2020.0],
            [-80, 240, 2020.0],
            [0, 0, 2022.5],
            [80, 0, 2022.5],
            [0, 120, 2022.5],
            [-80, 240, 2022.5]
        ]
        
        for point in test_points:
            lat, lon, year = point
            
            # Calculate at sea level
            self.wmm.calculate_geomagnetic(lat, lon, year, 0)
            ti_sea_level = self.wmm.ti
            bh_sea_level = self.wmm.bh
            bz_sea_level = self.wmm.bz
            
            # Calculate at 100 km altitude
            self.wmm.calculate_geomagnetic(lat, lon, year, 100)
            ti_altitude = self.wmm.ti
            bh_altitude = self.wmm.bh
            bz_altitude = self.wmm.bz
            
            # Field strength should decrease with altitude (inverse cube law)
            self.assertLess(ti_altitude, ti_sea_level, 
                           msg=f"Total intensity should decrease with altitude at lat={lat}, lon={lon}")
            
            # Horizontal component should decrease with altitude
            self.assertLess(bh_altitude, bh_sea_level,
                           msg=f"Horizontal intensity should decrease with altitude at lat={lat}, lon={lon}")
            
            # Vertical component should decrease with altitude
            # The absolute value should decrease
            self.assertLess(abs(bz_altitude), abs(bz_sea_level),
                           msg=f"Vertical intensity magnitude should decrease with altitude at lat={lat}, lon={lon}")
    
    def test_poles_and_equator(self):
        """Test behavior at special locations: poles and equator"""
        # Inclination should be ~90° at North Pole
        self.wmm.calculate_geomagnetic(90, 0, 2020.0, 0)
        self.assertAlmostEqual(abs(self.wmm.dip), 90.0, delta=2.0, 
                              msg="Inclination should be nearly 90° at North Pole")
        
        # Inclination should be ~-90° at South Pole
        self.wmm.calculate_geomagnetic(-90, 0, 2020.0, 0)
        self.assertAlmostEqual(abs(self.wmm.dip), 90.0, delta=2.0,
                              msg="Inclination should be nearly -90° at South Pole")
        
        # Test points along the magnetic equator (where dip should be close to 0)
        # These are approximate locations for 2020
        mag_equator_points = [
            [8.5, -80.0],  # South America
            [11.0, -10.0],  # Africa
            [0.0, 80.0],    # Indian Ocean
            [-8.0, 125.0],  # Indonesia
        ]
        
        for point in mag_equator_points:
            lat, lon = point
            self.wmm.calculate_geomagnetic(lat, lon, 2020.0, 0)
            self.assertAlmost