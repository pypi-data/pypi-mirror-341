import math
import numpy as np
from .coefficients import read_coefficients, read_coefficients_from_bytes
from .calculator import calculate_geomagnetic

class WMMv2:
    """
    World Magnetic Model (WMM) version 2 implementation.
    
    This class implements the World Magnetic Model which provides magnetic field parameters
    (declination, inclination, intensity) at given coordinates and time. The WMM is the standard
    model used by the U.S. Department of Defense, the U.K. Ministry of Defence, NATO, and the
    International Hydrographic Organization.
    
    Attributes:
        maxdeg (int): Maximum degree of spherical harmonic model.
        maxord (int): Maximum order of spherical harmonic model.
        defaultDate (float): Default decimal year to use if none specified.
        dec (float): Declination in degrees (positive east).
        dip (float): Dip/inclination angle in degrees (positive down).
        ti (float): Total intensity of the magnetic field in nT.
        bx (float): North component of the magnetic field in nT.
        by (float): East component of the magnetic field in nT.
        bz (float): Vertical/downward component of the magnetic field in nT.
        bh (float): Horizontal intensity of the magnetic field in nT.
    """

    def __init__(self, coeff_file=None, coeff_data=None):
        """
        Initialize the WMMv2 model.
        
        Parameters:
            coeff_file (str, optional): Path to custom coefficients file. If None, default 
                                        coefficients will be used.
            coeff_data (bytes, optional): Coefficient data as bytes. If provided, this will
                                          be used instead of loading from a file.
        """
        # Allow the user to pass a custom coefficients file path or byte data
        self.coeff_file = coeff_file
        self.coeff_data = coeff_data

        self.maxdeg = 12
        self.maxord = self.maxdeg
        self.defaultDate = 2025.0

        # Magnetic field outputs (nT and degrees)
        self.dec = 0.0   # declination
        self.dip = 0.0   # dip angle
        self.ti = 0.0    # total intensity
        self.bx = 0.0    # north intensity
        self.by = 0.0    # east intensity
        self.bz = 0.0    # vertical intensity
        self.bh = 0.0    # horizontal intensity

        # Epoch and caching variables (for geodetic conversion)
        self.epoch = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

        # WGS-84/IAU constants
        self.a = 6378.137           # semi-major axis (km) of WGS-84 ellipsoid
        self.b = 6356.7523142       # semi-minor axis (km) of WGS-84 ellipsoid
        self.re = 6371.2            # Earth's mean radius (km)
        self.a2 = self.a * self.a   # a squared
        self.b2 = self.b * self.b   # b squared
        self.c2 = self.a2 - self.b2 # c squared (c is linear eccentricity)
        self.a4 = self.a2 * self.a2 # a to the fourth power
        self.b4 = self.b2 * self.b2 # b to the fourth power
        self.c4 = self.a4 - self.b4 # c to the fourth power

        # Allocate arrays for spherical harmonic coefficients and calculations
        self.c    = [[0.0 for _ in range(13)] for _ in range(13)]  # Main field coefficients
        self.cd   = [[0.0 for _ in range(13)] for _ in range(13)]  # Secular variation coefficients
        self.tc   = [[0.0 for _ in range(13)] for _ in range(13)]  # Time-adjusted coefficients
        self.dp   = [[0.0 for _ in range(13)] for _ in range(13)]  # Legendre derivative function
        self.snorm = np.zeros(169)  # Schmidt normalization factors (13x13 = 169 entries)
        self.sp   = np.zeros(13)    # sin(m*phi) (longitude)
        self.cp   = np.zeros(13)    # cos(m*phi) (longitude)
        self.fn   = np.zeros(13)    # n+1 factors
        self.fm   = np.zeros(13)    # m factors
        self.pp   = np.zeros(13)    # Associated Legendre polynomial values
        self.k    = [[0.0 for _ in range(13)] for _ in range(13)]  # Recursion coefficients

        # Variables for geodetic-to-spherical conversion
        self.ct = 0.0  # cos(theta)
        self.st = 0.0  # sin(theta)
        self.r  = 0.0  # distance from center of Earth
        self.d  = 0.0  # down component
        self.ca = 0.0  # cos(alpha)
        self.sa = 0.0  # sin(alpha)

        self.start()

    def read_coefficients(self):
        """
        Read spherical harmonic coefficients from the coefficient file or data.
        
        This method uses the external functions from the coefficients module,
        passing the current instance so the function can modify the object's properties.
        """
        if self.coeff_data is not None:
            # If coefficient data was provided as bytes, use that
            read_coefficients_from_bytes(self, self.coeff_data)
        else:
            # Otherwise read from file
            read_coefficients(self)

    def start(self):
        """
        Initialize the model by setting up normalization factors and processing coefficients.
        
        This method:
        1. Reads the spherical harmonic coefficients
        2. Calculates Schmidt normalization factors
        3. Performs normalization on the coefficients
        4. Initializes recursion coefficients for Legendre functions
        """
        self.maxord = self.maxdeg
        self.sp[0] = 0.0
        self.cp[0] = self.snorm[0] = self.pp[0] = 1.0
        self.dp[0][0] = 0.0

        # Read coefficients (this will use self.coeff_file if it was provided)
        self.read_coefficients()

        # Schmidt normalization factors
        self.snorm[0] = 1.0
        n = 1
        while n <= self.maxord:
            self.snorm[n] = self.snorm[n - 1] * (2 * n - 1) / n
            j = 2
            m = 0
            D1 = 1
            D2 = (n - m + D1) / D1
            while D2 > 0:
                self.k[m][n] = float(((n - 1)**2 - m**2)) / float((2 * n - 1) * (2 * n - 3))
                if m > 0:
                    flnmj = ((n - m + 1) * j) / float(n + m)
                    self.snorm[n + m * 13] = self.snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                    j = 1
                    self.c[n][m - 1] = self.snorm[n + m * 13] * self.c[n][m - 1]
                    self.cd[n][m - 1] = self.snorm[n + m * 13] * self.cd[n][m - 1]
                self.c[m][n] = self.snorm[n + m * 13] * self.c[m][n]
                self.cd[m][n] = self.snorm[n + m * 13] * self.cd[m][n]
                D2 = D2 - 1
                m = m + D1
            self.fn[n] = n + 1
            self.fm[n] = n
            n = n + 1
        self.k[1][1] = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

    def update_coefficients(self, new_coeff_file=None, new_coeff_data=None):
        """
        Update the model with new coefficient data.
        
        This method allows updating the model's coefficients without reinitializing
        the entire object.
        
        Parameters:
            new_coeff_file (str, optional): Path to new coefficient file
            new_coeff_data (bytes, optional): New coefficient data as bytes
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        # Store original values in case update fails
        original_file = self.coeff_file
        original_data = self.coeff_data
        
        try:
            # Update with new values
            if new_coeff_file is not None:
                self.coeff_file = new_coeff_file
                self.coeff_data = None
            elif new_coeff_data is not None:
                self.coeff_data = new_coeff_data
                self.coeff_file = None
            else:
                return False  # No new data provided
            
            # Reinitialize the model with new coefficients
            self.read_coefficients()
            
            # Reset cache values to force recalculation
            self.otime = self.oalt = self.olat = self.olon = -1000.0
            
            return True
            
        except Exception as e:
            # Restore original values if update fails
            self.coeff_file = original_file
            self.coeff_data = original_data
            print(f"Failed to update coefficients: {str(e)}")
            return False

    def get_declination(self, dLat, dLong, year, altitude):
        """
        Calculate magnetic declination at the given location and time.
        
        Declination is the angle between true north and magnetic north,
        positive when magnetic north is east of true north.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Magnetic declination in degrees (positive east).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.dec

    def get_dip_angle(self, dLat, dLong, year, altitude):
        """
        Calculate magnetic dip angle (inclination) at the given location and time.
        
        Dip angle is the angle between the horizontal plane and the magnetic field vector,
        positive when the magnetic field points downward.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Magnetic dip angle in degrees (positive downward).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.dip

    def get_intensity(self, dLat, dLong, year, altitude):
        """
        Calculate total magnetic field intensity at the given location and time.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Total magnetic field intensity in nanoteslas (nT).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.ti

    def get_horizontal_intensity(self, dLat, dLong, year, altitude):
        """
        Calculate horizontal magnetic field intensity at the given location and time.
        
        The horizontal intensity is the magnitude of the horizontal components (north and east).
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Horizontal magnetic field intensity in nanoteslas (nT).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bh

    def get_north_intensity(self, dLat, dLong, year, altitude):
        """
        Calculate northward component of the magnetic field at the given location and time.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Northward magnetic field component in nanoteslas (nT).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bx

    def get_east_intensity(self, dLat, dLong, year, altitude):
        """
        Calculate eastward component of the magnetic field at the given location and time.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Eastward magnetic field component in nanoteslas (nT).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.by

    def get_vertical_intensity(self, dLat, dLong, year, altitude):
        """
        Calculate vertical (downward) component of the magnetic field at the given location and time.
        
        Parameters:
            dLat (float): Latitude in decimal degrees.
            dLong (float): Longitude in decimal degrees.
            year (float): Decimal year (e.g., 2025.5 for July 1, 2025).
            altitude (float): Altitude above WGS-84 ellipsoid in kilometers.
            
        Returns:
            float: Downward magnetic field component in nanoteslas (nT).
        """
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bz

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create a WMMv2 instance from byte data.
        
        This is a convenience method for initializing a model directly from coefficient data
        received via HTTP requests or other byte streams.
        
        Parameters:
            byte_data (bytes): Coefficient data as bytes
            
        Returns:
            WMMv2: Initialized WMMv2 instance
        """
        return cls(coeff_data=byte_data)