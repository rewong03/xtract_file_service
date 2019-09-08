# XtractHub File Service CLI
`xfs` CLI is a command line interface for interacting with the XtractHub File Service server.

## Getting Started
These instructions will get a copy of the `xfs` CLI running on your local machine for development and testing 
purposes.

## Prerequisites
- XtractHub File Service Server (found [here](https://github.com/rewong03/xtract_file_service))

## Installation
First, clone the repository and `cd` into the `xfs_cli` folder:
```
git clone https://github.com/rewong03/xtract_file_service
cd xtract_file_service/xfs_cli
``` 

Then pip install the folder:
```
pip install --editable .
```

## CLI Commands
This section is documentation for how to use the `xfs` CLI.

### Configuring the CLI
To configure the CLI, run:
```
xfs config --url xfs_url
```
- `xfs_url` is the url that your XtractHub File Service server is running on.
- **By default this is set to `http://localhost:5000`.**

### Creating a user:
To create a new user, run:
```
xfs create-user
```
- This will prompt you to enter a username, email and password.

### Logging in
To login to your XtractHub FIle Service account, run:
```
xfs login 
```
- This will prompt you to enter your username and password.
- Your username and the authentication returned from the server will be saved. If you login with another account, you 
will be prompted to override the existing credentials.

### Deleting an account:
To delete an account, run:
```
xfs delete-user
```
- This will prompt you to provide credentials and confirm that you wish to delete a user.
- **You must first login before deleting your account.**

### Viewing, uploading, and deleting files:
To upload files for automatic metadata processing, run:
```
xfs upload-files --extractor extractor_name
```
- This will return a task ID for the metadata processing job, which can be used to view the status of your job. Omitting
`extractor_name` will still return a task ID but will not result in any metadata being processed.
- Compressed files will be automatically be decompressed. 

To view uploaded files, run:
```
xfs view-files
```
- This will return a string containing the names of uploaded files as well as their size.

To delete files, run:
```
xfs delete-files file_name
```
- This will return a success message or an error message if the file doesn't exist.

### Viewing, processing, and deleting metadata:
To view processed metadata, run:
```
xfs view-metadata file_name
```
- This will return all metadata extracted for file_name.

To process metadata for an uploaded file, run:
```
xfs extract-metadata file_name extractor
```
- **Note: You cannot process metadata for a file and extractor if you have already done so for that file and extractor
combination.**
- This will return a task ID for the metadata processing job, which can be used to view the status of your job. 

To delete all metadata for a file, run:
```
xfs delete-metadata file_name
```
- An additional `--extractor extractor` can be passed to specify extractor metadata to delete for `file_name`. 
If omitted, all metadata for `file_name` will be deleted.

### Viewing task status:
To view a task status, run:
```
xfs task-status task_id
```
- This returns a status message for the given task ID. 

