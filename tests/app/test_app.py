import os
import shutil
import unittest
from app import process_data, get_output_line
from tempfile import TemporaryDirectory
from parameterized import parameterized

class TestProcessData(unittest.TestCase):
    def setUp(self):
        # Create temp directory mirroring the project structure
        self.temp_dir = TemporaryDirectory()
        self.BASE_DIR = self.temp_dir.name
        self.specs_dir = os.path.join(self.BASE_DIR, 'specs')
        self.data_dir = os.path.join(self.BASE_DIR, 'data')
        self.output_dir = os.path.join(self.BASE_DIR, 'output')

        # Create mock directories
        os.makedirs(self.specs_dir)
        os.makedirs(self.data_dir)
        os.makedirs(self.output_dir)

    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_process_data_invalid_spec(self):
        # Create a mock spec file with invalid content
        spec_file = 'spec1.txt'
        with open(os.path.join(self.specs_dir, spec_file), 'w') as f:
            f.write("Invalid spec content")

        # Create a mock data file
        data_file = 'data1.txt'
        with open(os.path.join(self.data_dir, data_file), 'w') as f:
            f.write("Mock data content")

        # Calling the function under test
        process_data(self.specs_dir, self.data_dir, self.output_dir, [spec_file], [data_file])

        # Check the directory for the output files
        self.assertEqual(os.listdir(self.output_dir), [])
    
    def test_process_data_valid_spec(self):
            # Create a mock spec file with valid content
        spec_file = 'spec1.csv'
        with open(os.path.join(self.specs_dir, spec_file), 'w') as f:
            f.write("column name,width,datatype\n")
            f.write("name,10,text\n")
            f.write("age,3,integer\n")
            f.write("valid,1,boolean\n")

        # Create a mock data file
        data_file = 'spec1_data.txt'
        with open(os.path.join(self.data_dir, data_file), 'w') as f:
            f.write("John      25 1\n")
            f.write("Jane      30 0\n")

        # Calling the function under test
        process_data(self.specs_dir, self.data_dir, self.output_dir, [spec_file], [data_file])

        # Check the directory for the output files
        self.assertEqual(os.listdir(self.output_dir), ['spec1_data.ndjson'])

        # Check the content of the output file
        with open(os.path.join(self.output_dir, 'spec1_data.ndjson'), 'r') as f:
            output = f.readlines()
            self.assertEqual(len(output), 2)
            self.assertEqual(output[0], '{"name": "John", "age": 25, "valid": True}\n')
            self.assertEqual(output[1], '{"name": "Jane", "age": 30, "valid": False}\n')

    @staticmethod
    def parametrize_test_data():
        return [
            (                
                "testformat1.csv",
                "testformat1_2021-07-06.txt",
                "testformat1_2021-07-06.ndjson",
            ),
            (                
                "testformat2.csv",
                "testformat2_2021-08-01.txt",
                "testformat2_2021-08-01.ndjson",
            ),
            (
                "testformat3.csv",
                "testformat3_2021-09-15.txt",
                "testformat3_2021-09-15.ndjson",
            ),
            (
                "testformat4.csv",
                "testformat4_2022-06-30.txt",
                "testformat4_2022-06-30.ndjson",
            )
        ]

    @parameterized.expand(parametrize_test_data())
    def test_process_data_parametrized(self, spec_filename, data_filename, expected_output_filename):
        # Get current directory and test data files
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        spec_file = os.path.join(base_dir, 'data', spec_filename)
        data_file = os.path.join(base_dir, 'data', data_filename)
        expected_output_file = os.path.join(base_dir, 'data', expected_output_filename)

        # Copy the spec and data files to their respective directories in the temp directory
        shutil.copy(spec_file, self.specs_dir)
        shutil.copy(data_file, self.data_dir)
            
        # Process the data
        process_data(self.specs_dir, self.data_dir, self.output_dir, [spec_filename], [data_filename])
        
        # Check if the output file exists
        output_file_path = os.path.join(self.output_dir, expected_output_filename)
        self.assertTrue(os.path.exists(output_file_path), f"Expected output file {expected_output_filename} not found.")
        
        # Check that the generated output file is equal to expected output file
        with open(output_file_path, 'r') as f:
            output_data = f.read()
            with open(expected_output_file, 'r') as f:
                expected_output_data = f.read()
                self.assertEqual(output_data, expected_output_data)


class TestGetOutputLine(unittest.TestCase):
    @staticmethod
    def test_data():
        return [
            (
                {
                    'column1': {'width': '5', 'datatype': 'text'},
                    'column2': {'width': '1', 'datatype': 'boolean'},
                    'column3': {'width': '3', 'datatype': 'integer'}
                },
                'abcde1  123',
                {'column1': 'abcde', 'column2': True, 'column3': 1}
            ),
            (
                {
                    'name': {'width': '10', 'datatype': 'TEXT'},
                    'valid': {'width': '1', 'datatype': 'BOOLEAN'},
                    'count': {'width': '3', 'datatype': 'INTEGER'}
                },
                'Diabetes  1  1',
                {'name': 'Diabetes', 'valid': True, 'count': 1}
            ),
            (
                {
                    'name': {'width': '10', 'datatype': 'TEXT'},
                    'valid': {'width': '1', 'datatype': 'BOOLEAN'},
                    'count': {'width': '3', 'datatype': 'INTEGER'}
                },
                'Asthma    0-14',
                {'name': 'Asthma', 'valid': False, 'count': -14}
            ),
            (
                {
                    'name': {'width': '10', 'datatype': 'TEXT'},
                    'valid': {'width': '1', 'datatype': 'BOOLEAN'},
                    'count': {'width': '3', 'datatype': 'INTEGER'}
                },
                'Stroke    1122',
                {'name': 'Stroke', 'valid': True, 'count': 122}
            )
        ]
    
    @parameterized.expand(test_data())
    def test_get_output_line(self, dict_specs, line, expected_output):
        self.assertEqual(get_output_line( line, dict_specs), expected_output)

if __name__ == '__main__':
    unittest.main()