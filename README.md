# Sheet2Api
A simple script that converts xlsx or csv files into a basic REST API using pandas and FastAPI. 
This tiny API makes it easy to use xlsx or csv-files in new ways.

## Features
- Convert xlsx or csv files to a REST API
- Support for multiple file formats (xlsx and csv)
- Multiple endpoints for data retrieval and manipulation

## Usage

### Installation
* Install the required libraries by running `pip install -r requirements.txt`

### Starting the API
* Run the following command to start the FastAPI server: `fastapi dev main.py` or `fastapi run main.py`
* The API will be available at `http://127.0.0.1:8000`
* The docs/swagger si available at `http://127.0.0.1:8000/docs`
* **NOTE**: The first thing which has to be called is a reload-endpoint to use all other endpoints or they fail!

### Available Endpoints

#### Activating/Reloading Data
##### `/reload/xlsx?file=<path/to/file.xlsx>`: Reloads the data from an xlsx file. Specify the file path using `file` query parameter.

##### `/reload/csv?file=<path/to/file.csv>&sep=<sep/value>`: Reloads the data from a CSV file. Specify the file path and separator character using `file` and `sep` query parameters, respectively (default in code is: `;`).

#### Retrieving Data
##### `/headers`: Retrieves the headers of the csv or xlsx file

##### `/fullcol/{HeaderName}`: Retrieves all the data in a specific column

##### `/fullrow/{Index}`: Retrieves all the data in a specific row

##### `/fullrows/{Index}`: Retrieves all the data up to a specific row

##### `/allrows`: Gives back all rows

##### `/item/{HeaderName}/{Index}`: Retrieves a specific cell item from the dataset

##### `/count`: Retrieves the count of records in the dataset

### Example Usage

Suppose you have an xlsx file named `example.xlsx` and you want to retrieve the headers of the file. You can use the following endpoint:

To load xlsx-data in the app you can use:

* GET http://127.0.0.1:8000/reload/xlsx?file=/Path/To/example.xlsx

To retrieve all headers, you can use:

* GET http://127.0.0.1:8000/headers

To retrieve a specific column say `Column A`, you can use:

* GET http://127.0.0.1:8000/fullcol/Column%20A or simply GET http://127.0.0.1:8000/fullcol/Column A

### Return Format

The API returns data in JSON format. The response will always be a JSON object, even if it contains a single value.

#### Response Structure
Each endpoint returns a JSON object with a content key that contains the requested data. For example:
```
{ "content": [the content] }
```

### Error Handling

If an error occurs, the API returns a JSON object with an error key that contains a detailed message describing the problem. For example:
```
{ "error": "No file loaded, please use /reload/xlsx or /reload/csv" }
```

**NOTE**: Everything not existing or related to any kind of error should print a default error message `Internal Server Error`.

### Limitations!

Currently there is **no** way to push/edit/change data in a file that is selected, this is purely read-only. It is basically one-way, I may add write-capabilities.

### Example Files

Simpel files which can be used to test the whole thing out, just visit these nice pages which serve example files:

* CSV: https://support.staffbase.com/hc/en-us/articles/360007108391-CSV-File-Examples
* XLSX: https://file-examples.com/index.php/sample-documents-download/sample-xls-download/

### License

Sheet2Api is licensed under the GNU General Public License v3.0.
You can read the full license details of the GNU General Public License v3.0 [here](https://choosealicense.com/licenses/gpl-3.0/)