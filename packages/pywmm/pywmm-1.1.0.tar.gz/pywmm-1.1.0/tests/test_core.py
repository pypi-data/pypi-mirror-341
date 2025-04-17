import unittest
import os
import tempfile
from pywmm.core import WMMv2

class TestWMMv2(unittest.TestCase):
    def setUp(self):
        # Create a temporary dummy WMM.COF file with minimal valid content.
        # The file format is expected to have:
        # - A header line with 3 tokens (for epoch info)
        # - One or more coefficient lines with 6 tokens.
        #
        # Here, the first line sets epoch = 2025.0 and defaultDate = 2022.5,
        # and the second line provides a dummy coefficient.
        self.dummy_cof_content = (
            "2025.0 0.0 0.0\n"      # Header: sets epoch
            "1 0 1000.0 0.0 0.0 0.0\n"  # Dummy coefficient line
        )
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.dummy_cof_content)
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_get_declination(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        decl = wmm.get_declination(34.0, -118.0, 2025, 0)
        self.assertIsInstance(decl, float)
    
    def test_get_dip_angle(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        dip = wmm.get_dip_angle(34.0, -118.0, 2025, 0)
        self.assertIsInstance(dip, float)
    
    def test_get_intensity(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        intensity = wmm.get_intensity(34.0, -118.0, 2025, 0)
        self.assertIsInstance(intensity, float)
    
    def test_get_horizontal_intensity(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        h_intensity = wmm.get_horizontal_intensity(34.0, -118.0, 2025, 0)
        self.assertIsInstance(h_intensity, float)
    
    def test_get_north_intensity(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        n_intensity = wmm.get_north_intensity(34.0, -118.0, 2025, 0)
        self.assertIsInstance(n_intensity, float)
    
    def test_get_east_intensity(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        e_intensity = wmm.get_east_intensity(34.0, -118.0, 2025, 0)
        self.assertIsInstance(e_intensity, float)
    
    def test_get_vertical_intensity(self):
        wmm = WMMv2(coeff_file=self.temp_file.name)
        v_intensity = wmm.get_vertical_intensity(34.0, -118.0, 2025, 0)
        self.assertIsInstance(v_intensity, float)

if __name__ == '__main__':
    unittest.main()
