import math

def calculate_geomagnetic(instance, fLat, fLon, year, altitude=0):
    """
    Calculate geomagnetic field components at a specified location and time.
    
    This function implements the spherical harmonic synthesis algorithm for the World 
    Magnetic Model (WMM). It computes the magnetic field vector components and derived
    quantities at the specified geodetic coordinates and time, storing results in the 
    given instance.
    
    Parameters:
        instance: A WMMv2 model instance with the following required attributes:
            - Arrays: c, cd, tc, snorm, sp, cp, dp, k, fn, fm, pp (see WMMv2 class)
            - Model parameters: epoch, maxord, re, a, b, a2, b2, c2, a4, b4, c4
            - Caching variables: otime, oalt, olat, olon
            - Output fields: bx, by, bz, bh, ti, dec, dip
        
        fLat (float): Geodetic latitude in decimal degrees (-90 to 90)
        fLon (float): Geodetic longitude in decimal degrees (-180 to 180)
        year (float): Decimal year (e.g., 2025.5 for July 1, 2025)
        altitude (float, optional): Altitude above WGS-84 ellipsoid in kilometers. 
                                    Default is 0 (sea level).
    
    Returns:
        None: Results are stored in the instance attributes:
            - bx: Northward component (nT)
            - by: Eastward component (nT)
            - bz: Downward component (nT)
            - bh: Horizontal intensity (nT)
            - ti: Total intensity (nT)
            - dec: Declination (degrees, positive east)
            - dip: Inclination (degrees, positive down)
    
    Algorithm notes:
        1. Converts geodetic coordinates to spherical coordinates
        2. Computes time-adjusted Gauss coefficients
        3. Calculates associated Legendre functions
        4. Synthesizes magnetic field components in spherical coordinates
        5. Converts to geodetic components (north, east, down)
        6. Derives derived quantities (declination, inclination, intensities)
        
    The function uses caching to avoid redundant calculations when called repeatedly
    with the same latitude, longitude, or altitude.
    """
    instance.glat = fLat
    instance.glon = fLon
    instance.alt = altitude
    instance.time = year

    dt = instance.time - instance.epoch  # Time difference from epoch in years
    pi = math.pi
    dtr = pi / 180.0  # Degrees to radians conversion factor
    rlon = instance.glon * dtr  # Longitude in radians
    rlat = instance.glat * dtr  # Latitude in radians
    srlon = math.sin(rlon)
    srlat = math.sin(rlat)
    crlon = math.cos(rlon)
    crlat = math.cos(rlat)
    srlat2 = srlat * srlat
    crlat2 = crlat * crlat

    # Initialize sine and cosine of longitude for recursion
    instance.sp[1] = srlon
    instance.cp[1] = crlon

    # Geodetic to spherical coordinate transformation
    # Recalculate only if latitude or altitude has changed
    if altitude != instance.oalt or fLat != instance.olat:
        # Calculate geocentric coordinates from geodetic
        q = math.sqrt(instance.a2 - instance.c2 * srlat2)  # Distance from rotation axis
        q1 = altitude * q
        q2 = ((q1 + instance.a2) / (q1 + instance.b2)) ** 2
        ct = srlat / math.sqrt(q2 * crlat2 + srlat2)  # cos(theta) - theta is geocentric colatitude
        st = math.sqrt(1.0 - ct * ct)                 # sin(theta)
        r2 = altitude * altitude + 2.0 * q1 + (instance.a4 - instance.c4 * srlat2) / (q * q)
        r = math.sqrt(r2)  # Geocentric radius
        d = math.sqrt(instance.a2 * crlat2 + instance.b2 * srlat2)  # Distance from rotation axis
        ca = (altitude + d) / r  # cos(alpha) - alpha is angle between radial vector and horizontal
        sa = instance.c2 * crlat * srlat / (r * d)    # sin(alpha)
        
        # Cache the calculated values
        instance.ct = ct
        instance.st = st
        instance.r  = r
        instance.d  = d
        instance.ca = ca
        instance.sa = sa
    else:
        # Use cached values
        ct = instance.ct
        st = instance.st
        r  = instance.r
        d  = instance.d
        ca = instance.ca
        sa = instance.sa

    # Compute recursion of sin(m*lon) and cos(m*lon)
    # Recalculate only if longitude has changed
    if fLon != instance.olon:
        m = 2
        while m <= instance.maxord:
            instance.sp[m] = instance.sp[1] * instance.cp[m - 1] + instance.cp[1] * instance.sp[m - 1]
            instance.cp[m] = instance.cp[1] * instance.cp[m - 1] - instance.sp[1] * instance.sp[m - 1]
            m += 1

    # Powers of (earth_radius/geocentric_radius)
    aor = instance.re / r  # Ratio of reference sphere radius to geocentric radius
    ar = aor * aor        # Initial value for recursion
    
    # Initialize magnetic field components
    br = 0.0  # Radial component
    bt = 0.0  # Theta (colatitude) component
    bp = 0.0  # Phi (longitude) component
    bpp = 0.0  # Special case for poles

    # Main spherical harmonic synthesis loop
    n = 1
    while n <= instance.maxord:
        ar = ar * aor  # (earth_radius/geocentric_radius)^(n+2)
        m = 0
        D1 = 1
        D2 = (n + m + D1) / D1
        while D2 > 0:
            # Compute Schmidt quasi-normalized associated Legendre functions
            # and their theta derivatives
            if altitude != instance.oalt or fLat != instance.olat:
                if n == m:
                    instance.snorm[n + m * 13] = st * instance.snorm[n - 1 + (m - 1) * 13]
                    instance.dp[m][n] = st * instance.dp[m - 1][n - 1] + ct * instance.snorm[n - 1 + (m - 1) * 13]
                if n == 1 and m == 0:
                    instance.snorm[n + m * 13] = ct * instance.snorm[n - 1 + m * 13]
                    instance.dp[m][n] = ct * instance.dp[m][n - 1] - st * instance.snorm[n - 1 + m * 13]
                if n > 1 and n != m:
                    if m > n - 2:
                        instance.snorm[n - 2 + m * 13] = 0.0
                        instance.dp[m][n - 2] = 0.0
                    instance.snorm[n + m * 13] = ct * instance.snorm[n - 1 + m * 13] - instance.k[m][n] * instance.snorm[n - 2 + m * 13]
                    instance.dp[m][n] = ct * instance.dp[m][n - 1] - st * instance.snorm[n - 1 + m * 13] - instance.k[m][n] * instance.dp[m][n - 2]
            
            # Time-adjusted Gauss coefficients
            instance.tc[m][n] = instance.c[m][n] + dt * instance.cd[m][n]
            if m != 0:
                instance.tc[n][m - 1] = instance.c[n][m - 1] + dt * instance.cd[n][m - 1]
            
            # Spherical harmonic terms
            par = ar * instance.snorm[n + m * 13]
            if m == 0:
                temp1 = instance.tc[m][n] * instance.cp[m]
                temp2 = instance.tc[m][n] * instance.sp[m]
            else:
                temp1 = instance.tc[m][n] * instance.cp[m] + instance.tc[n][m - 1] * instance.sp[m]
                temp2 = instance.tc[m][n] * instance.sp[m] - instance.tc[n][m - 1] * instance.cp[m]
            
            # Accumulate field components in spherical coordinates
            bt = bt - ar * temp1 * instance.dp[m][n]     # theta component
            bp = bp + instance.fm[m] * temp2 * par       # phi component
            br = br + instance.fn[n] * temp1 * par       # radial component
            
            # Special case for poles (where latitude = +/- 90 degrees)
            if st == 0.0 and m == 1:
                if n == 1:
                    instance.pp[n] = instance.pp[n - 1]
                else:
                    instance.pp[n] = ct * instance.pp[n - 1] - instance.k[m][n] * instance.pp[n - 2]
                parp = ar * instance.pp[n]
                bpp = bpp + instance.fm[m] * temp2 * parp
            
            D2 -= 1
            m += 1
        n += 1

    # Handle special case for poles
    if st == 0.0:
        bp = bpp
    else:
        bp = bp / st  # Adjust phi component

    # Convert from spherical to geodetic components
    instance.bx = -bt * ca - br * sa  # North component
    instance.by = bp                  # East component
    instance.bz = bt * sa - br * ca   # Down component

    # Calculate derived quantities
    instance.bh = math.sqrt(instance.bx * instance.bx + instance.by * instance.by)  # Horizontal intensity
    instance.ti = math.sqrt(instance.bh * instance.bh + instance.bz * instance.bz)  # Total intensity

    # Calculate declination and inclination (dip) angles
    instance.dec = math.atan2(instance.by, instance.bx) / dtr  # Declination in degrees
    instance.dip = math.atan2(instance.bz, instance.bh) / dtr  # Inclination in degrees

    # Update cached location and time
    instance.otime = instance.time
    instance.oalt = altitude
    instance.olat = fLat
    instance.olon = fLon