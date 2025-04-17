import os
from .coefficient_handler import WMMCoefficientHandler

def read_coefficients(instance):
    """
    Read the World Magnetic Model (WMM) coefficients from a file and populate the instance variables.
    
    This function reads spherical harmonic coefficients from a WMM coefficient file (.COF) and
    assigns them to the appropriate arrays in the provided instance. The coefficient file follows
    the standard format used by NOAA's National Centers for Environmental Information (NCEI).
    
    Parameters:
        instance: An instance of WMMv2 or compatible model class that contains the following attributes:
            - coeff_file (str, optional): Custom path to coefficient file
            - epoch (float): Base epoch of the model (will be set from file)
            - defaultDate (float): Default calculation date (will be set to epoch + 2.5 years)
            - c (list): 2D array for Gauss coefficients (gnm, hnm)
            - cd (list): 2D array for secular variation coefficients (dgnm, dhnm)
    
    Notes:
        - If instance.coeff_file is not specified, the default WMM.COF file in the package's
          data directory will be used.
        - The file format is expected to contain:
            * Header line with epoch year 
            * Data lines with: n, m, gnm, hnm, dgnm, dhnm values
                where:
                - n: degree (int)
                - m: order (int)
                - gnm: Gauss coefficient (float, nT)
                - hnm: Gauss coefficient (float, nT)
                - dgnm: Annual rate of change (float, nT/year)
                - dhnm: Annual rate of change (float, nT/year)
        - Coefficients are stored in a specific arrangement in the instance arrays:
            * c[m][n] stores gnm values
            * c[n][m-1] stores hnm values (for m > 0)
            * cd[m][n] stores dgnm values
            * cd[n][m-1] stores dhnm values (for m > 0)
    
    Raises:
        FileNotFoundError: If the coefficient file cannot be found
        ValueError: If the coefficient file format is invalid
    """
    file_path = getattr(instance, 'coeff_file', None)
    
    if not file_path:
        # Use default coefficient file
        file_path = os.path.join(os.path.dirname(__file__), "data", "WMM.COF")
    
    # Validate the coefficient file using the handler
    is_valid, error_message = WMMCoefficientHandler.validate_coefficient_file(file_path)
    
    if not is_valid:
        raise ValueError(f"Invalid coefficient file: {error_message}")
    
    # Read and parse the file
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('9999'):
                break
                
            parts = line.split()
            
            # Header line with epoch information
            if len(parts) <= 3 and any(part.replace('.', '', 1).isdigit() for part in parts):
                for part in parts:
                    if part.replace('.', '', 1).isdigit():
                        try:
                            instance.epoch = float(part)
                            instance.defaultDate = instance.epoch + 2.5
                            break
                        except ValueError:
                            pass
                continue
            
            # Coefficient line
            if len(parts) >= 6:
                try:
                    n = int(parts[0])
                    m = int(parts[1])
                    gnm = float(parts[2])
                    hnm = float(parts[3])
                    dgnm = float(parts[4])
                    dhnm = float(parts[5])
                    
                    if m <= n:
                        instance.c[m][n] = gnm
                        instance.cd[m][n] = dgnm
                        if m != 0:
                            instance.c[n][m - 1] = hnm
                            instance.cd[n][m - 1] = dhnm
                except (ValueError, IndexError):
                    # Skip invalid lines
                    continue

def read_coefficients_from_bytes(instance, byte_data):
    """
    Read the World Magnetic Model (WMM) coefficients from byte data and populate the instance variables.
    
    This function is useful for processing coefficient data received via HTTP requests or other
    byte streams without needing to save to a temporary file first.
    
    Parameters:
        instance: An instance of WMMv2 or compatible model class
        byte_data (bytes): Byte stream containing WMM coefficient data
        
    Raises:
        ValueError: If the coefficient data is invalid or cannot be parsed
    """
    # Use the coefficient handler to validate and parse the data
    is_valid, error_message = WMMCoefficientHandler.validate_bytes(byte_data)
    
    if not is_valid:
        raise ValueError(f"Invalid coefficient data: {error_message}")
    
    # Parse the data into coefficient arrays
    success, result = WMMCoefficientHandler.parse_bytes_to_arrays(byte_data)
    
    if not success:
        raise ValueError(f"Failed to parse coefficient data: {result}")
    
    # Set the parsed values in the instance
    instance.epoch = result['epoch']
    instance.defaultDate = instance.epoch + 2.5
    
    # Copy the coefficient arrays
    for m in range(len(result['c'])):
        for n in range(len(result['c'][m])):
            instance.c[m][n] = result['c'][m][n]
            instance.cd[m][n] = result['cd'][m][n]

def replace_coefficient_file(new_file_path, backup=True):
    """
    Replace the default WMM coefficient file with a new one.
    
    This function validates the new coefficient file and copies it to the package's
    data directory, optionally creating a backup of the original file.
    
    Parameters:
        new_file_path (str): Path to the new coefficient file
        backup (bool): Whether to create a backup of the original file
        
    Returns:
        tuple: (success, message)
            - success (bool): True if replacement was successful, False otherwise
            - message (str): Description of the operation outcome
    """
    return WMMCoefficientHandler.replace_default_coefficient_file(new_file_path, backup=backup)

def convert_to_cof_format(input_file_path, output_file_path=None):
    """
    Convert a text file with WMM coefficient data to the proper COF format.
    
    This function attempts to parse a text file containing WMM coefficients and
    reformat it to the standard COF format used by the WMM model.
    
    Parameters:
        input_file_path (str): Path to the input text file
        output_file_path (str, optional): Path for the output COF file
                                        If None, uses the same name with .COF extension
                                        
    Returns:
        tuple: (success, file_path or error_message)
            - success (bool): True if conversion was successful, False otherwise
            - result: Path to the created COF file if successful, error message if failed
    """
    return WMMCoefficientHandler.convert_to_cof_format(input_file_path, output_file_path)

def restore_original_coefficients():
    """
    Restore the original WMM.COF file from backup if available.
    
    Returns:
        tuple: (success, message)
            - success (bool): True if restoration was successful, False otherwise
            - message (str): Description of the operation outcome
    """
    return WMMCoefficientHandler.restore_backup()

def validate_coefficient_file(file_path):
    """
    Validate that a file contains properly formatted WMM coefficients.
    
    Parameters:
        file_path (str): Path to the coefficient file to validate
        
    Returns:
        tuple: (is_valid, error_message or None)
            - is_valid (bool): True if the file is valid, False otherwise
            - error_message (str or None): Description of the validation error, or None if valid
    """
    return WMMCoefficientHandler.validate_coefficient_file(file_path)

def parse_coefficients_to_arrays(file_path):
    """
    Parse a WMM coefficient file directly into arrays.
    
    Parameters:
        file_path (str): Path to the WMM coefficient file
        
    Returns:
        tuple: (success, result)
            - success (bool): True if parsing was successful, False otherwise
            - result: Dictionary with coefficient arrays if successful, error message if failed
    """
    return WMMCoefficientHandler.parse_to_arrays(file_path)

def save_coefficients_from_request(request_data, output_file_path):
    """
    Save coefficient data from a HTTP request to a file.
    
    Parameters:
        request_data (bytes): Raw byte data from the request body
        output_file_path (str): Path where to save the coefficient file
        
    Returns:
        tuple: (success, message)
            - success (bool): True if operation was successful, False otherwise
            - message (str): Description of the operation outcome or error
    """
    return WMMCoefficientHandler.bytes_to_cof_file(request_data, output_file_path)