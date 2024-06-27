import os
import unittest
from tempfile import TemporaryDirectory
from utils.file_utils import get_dirs, get_files_in_dir, get_specs_dict, is_valid_spec

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.base_dir = self.temp_dir.name
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def test_get_dirs_creates_directories(self):
        # Case 1: Directories should be created if they don't exist

        # Directories should not exist
        self.specs_dir = os.path.join(self.base_dir, 'specs')
        self.assertFalse(os.path.isdir(self.specs_dir))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.assertFalse(os.path.isdir(self.data_dir))        
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.assertFalse(os.path.isdir(self.output_dir))
            
        # Call get_dirs to create the directories
        dirs = get_dirs(self.base_dir)
        
        # Assert that the directories are created
        self.assertEqual(len(dirs), 3)
        self.assertTrue(all([os.path.isdir(d) for d in dirs]))
        self.assertEqual(dirs[0], self.specs_dir)
        self.assertEqual(dirs[1], self.data_dir)
        self.assertEqual(dirs[2], self.output_dir)
        
    def test_get_dirs_returns_existing_directories(self):
        # Case 2: Should return the directories if they already exist
        self.specs_dir = os.path.join(self.base_dir, 'specs')
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.output_dir = os.path.join(self. base_dir, 'output')

        # Create directories before calling get_dirs
        os.makedirs(self.specs_dir)
        os.makedirs(self.data_dir)
        os.makedirs(self.output_dir)
        
        # Add test files to ensure they are not overwritten
        specs_file = os.path.join(self.specs_dir, 'test_specs.txt')
        data_file = os.path.join(self.data_dir, 'test_data.txt')
        output_file = os.path.join(self.output_dir, 'test_output.txt')
        
        with open(specs_file, 'w') as f:
            f.write('specs file content')
        with open(data_file, 'w') as f:
            f.write('data file content')
        with open(output_file, 'w') as f:
            f.write('output file content')
            
        # Call get_dirs to get the directories
        dirs = get_dirs(self. base_dir)
        
        # Assert that the directories are returned and not recreated
        self.assertEqual(len(dirs), 3)
        self.assertTrue(all([os.path.isdir(d) for d in dirs]))
        self.assertEqual(dirs[0], self.specs_dir)
        self.assertEqual(dirs[1], self.data_dir)
        self.assertEqual(dirs[2], self.output_dir)
        
        # Assert that the test files are still there
        self.assertTrue(os.path.isfile(specs_file))
        self.assertTrue(os.path.isfile(data_file))
        self.assertTrue(os.path.isfile(output_file))

        # Check the content of the files to ensure they are not overwritten
        with open(specs_file, 'r') as f:
            self.assertEqual(f.read(), 'specs file content')
        with open(data_file, 'r') as f:
            self.assertEqual(f.read(), 'data file content')
        with open(output_file, 'r') as f:
            self.assertEqual(f.read(), 'output file content')
        
    def test_get_files_in_dir_raises_error_for_empty_directory(self):
        # Case 1: The directory is empty, and a FileNotFoundError should be raised
        [specs_dir, data_dir, output_dir] = get_dirs(self. base_dir)
        with self.assertRaises(FileNotFoundError):
            get_files_in_dir(specs_dir)
        with self.assertRaises(FileNotFoundError):
            get_files_in_dir(data_dir)
        with self.assertRaises(FileNotFoundError):
            get_files_in_dir(output_dir)
            
    def test_get_files_in_dir_returns_files(self):
        # Case 2: The directory contains files, and the function should return the list of files
        [specs_dir, data_dir, output_dir] = get_dirs(self. base_dir)
        test_file_specs = os.path.join(specs_dir, 'test_specs.txt')
        test_file_data = os.path.join(data_dir, 'test_data.txt')
        test_file_output = os.path.join(output_dir, 'test_output.txt')
        
        with open(test_file_specs, 'w') as f:
            f.write('specs file content')
        with open(test_file_data, 'w') as f:
            f.write('data file content')
        with open(test_file_output, 'w') as f:
            f.write('output file content')
        
        self.assertEqual(get_files_in_dir(specs_dir), ['test_specs.txt'])
        self.assertEqual(get_files_in_dir(data_dir), ['test_data.txt'])
        self.assertEqual(get_files_in_dir(output_dir), ['test_output.txt'])
        
    def test_is_valid_spec_non_csv_file(self):
        # Case 1: The file is not a .csv file, and the function should return False
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.txt'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('column name,width,datatype\n')
        self.assertFalse(is_valid_spec(test_file, specs_dir))
        
    def test_is_valid_spec_invalid_first_line(self):
        # Case 2: The first line of the file is not 'column name,width,datatype', and the function should return False
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.csv'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('invalid first line\n')
        self.assertFalse(is_valid_spec(test_file, specs_dir))
        
    def test_is_valid_spec_valid_file(self):
        # Case 3: The file is a .csv file with the correct first line, and the function should return True
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.csv'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('column name,width,datatype\n')
        self.assertTrue(is_valid_spec(test_file, specs_dir))
        
    def test_get_specs_dict_valid_file(self):
        # Case 1: The spec_file exists and is correctly formatted, and the function should return a dictionary
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.csv'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('column name,width,datatype\nname,10,string\nage,3,int\nvalid,1,bool\n')
        expected_dict = {
            'name': {'width': '10', 'datatype': 'string'},
            'age': {'width': '3', 'datatype': 'int'},
            'valid': {'width': '1', 'datatype': 'bool'}
        }
        self.assertEqual(get_specs_dict(test_file, specs_dir), expected_dict)
    
        
    def test_get_specs_dict_empty_file(self):
        # Case 2: The spec_file does not exist or is empty, and the function should return an empty dictionary
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.csv'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('column name,width,datatype\n')
        expected_dict = {}
        self.assertEqual(get_specs_dict(test_file, specs_dir), expected_dict)
        
    def test_get_specs_dict_missing_file(self):
        # Case 3: The spec_file does not exist, and the function should raise a FileNotFoundError
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'missing_specs.csv'
        with self.assertRaises(FileNotFoundError):
            get_specs_dict(test_file, specs_dir)
            
    def test_get_specs_dict_incorrectly_formatted_file(self):
        # Case 4: The spec_file exists but is incorrectly formatted, and the function should handle it gracefully
        [specs_dir, _, _] = get_dirs(self. base_dir)
        test_file = 'test_specs.csv'
        with open(os.path.join(specs_dir, test_file), 'w') as f:
            f.write('column name,width,datatype\nname,10\nage,3,int\nvalid,bool\n')
        
        with self.assertRaises(IndexError):
            get_specs_dict(test_file, specs_dir)

if __name__ == '__main__':
    unittest.main()