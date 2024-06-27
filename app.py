import os
from utils.file_utils import get_dirs, get_files_in_dir, get_specs_dict, is_valid_spec

# Get base directory and directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
[specs_dir, data_dir, output_dir] = get_dirs(BASE_DIR)

# Get list of files in specs and data
specs_files = get_files_in_dir(specs_dir)
data_files = get_files_in_dir(data_dir)

def get_output_line(line, dict_specs):
    """
    Process a single line of data based on given specifications.

    Args:
        line (str): A single line of data to be processed.
        dict_specs (dict): Dictionary containing column specifications.

    Returns:
        dict: Processed output line as a dictionary.
    """
    output_line = {}
    start = 0

    for column_name, column_specs in dict_specs.items():
        width = int(column_specs['width'])
        datatype = column_specs['datatype'].lower()
        end = start + width
        value = line[start:end].strip()

        # Convert the value based on the datatype
        if datatype == 'boolean':
            output_line[column_name] = value == '1'
        elif datatype == 'integer':
            try:
                output_line[column_name] = int(value)
            except ValueError:
                output_line[column_name] = None
        elif datatype == 'text':
            output_line[column_name] = value
        else:
            output_line[column_name] = value

        start = end
        
    return output_line

def process_data(specs_dir, data_dir, output_dir, specs_files, data_files):
    """
    Process data files based on specifications and write output to JSON lines format.

    Args:
        specs_dir (str): Directory containing specification files.
        data_dir (str): Directory containing data files.
        output_dir (str): Directory where output files will be written.
        specs_files (list): List of specification file names.
        data_files (list): List of data file names.
    """
    for spec_file in specs_files:
        if not is_valid_spec(spec_file, specs_dir):
            continue

        spec_filename = os.path.splitext(spec_file)[0]
        dict_specs = get_specs_dict(spec_file, specs_dir)

        for data_file in data_files:
            data_filename = os.path.splitext(data_file)[0].split('_')[0]

            if spec_filename != data_filename:
                continue

            # Prepare output file
            output_filename = os.path.join(output_dir, f"{spec_filename}.ndjson")

            # Process data file and write output
            with open(os.path.join(data_dir, data_file), 'r') as f:
                with open(output_filename, 'w') as output_file:
                    for line in f.readlines():
                        output_line = get_output_line(line, dict_specs)
                        output_file.write(str(output_line).replace("'", '"') + '\n')


process_data(specs_dir, data_dir, output_dir, specs_files, data_files)