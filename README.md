# Python Data Formatter Demo

## Tests
To run tests: `python3 -m unittest tests/app/test_app.py tests/utils/test_utils.py`

## Problem
You have directories containing data files and specification files. The specification files describe the structure of the data files. Write an app that reads format definitions from specification files. Use these definitions to convert the parsed files to NDJSON files.

## Details
- Data files exist in `data/`, specification files exist in `specs/`.
- Spec files will have filenames equal to the file type they specify and an extension of `.csv`. E.g. `fileformat1.csv` specifies files of type `fileformat1`.
- Data files will have filenames based on their specification file name, followed by an underscore, followed by the drop date and an extension of `.txt`. E.g. `fileformat1_2020-10-15.txt` would be parsed using `specs/fileformat1.csv`.
- Spec files will be CSV formatted with columns `column name`, `width`, and `datatype`.
  - `column name`: Name of the keys in the JSON object.
  - `width`: Number of characters taken up by the column in the data file.
  - `datatype`: JSON data type present in the resulting JSON object.
- Data files will be flat text files with lines formatted as specified by their associated specification file.
- Output the parsed files into an NDJSON format with one JSON object for each line of the input file.
- The output file should be in the `output/` directory with the same name as the input file before the extension.

## Example
Given:
- `specs/testformat1.csv`:
```
“column name”,width,datatype
name,10,TEXT
valid,1,BOOLEAN
count,3,INTEGER
```

- `data/testformat1_2021-07-06.txt`:
```
Diabetes 1 1
Asthma 0-14
Stroke 1122
```

Processing `data/testformat1_2021-07-06.txt` results in:
- `output/testformat1_2021-07-06.ndjson`:
```
{“name”: “Diabetes”, “valid”: true, “count”: 1}
{“name”: “Asthma”, “valid”: false, “count”: -14}
{“name”: “Stroke”, “valid”: true, “count”: 1122}
```
