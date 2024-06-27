import os
import shutil
import unittest
from app import process_data
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

    @staticmethod
    def parametrize_test_data():
        return [
            (                
                "testformat1.csv",
                "testformat1_2021-07-06.txt",
                'testformat1.ndjson',
            ),
            (                
                "testformat2.csv",
                "testformat2_2021-08-01.txt",
                'testformat2.ndjson',
            ),
            (
                "testformat3.csv",
                "testformat3_2021-09-15.txt",
                'testformat3.ndjson',
            ),
            (
                "testformat4.csv",
                "testformat4_2022-06-30.txt",
                'testformat4.ndjson'
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
        
if __name__ == '__main__':
    unittest.main()
