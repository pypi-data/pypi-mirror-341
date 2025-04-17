import os
import shutil
import re
import tempfile
import numpy as np

class WMMCoefficientHandler:
    """
    Utility class for handling World Magnetic Model coefficient files.
    
    This class provides functionality to:
    1. Validate WMM coefficient files (.COF format)
    2. Convert text files to proper COF format
    3. Replace the default WMM.COF file with a custom one
    4. Parse coefficient files for direct use in code
    5. Handle coefficient data from byte streams (e.g., from POST requests)
    
    The World Magnetic Model (WMM) is a standard mathematical representation of Earth's
    magnetic field used by navigation systems worldwide.
    """
    
    @staticmethod
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
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            with open(file_path, "r") as f:
                lines = f.readlines()
                
            # Check if file has content
            if not lines:
                return False, "File is empty"
                
            # Validate header line (should contain epoch year and possibly other metadata)
            header_parts = lines[0].strip().split()
            if len(header_parts) < 1:
                return False, "Invalid header: missing epoch year"
                
            try:
                epoch_year = float(re.search(r'\d+\.\d+', lines[0]).group())
                if epoch_year < 1900 or epoch_year > 2100:  # Reasonable range check
                    return False, f"Epoch year {epoch_year} outside reasonable range (1900-2100)"
            except (ValueError, AttributeError):
                return False, f"Invalid epoch year format in header: {lines[0]}"
                
            # Validate coefficient lines
            line_number = 1
            valid_coef_lines = 0
            
            for line in lines[1:]:
                line = line.strip()
                # Skip empty lines or end marker lines (999...)
                if not line or line.startswith('9999'):
                    continue
                    
                parts = line.split()
                # Each coefficient line should have at least 6 values: n, m, gnm, hnm, dgnm, dhnm
                if len(parts) < 6:
                    return False, f"Line {line_number}: Invalid format, expected at least 6 values"
                    
                try:
                    n = int(parts[0])
                    m = int(parts[1])
                    gnm = float(parts[2])
                    hnm = float(parts[3])
                    dgnm = float(parts[4])
                    dhnm = float(parts[5])
                    
                    # Basic validation of degree and order
                    if n < 0 or n > 13:  # Maximum degree in typical WMM models
                        return False, f"Line {line_number}: Degree n={n} out of valid range (0-13)"
                    if m < 0 or m > n:
                        return False, f"Line {line_number}: Order m={m} out of valid range (0-{n})"
                    
                    valid_coef_lines += 1
                        
                except ValueError:
                    return False, f"Line {line_number}: Invalid numeric format"
                    
                line_number += 1
            
            # Check if we have enough coefficient lines
            if valid_coef_lines < 10:  # At minimum we need main harmonic coefficients
                return False, f"File contains only {valid_coef_lines} valid coefficient lines, minimum 10 expected"
                
            # Check if file has terminator lines
            has_terminator = False
            for line in lines[-2:]:
                if line.strip().startswith('9999'):
                    has_terminator = True
                    break
                    
            if not has_terminator:
                # Not a strict error, but worth noting
                print("Warning: File does not contain standard terminator lines (999...)")
                
            return True, None
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def convert_to_cof_format(input_file_path, output_file_path=None):
        """
        Convert a text file with WMM coefficient data to the proper COF format.
        
        This method attempts to parse a text file containing WMM coefficients and
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
        if output_file_path is None:
            base_name = os.path.splitext(input_file_path)[0]
            output_file_path = base_name + ".COF"
        
        try:
            with open(input_file_path, 'r') as f:
                lines = f.readlines()
            
            # Process the file to extract the relevant data
            processed_lines = []
            epoch_year = None
            model_name = None
            date_info = None
            
            # Try to extract header information
            for line in lines[:5]:  # Check first few lines for header info
                line = line.strip()
                if not line:
                    continue
                
                # Look for a float that could be a year
                year_match = re.search(r'(?<!\d)(?:19|20)\d{2}(?:\.\d+)?(?!\d)', line)
                if year_match and not epoch_year:
                    epoch_year = year_match.group()
                
                # Look for model name
                model_match = re.search(r'WMM-\d{4}', line)
                if model_match and not model_name:
                    model_name = model_match.group()
                
                # Look for a date
                date_match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', line)
                if date_match and not date_info:
                    date_info = date_match.group()
            
            # If we couldn't find the epoch year, try to infer it
            if not epoch_year:
                # Try from model name
                if model_name:
                    try:
                        epoch_year = model_name.split('-')[1]
                        # Add decimal point if needed
                        if '.' not in epoch_year:
                            epoch_year = f"{epoch_year}.0"
                    except:
                        pass
                
                # If still not found, use a default value and warn
                if not epoch_year:
                    # Default to 2025.0 with warning
                    epoch_year = "2025.0"
                    print("Warning: Could not determine epoch year, using default 2025.0")
            
            # If no model name found, create one from epoch year
            if not model_name:
                model_name = f"WMM-{int(float(epoch_year))}"
            
            # If no date info found, use the current date or epoch year as a fallback
            if not date_info:
                from datetime import datetime
                date_info = datetime.now().strftime("%m/%d/%Y")
            
            # Create the header line with proper formatting
            header = f"    {epoch_year}            {model_name}     {date_info}"
            processed_lines.append(header)
            
            # Process coefficient lines
            for line in lines:
                line = line.strip()
                if not line or line.startswith('9999'):  # Skip empty or marker lines
                    continue
                
                parts = line.split()
                # Skip the header line if we encounter it again
                if len(parts) <= 3 and any(part.replace('.', '').isdigit() and 1900 <= float(part) <= 2100 for part in parts if part.replace('.', '').isdigit()):
                    continue
                
                # Check if this looks like a coefficient line (n, m, gnm, hnm, dgnm, dhnm)
                if len(parts) >= 6:
                    try:
                        n = int(parts[0])
                        m = int(parts[1])
                        gnm = float(parts[2])
                        hnm = float(parts[3])
                        dgnm = float(parts[4])
                        dhnm = float(parts[5])
                        
                        # Ensure values are within valid ranges
                        if 0 <= n <= 13 and 0 <= m <= n:
                            # Format with proper spacing (align columns)
                            formatted_line = f"{n:3d}{m:3d}{gnm:11.1f}{hnm:11.1f}{dgnm:11.1f}{dhnm:11.1f}"
                            processed_lines.append(formatted_line)
                    except ValueError:
                        # Not a coefficient line, skip it
                        continue
            
            # Add terminator lines
            processed_lines.append("999999999999999999999999999999999999999999999999")
            processed_lines.append("999999999999999999999999999999999999999999999999")
            
            # Write the processed data to the output file
            with open(output_file_path, 'w') as f:
                for line in processed_lines:
                    f.write(line + '\n')
            
            # Validate the created file
            is_valid, error_message = WMMCoefficientHandler.validate_coefficient_file(output_file_path)
            if is_valid:
                return True, output_file_path
            else:
                return False, f"Created file is invalid: {error_message}"
                
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    @staticmethod
    def replace_default_coefficient_file(new_file_path, package_dir=None, backup=True):
        """
        Replace the default WMM.COF file with a custom one.
        
        Parameters:
            new_file_path (str): Path to the new coefficient file
            package_dir (str, optional): Directory of the WMM package (containing data/WMM.COF)
                                         If None, tries to determine automatically
            backup (bool): Whether to create a backup of the original file
            
        Returns:
            tuple: (success, message)
                - success (bool): True if replacement was successful, False otherwise
                - message (str): Description of the operation outcome
        """
        # First validate the new file
        is_valid, error_message = WMMCoefficientHandler.validate_coefficient_file(new_file_path)
        if not is_valid:
            return False, f"Validation failed: {error_message}"
        
        # Determine the package directory if not provided
        if package_dir is None:
            # Try to find the module directory
            import inspect
            import sys
            
            # Try to find the WMM module in loaded modules
            wmm_module = None
            for name, module in sys.modules.items():
                if 'pywmm' in name.lower():
                    wmm_module = module
                    break
            
            if wmm_module:
                try:
                    # Get the file path of the module
                    package_dir = os.path.dirname(inspect.getfile(wmm_module))
                except (TypeError, ValueError):
                    pass
            
            # If still not found, use current directory
            if not package_dir:
                package_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Determine the target path for WMM.COF
        data_dir = os.path.join(package_dir, "data")
        target_path = os.path.join(data_dir, "WMM.COF")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
            except Exception as e:
                return False, f"Failed to create data directory: {str(e)}"
        
        # Create backup if requested
        if backup and os.path.exists(target_path):
            backup_path = target_path + ".backup"
            try:
                shutil.copy2(target_path, backup_path)
                print(f"Backup created at {backup_path}")
            except Exception as e:
                return False, f"Failed to create backup: {str(e)}"
        
        # Copy the new file to the target location
        try:
            shutil.copy2(new_file_path, target_path)
            return True, f"Successfully replaced {target_path} with {os.path.basename(new_file_path)}"
        except Exception as e:
            return False, f"Failed to replace coefficient file: {str(e)}"
    
    @staticmethod
    def parse_to_arrays(cof_file_path):
        """
        Parse a WMM coefficient file directly into arrays for use in the WMMv2 class.
        
        This method reads the coefficient file and returns the data in the format
        expected by the WMMv2 constructor.
        
        Parameters:
            cof_file_path (str): Path to the WMM coefficient file
            
        Returns:
            tuple: (success, result)
                - success (bool): True if parsing was successful, False otherwise
                - result: Dictionary with coefficient arrays if successful, error message if failed
        """
        try:
            # Validate file first
            is_valid, error_message = WMMCoefficientHandler.validate_coefficient_file(cof_file_path)
            if not is_valid:
                return False, f"Invalid coefficient file: {error_message}"
            
            with open(cof_file_path, 'r') as f:
                lines = f.readlines()
            
            return WMMCoefficientHandler._parse_lines_to_arrays(lines)
            
        except Exception as e:
            return False, f"Parsing error: {str(e)}"
    
    @staticmethod
    def parse_bytes_to_arrays(byte_data):
        """
        Parse WMM coefficient data from a byte stream directly into arrays.
        
        This method is useful for processing data received via HTTP requests
        without needing to save to a temporary file first.
        
        Parameters:
            byte_data (bytes): Byte stream containing WMM coefficient data
            
        Returns:
            tuple: (success, result)
                - success (bool): True if parsing was successful, False otherwise
                - result: Dictionary with coefficient arrays if successful, error message if failed
        """
        try:
            # Convert bytes to string and split into lines
            text_data = byte_data.decode('utf-8')
            lines = text_data.splitlines()
            
            return WMMCoefficientHandler._parse_lines_to_arrays(lines)
            
        except UnicodeDecodeError:
            # Try with different encodings if UTF-8 fails
            try:
                text_data = byte_data.decode('latin-1')
                lines = text_data.splitlines()
                return WMMCoefficientHandler._parse_lines_to_arrays(lines)
            except Exception as e:
                return False, f"Failed to decode byte data: {str(e)}"
        except Exception as e:
            return False, f"Parsing error: {str(e)}"
    
    @staticmethod
    def _parse_lines_to_arrays(lines):
        """
        Internal helper method to parse coefficient lines into arrays.
        
        Parameters:
            lines (list): List of strings containing coefficient data
            
        Returns:
            tuple: (success, result)
                - success (bool): True if parsing was successful, False otherwise
                - result: Dictionary with coefficient arrays if successful, error message if failed
        """
        try:
            if not lines:
                return False, "No data provided"
                
            # Extract epoch from header
            header_line = lines[0].strip()
            epoch_match = re.search(r'\d+\.\d+', header_line)
            if not epoch_match:
                return False, "Could not parse epoch year from header"
            
            epoch = float(epoch_match.group())
            
            # Initialize coefficient arrays (13x13 for degrees/orders 0-12)
            c = [[0.0 for _ in range(13)] for _ in range(13)]   # Main field coefficients
            cd = [[0.0 for _ in range(13)] for _ in range(13)]  # Secular variation coefficients
            
            # Parse coefficient lines
            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('9999'):  # Skip empty or terminator lines
                    continue
                
                parts = line.split()
                if len(parts) < 6:
                    continue
                
                try:
                    n = int(parts[0])
                    m = int(parts[1])
                    gnm = float(parts[2])
                    hnm = float(parts[3])
                    dgnm = float(parts[4])
                    dhnm = float(parts[5])
                    
                    # Validate degree and order
                    if n < 0 or n > 12 or m < 0 or m > n:
                        continue
                    
                    # Store coefficients in the appropriate arrays
                    # Main field coefficients (gnm and hnm)
                    c[m][n] = gnm
                    if m > 0:
                        c[n][m-1] = hnm
                    
                    # Secular variation coefficients (dgnm and dhnm)
                    cd[m][n] = dgnm
                    if m > 0:
                        cd[n][m-1] = dhnm
                        
                except (ValueError, IndexError):
                    # Skip invalid lines
                    continue
            
            # Return the parsed data
            return True, {
                'epoch': epoch,
                'c': c,
                'cd': cd
            }
            
        except Exception as e:
            return False, f"Parsing error: {str(e)}"
    
    @staticmethod
    def validate_bytes(byte_data):
        """
        Validate WMM coefficient data from a byte stream.
        
        This method is useful for validating data received via HTTP requests
        without needing to save to a temporary file first.
        
        Parameters:
            byte_data (bytes): Byte stream containing WMM coefficient data
            
        Returns:
            tuple: (is_valid, error_message or None)
                - is_valid (bool): True if the data is valid, False otherwise
                - error_message (str or None): Description of the validation error, or None if valid
        """
        try:
            # Try UTF-8 decoding first
            text_data = byte_data.decode('utf-8')
            lines = text_data.splitlines()
            
            # Now perform the same validation as the file-based method
            return WMMCoefficientHandler._validate_lines(lines)
            
        except UnicodeDecodeError:
            # Try with different encodings if UTF-8 fails
            try:
                text_data = byte_data.decode('latin-1')
                lines = text_data.splitlines()
                # Repeat validation with latin-1 decoded data
                return WMMCoefficientHandler._validate_lines(lines)
            except Exception as e:
                return False, f"Failed to decode byte data: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def _validate_lines(lines):
        """
        Internal helper method to validate coefficient data lines.
        
        Parameters:
            lines (list): List of strings containing coefficient data
            
        Returns:
            tuple: (is_valid, error_message or None)
                - is_valid (bool): True if the data is valid, False otherwise
                - error_message (str or None): Description of the validation error, or None if valid
        """
        try:
            if not lines:
                return False, "No data provided"
                
            header_parts = lines[0].strip().split()
            if len(header_parts) < 1:
                return False, "Invalid header: missing epoch year"
                
            try:
                epoch_year = float(re.search(r'\d+\.\d+', lines[0]).group())
                if epoch_year < 1900 or epoch_year > 2100:  # Reasonable range check
                    return False, f"Epoch year {epoch_year} outside reasonable range (1900-2100)"
            except (ValueError, AttributeError):
                return False, f"Invalid epoch year format in header: {lines[0]}"
                
            # Validate coefficient lines
            line_number = 1
            valid_coef_lines = 0
            
            for line in lines[1:]:
                line = line.strip()
                # Skip empty lines or end marker lines
                if not line or line.startswith('9999'):
                    continue
                    
                parts = line.split()
                # Each coefficient line should have at least 6 values
                if len(parts) < 6:
                    return False, f"Line {line_number}: Invalid format, expected at least 6 values"
                    
                try:
                    n = int(parts[0])
                    m = int(parts[1])
                    
                    # Basic validation of degree and order
                    if n < 0 or n > 13: 
                        return False, f"Line {line_number}: Degree n={n} out of valid range (0-13)"
                    if m < 0 or m > n:
                        return False, f"Line {line_number}: Order m={m} out of valid range (0-{n})"
                    
                    valid_coef_lines += 1
                        
                except ValueError:
                    return False, f"Line {line_number}: Invalid numeric format"
                    
                line_number += 1
            
            # Check if we have enough coefficient lines
            if valid_coef_lines < 10:
                return False, f"Data contains only {valid_coef_lines} valid coefficient lines, minimum 10 expected"
                    
            return True, None
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def bytes_to_cof_file(byte_data, output_file_path):
        """
        Convert WMM coefficient data from a byte stream and save to a COF file.
        
        This method is useful for saving data received via HTTP requests directly to a COF file.
        
        Parameters:
            byte_data (bytes): Byte stream containing WMM coefficient data
            output_file_path (str): Path where the COF file should be saved
            
        Returns:
            tuple: (success, message)
                - success (bool): True if operation was successful, False otherwise
                - message (str): Description of the operation outcome or error
        """
        try:
            # First validate the data
            is_valid, error_message = WMMCoefficientHandler.validate_bytes(byte_data)
            
            if not is_valid:
                # If invalid, try to convert/format it
                try:
                    # Create a temporary file for the input data
                    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                        temp_file.write(byte_data)
                        temp_file_path = temp_file.name
                    
                    # Try to convert it to proper format
                    success, result = WMMCoefficientHandler.convert_to_cof_format(temp_file_path, output_file_path)
                    
                    # Remove the temporary file
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                    
                    return success, result
                    
                except Exception as e:
                    return False, f"Invalid data and conversion failed: {str(e)}"
            
            # If data is already valid, write it directly to the output file
            try:
                # Decode to text
                try:
                    text_data = byte_data.decode('utf-8')
                except UnicodeDecodeError:
                    text_data = byte_data.decode('latin-1')
                
                # Write to the output file
                with open(output_file_path, 'w') as f:
                    f.write(text_data)
                
                return True, output_file_path
                
            except Exception as e:
                return False, f"Failed to write data to file: {str(e)}"
            
        except Exception as e:
            return False, f"Processing error: {str(e)}"

    @staticmethod
    def restore_backup(package_dir=None):
        """
        Restore the original WMM.COF file from backup if available.
        
        Parameters:
            package_dir (str, optional): Directory of the WMM package (containing data/WMM.COF)
                                         If None, tries to determine automatically
                                         
        Returns:
            tuple: (success, message)
                - success (bool): True if restoration was successful, False otherwise
                - message (str): Description of the operation outcome
        """
        # Determine the package directory if not provided
        if package_dir is None:
            # Try to find the module directory
            import inspect
            import sys
            
            # Try to find the WMM module in loaded modules
            wmm_module = None
            for name, module in sys.modules.items():
                if 'pywmm' in name.lower():
                    wmm_module = module
                    break
            
            if wmm_module:
                try:
                    # Get the file path of the module
                    package_dir = os.path.dirname(inspect.getfile(wmm_module))
                except (TypeError, ValueError):
                    pass
            
            # If still not found, use current directory
            if not package_dir:
                package_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Determine the paths
        data_dir = os.path.join(package_dir, "data")
        target_path = os.path.join(data_dir, "WMM.COF")
        backup_path = target_path + ".backup"
        
        # Check if backup exists
        if not os.path.exists(backup_path):
            return False, "No backup file found"
        
        # Restore from backup
        try:
            shutil.copy2(backup_path, target_path)
            return True, f"Successfully restored {target_path} from backup"
        except Exception as e:
            return False, f"Failed to restore from backup: {str(e)}"