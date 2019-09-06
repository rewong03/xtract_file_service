from globals import change_xfs_url, change_xfs_auth, xfs_url, xfs_auth
import json
import os
import click
import requests


@click.command(help='Configure the url of xtract_file_service')
@click.option('--url', default=xfs_url, show_default=True,
              help='URL for xtract_file_service')
def config(url):
    """Configures the url for xtract_file_service.

    Parameter:
    url (str): Default to configure the url to, default is http://localhost:5000.
    """
    global xfs_url

    if xfs_url is None:
        xfs_url = url
        change_xfs_url(url)
        click.echo('Successfully changed the url')
    elif xfs_url == url:
        click.echo('The url is already set to {}'.format(url))
    else:
        if click.confirm('The url {} is already set, do you want to change it?'.format(xfs_url)):
            xfs_url = url
            change_xfs_url(url)
            click.echo('Successfully changed the url')
        else:
            click.echo('Did not change the url')


@click.command(help='Login to your xtract_file_service account')
@click.option('--username', prompt=True, help='Username for your xtract_file_service account')
@click.password_option('--password', help='Password for your xtract_file_service account')
def login(username, password):
    """Logs in a user to xtract_file_service and remembers their authentiation value.

    Parameters:
    username (str): Username for xtract_file_service account.
    password (str): Password for xtract_file_serviece account.
    """
    url = xfs_url + "/login"
    payload = json.dumps({"Username": username, "Password": password})
    response = requests.get(url, data=payload).text.rstrip()
    response = response[-36:] # We only want the UUID returned in the response

    if response == "Incorrect login\n":
        click.echo(response)
    elif not(response == xfs_auth['auth']) and xfs_auth['auth'] is not None:
        if click.confirm("User with username {}'s authentication has already been "
                         "saved, do you want to overwrite it?".format(xfs_auth['username'])):
            change_xfs_auth({"username": username, "auth": response})
            click.echo("Successfully logged in, authentication for {} has been saved".format(username))
        else:
            click.echo("Authentication was not saved")

    else:
        change_xfs_auth({"username": username, "auth": response})
        click.echo("Successfully logged in, authentication for {} has been saved".format(username))


@click.command(help='Create a new user')
@click.option('--username', prompt=True, help='Username for your xtract_file_service account')
@click.option('--email', prompt=True, help='Email for your xtract_file_service account')
@click.password_option('--password', help='Password for your xtract_file_service account')
def create_user(username, email, password):
    """Creates a new user account.

    Parameters:
    username (str): Username for your xtract_file_service account
    email (str): Email for your xtract_file_service account
    password (str): Password for your xtract_file_service account
    """
    url = xfs_url + "/create_user"
    payload = json.dumps({"Username": username, "Email": email, "Password": password})
    response = requests.post(url, data=payload).text
    click.echo(response)


@click.command(help='Deletes a user')
@click.option('--username', prompt=True, help='Username of user to delete')
@click.password_option('--password', help='Password of user to delete')
def delete_user(username, password):
    """Deletes a user account.

    Parameters:
    username (str): Username of user to delete
    password (str): Password of user to delete
    """
    url = xfs_url + "/delete_user"
    payload = json.dumps({"Username": username, "Password": password})
    auth_header = {"Authentication": xfs_auth["auth"]}

    if click.confirm("This will delete all user metadata and files, do you want to proceed?"):
        response = requests.delete(url, data=payload, headers=auth_header).text
        if response == "Authentication does not match credentials\n":
            click.echo("Login before attempting to delete user")
        else:
            click.echo(response)
    else:
        click.echo("User was not deleted")


@click.command(help='View a user\'s files')
def view_files():
    """Returns user files and file sizes."""
    url = xfs_url + "/files"
    auth_header = {"Authentication": xfs_auth["auth"]}
    response = requests.get(url, headers=auth_header).text
    click.echo(response)


