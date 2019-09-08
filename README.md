# XtractHub File Service
XtractHub File Service is a user metadata file service based on [XtractHub](https://github.com/xtracthub)
from Globus Labs. XtractHub File Service allows users to manage files, process metadata from uploaded files using 
XtractHub, and view extracted file metadata using a REST API.

## Getting Started
These instructions will get a copy of XtractHub File Service running on your local machine for development and testing 
purposes.

### Prerequisites
- Redis (available [here](https://redis.io/download))
- Docker (available [here](https://docs.docker.com/install/))

### Installation
First, clone this repository and activate a virtual environment:
```
git clone https://github.com/rewong03/xtract_file_service
cd xtract_file_service
python3 -m venv venv
source venv/bin/activate
```
Next, install the requirements:
```
pip install -r requirements.txt
deactivate
```

### Running XtractHub File Service
First, open a terminal and start a redis server:
```
cd /path/to/redis/
src/redis-server
```
Then in a second terminal, start a celery worker:
```
cd /path/to/xtract_file_service/
source venv/bin/activate
venv/bin/celery -A app.celery_app worker -Q celery,priority
```
In a third terminal, start the flask app:
```
cd /path/to/xtract_file_service
source venv/bin/activate
venv/bin/flask run
```

## Interacting with the server
The server is a REST API with no GUI or HTML. All interactions are done using `curl` or the xtract_file_service command
line interface. This section is documentation of how to interact with all of the server's features with `curl`.  


**While you *can* use `curl` to interact with the server, it is recommended that you use the xtract_file_service CLI 
instead. To learn how to use the CLI, click [here](xfs_cli/README.md).**

### Creating a user:
To create a new user, run:
```
curl -X POST -d '{"Username": "your_username", "Email": "your_email", "Password": "your_password"}' http://localhost:5000
```
- This will either return a success message, or a failure message if your input wasn't formatted correctly or if the 
username has already been taken.

### Logging in:
To login, run:
```
curl -X GET -d '{"Username": "your_username", "Password": "your_password"}' http://localhost:5000/login
```
- This will return a user ID that will become your `"Authentication"` for other server interactions. Save or copy this 
so you won't have to login again.

### Deleting an account:
To delete an account, run:
```
curl -X DELETE -H "Authentication: your_authentication" -d '{"Username": "your_username", "Password": "your_password"}' http://localhost:5000/delete_user
```

### Viewing, uploading, and deleting files:
To upload files for automatic metadata processing, run:
```
curl -X POST -H "Authentication: your_authentication" -H "Extractor: extractor_name" -F "file=@/local/file/path.txt" http://localhost:5000/files
```
- **Note: See the available extractors section below.**  
- This will return a task ID for the metadata processing job, which can be used to view the status of your job. Omitting
`extractor_name` will still return a task ID but will not result in any metadata being processed.
- Compressed files will be automatically be decompressed. 

To view uploaded files, run:
```
curl -X GET -H "Authentication: your_authentication" http://localhost:5000/files
```
- This will return a string containing the names of uploaded files as well as their size.

To delete files, run:
```
curl -X DELETE -H "Authentication: your_authentication" -d filename http://localhost:5000/files
```
- This will return a success message or an error message if the file doesn't exist.

### Viewing, processing, and deleting metadata:
To view processed metadata, run:
```
curl -X GET -H "Authentication: your_authentication" -d filename http://localhost:5000/metadata
```
- This will return all metadata extracted for a given file.

To process metadata for an uploaded file, run:
```
curl -X POST -H "Authentication: your_authentication" -d '{"Filename": "filename", "Extractor": "extractor_name"}' http://localhost:5000/metadata
```
- **Note: See the available extractors section below.**  
- **Note: You cannot process metadata for a file and extractor if you have already done so for that file and extractor
combination.**
- This will return a task ID for the metadata processing job, which can be used to view the status of your job. 
Omitting `extractor_name` will still return a task ID but will not result in any metadata being processed.

To delete all metadata for a file, run:
```
curl -X DELETE -H "Authentication: your_authentication" -d filename http://localhost:5000/metadata
```
- An additional `-H "Extractor: extractor` header can be passed to specify extractor metadata to delete for `filename`. 
If omitted, all metadata for `filename` will be deleted.

### Viewing task status:
To view a task status, run:
```
curl -X GET -d task_id http://localhost:5000/tasks
```
- This returns a status message for the given task ID. 

## Available Extractors:
`tabular`:
- Can process tabular/columnar files (.tsv, .csv, etc.).
- Returns preamble, headers, and means, medians, modes, max, min for each column. 
    - Tabular files containing preamble will automatically process the preamble using the
    `keyword` extractor. 

`keyword`:
- Can process text files.
- Returns a list of keywords as well as scores for those keywords (calculated using (degree)/(frequency)).

`jsonxml`:
- Can process .json/.xml style files.
- Returns depth, headers, columns, and all text found in the file.
    - Json/xml files containing text will automatically process the text using the `keyword`
    extractor. 

`netcdf`:
- Can process netcdf style files.
- Returns attributes, dimensions, size, and variables.

`image`:
- Can process any image file.
- Returns a classification of plot, map, map-plot, graphic, or photograph.

`map`:
- Can process a map image (works better for maps with text or coordinates).
- Returns any text found from the image as well as locations on the map.

`matio`:
- Can process material science files.
- `matio` was built using the [MaterialsIO](https://github.com/materials-data-facility/MaterialsIO) library. For a more
extensive list of accepted file types and outputs, please visit their [documentation](https://materialsio.readthedocs.io/en/latest/parsers.html).
