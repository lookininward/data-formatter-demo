import os

def get_dirs(base_dir):
    """
    Ensure required directories exist or create them if missing.

    Args:
        base_dir (str): Base directory path.

    Returns:
        list: List containing paths to specs, data, and output directories.
    """
    SPECS_DIR = os.path.join(base_dir, 'specs')
    DATA_DIR = os.path.join(base_dir, 'data')
    OUTPUT_DIR = os.path.join(base_dir, 'output')

    # Create directories if they don't exist
    for directory in [SPECS_DIR, DATA_DIR, OUTPUT_DIR]:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        
    return [SPECS_DIR, DATA_DIR, OUTPUT_DIR]

def get_files_in_dir(directory):
    """
    Get list of files in a directory.

    Args:
        directory (str): Directory path.

    Returns:
        list: List of file names in the directory.

    Raises:
        FileNotFoundError: If no files are found in the directory.
    """
    files = os.listdir(directory)
    if len(files) == 0:
        raise FileNotFoundError(f"No files found in the {directory} folder")
    return files

def is_valid_spec(spec_file, specs):
    """
    Validate if a spec file is a valid CSV specification.

    Args:
        spec_file (str): File name of the spec file.
        specs (str): Path to the specs directory.

    Returns:
        bool: True if the spec file is valid, False otherwise.
    """
    # Validate file extension
    if not spec_file.endswith('.csv'):
        print(f"Skipping {spec_file} because it is not a .csv file")
        return False
    
    # Validate first line format
    with open(os.path.join(specs, spec_file), 'r') as f:
        first_line = f.readline().strip()
        if first_line != 'column name,width,datatype':
            print(f"Skipping {spec_file} because the first line is not 'column name,width,datatype'")
            return False
    
    return True

def get_specs_dict(spec_file, specs):
    """
    Parse a spec file and return specifications as a dictionary.

    Args:
        spec_file (str): File name of the spec file.
        specs (str): Path to the specs directory.

    Returns:
        dict: Dictionary containing column specifications.
    """
    dict_specs = {}
    
    with open(os.path.join(specs, spec_file), 'r') as f:
        for line in f.readlines()[1:]:
            columns = line.strip().split(',')
            dict_specs[columns[0]] = {
                'width': columns[1],
                'datatype': columns[2]
            }

    return dict_specs