@click.command(help='Uploads files to a user\'s account')
@click.argument('file_path')
@click.option('--extractor', help="Extractor to user to process file_path", default=None)
def upload_files(file_path, extractor):
    """Uploads files to a user's account.

    Parameters:
    file_path (str): Local file path of file to upload.
    extractor (str): Extractor to use to extract metadata from file.
    """
    url = xfs_url + "/files"
    headers = {"Authentication": xfs_auth["auth"]}

    if extractor is not None:
        headers.update({"Extractor": extractor})

    if os.path.isfile(file_path):
        files = {"file": open(file_path, 'rb')}
        response = requests.post(url, headers=headers, files=files).text
        click.echo(response)
    else:
        click.echo("Path does not exist")


@click.command(help='Delete files from a user\'s account')
@click.argument('file_name')
def delete_files(file_name):
    """Deletes a file from a user's account.

    Parameter:
    file_name (str): Name/path of file to delete.
    """
    url = xfs_url + "/files"
    auth_header = {"Authentication": xfs_auth["auth"]}
    response = requests.delete(url, headers=auth_header, data=file_name).text
    click.echo(response)


@click.command(help='View a user\'s file metadata')
@click.argument('file_name')
def view_metadata(file_name):
    """Returns user metadata.

    Parameter:
    file_name (str): Name/path of file to view metadata for.
    """
    url = xfs_url + "/metadata"
    auth_header = {"Authentication": xfs_auth["auth"]}
    response = requests.get(url, headers=auth_header, data=file_name).text
    click.echo(response)


@click.command(help='Submits a metadata extraction task')
@click.argument('file_name')
@click.argument('extractor')
def extract_metadata(file_name, extractor):
    """Extracts metadata from a file.

    Parameters:
    file_name (str): Name/path of file to extract metadata from.
    extractor (str): Name of extractor to use to extract metadata.

    Return:
    (str): Returns a string containing a task id.
    """
    url = xfs_url + "/metadata"
    auth_header = {"Authentication": xfs_auth["auth"]}
    payload = json.dumps({"Filename": file_name, "Extractor": extractor})
    response = requests.post(url, headers=auth_header, data=payload).text
    click.echo(response)


@click.command(help='Deletes user metadata')
@click.argument('file_name')
@click.option('--extractor', default=None,
              help='Specific extractor metadata to delete for file_name')
def delete_metadata(file_name, extractor):
    """Delete file metadata.

    file_name (str): Name/path of file to delete metadata for.
    extractor (str): Name of specific extractor metadata to delete for file_name.
    """
    url = xfs_url + "/metadata"
    headers = {"Authentication": xfs_auth["auth"], "Extractor": extractor}
    if extractor is None:
        confirm_message = "This will delete all metadata for {}. " \
                          "Do you wish to continue?".format(file_name)
    else:
        confirm_message = "This will delete {} metadata for {}. " \
                          "Do you wish to continue?".format(extractor, file_name)
    if click.confirm(confirm_message):
        response = requests.delete(url, headers=headers, data=file_name).text
        click.echo(response)
    else:
        click.echo("Metadata for {} was not deleted".format(file_name))


@click.command(help='View metadata extraction status')
@click.argument('task_id')
def task_status(task_id):
    """Returns the status of a metadata extraction task.

    Parameter:
    task_id (str): Task ID of metadata extraction task.
    """
    url = xfs_url + "/tasks"
    response = requests.get(url, data=task_id).text
    click.echo(response)


@click.group()
def xfs_cli():
    pass


xfs_cli.add_command(config)
xfs_cli.add_command(login)
xfs_cli.add_command(create_user)
xfs_cli.add_command(delete_user)
xfs_cli.add_command(upload_files)
xfs_cli.add_command(view_files)
xfs_cli.add_command(delete_files)
xfs_cli.add_command(view_metadata)
xfs_cli.add_command(extract_metadata)
xfs_cli.add_command(delete_metadata)
xfs_cli.add_command(task_status)
