What is NDJSON?

NDJSON (Newline Delimited JSON) is a simple and convenient format for storing or streaming JSON data. It separates individual JSON objects by newlines. Each line of the NDJSON file contains a valid JSON object, making it easy to parse and process each object independently. NDJSON is commonly used for scenarios where you need to handle a stream of JSON objects sequentially.

# Tests
To run the tests, run `python3 -m unittest tests/app/test_app.py tests/utils/test_utils.py`