import unittest
from pywmm.calculator import calculate_geomagnetic

class DummyWMM:
    """
    A minimal dummy instance to mimic the attributes required by calculate_geomagnetic.
    """
    def __init__(self):
        # Input and caching attributes.
        self.glat = None
        self.glon = None
        self.alt = None
        self.time = None
        self.epoch = 2020.0
        self.oalt = -1000.0
        self.olat = -1000.0
        self.olon = -1000.0

        # WGS-84/IAU constants.
        self.a = 6378.137
        self.b = 6356.7523142
        self.re = 6371.2
        self.a2 = self.a * self.a
        self.b2 = self.b * self.b
        self.c2 = self.a2 - self.b2
        self.a4 = self.a2 * self.a2
        self.b4 = self.b2 * self.b2
        self.c4 = self.a4 - self.b4

        # Maximum order.
        self.maxord = 12

        # Allocate arrays (13 elements for 0..12; 13x13 arrays for the others).
        self.sp = [0.0] * 13
        self.cp = [0.0] * 13
        self.snorm = [0.0] * 169  # 13x13 entries in a flattened array.
        self.dp = [[0.0 for _ in range(13)] for _ in range(13)]
        self.c = [[0.0 for _ in range(13)] for _ in range(13)]
        self.cd = [[0.0 for _ in range(13)] for _ in range(13)]
        self.tc = [[0.0 for _ in range(13)] for _ in range(13)]
        self.k = [[0.0 for _ in range(13)] for _ in range(13)]
        self.fn = [0.0] * 13
        self.fm = [0.0] * 13
        self.pp = [0.0] * 13

        # Variables used in the geodetic-to-spherical conversion.
        self.ct = 0.0
        self.st = 0.0
        self.r  = 0.0
        self.d  = 0.0
        self.ca = 0.0
        self.sa = 0.0

        # Magnetic field output values.
        self.bx = 0.0
        self.by = 0.0
        self.bz = 0.0
        self.bh = 0.0
        self.ti = 0.0
        self.dec = 0.0
        self.dip = 0.0

class TestCalculateGeomagnetic(unittest.TestCase):
    def setUp(self):
        self.dummy = DummyWMM()
    
    def test_calculate_geomagnetic_updates_instance(self):
        # Use a test location: for example, Los Angeles (approx. lat 34, lon -118), altitude=0, year=2020.
        lat = 34.0
        lon = -118.0
        year = 2020
        altitude = 0
        
        calculate_geomagnetic(self.dummy, lat, lon, year, altitude)
        
        # Check that the input values are set.
        self.assertEqual(self.dummy.glat, lat)
        self.assertEqual(self.dummy.glon, lon)
        self.assertEqual(self.dummy.alt, altitude)
        self.assertEqual(self.dummy.time, year)
        
        # Check that the caching variables are updated.
        self.assertEqual(self.dummy.oalt, altitude)
        self.assertEqual(self.dummy.olat, lat)
        self.assertEqual(self.dummy.olon, lon)
        
        # Check that magnetic field outputs are now floats.
        self.assertIsInstance(self.dummy.dec, float)
        self.assertIsInstance(self.dummy.dip, float)
        self.assertIsInstance(self.dummy.ti, float)
        self.assertIsInstance(self.dummy.bx, float)
        self.assertIsInstance(self.dummy.by, float)
        self.assertIsInstance(self.dummy.bz, float)
        self.assertIsInstance(self.dummy.bh, float)
    
    def test_consistency(self):
        # Calling the function twice with the same inputs should yield the same results.
        lat = 34.0
        lon = -118.0
        year = 2020
        altitude = 0
        
        calculate_geomagnetic(self.dummy, lat, lon, year, altitude)
        dec1 = self.dummy.dec
        dip1 = self.dummy.dip
        ti1 = self.dummy.ti
        
        # Call the function again.
        calculate_geomagnetic(self.dummy, lat, lon, year, altitude)
        self.assertAlmostEqual(dec1, self.dummy.dec, places=6)
        self.assertAlmostEqual(dip1, self.dummy.dip, places=6)
        self.assertAlmostEqual(ti1, self.dummy.ti, places=6)

if __name__ == '__main__':
    unittest.main()
