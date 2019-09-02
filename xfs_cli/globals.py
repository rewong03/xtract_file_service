import json
import os

"""Handles the global variables for xtract_file_service_cli.py"""

globals_json = None
xfs_url = None
xfs_auth = None


def setup():
    """Reads the global variables from xfs_globals.json or creates a xfs_globals.json file
    if it doesn't exist.
    """
    global globals_json
    global xfs_url
    global xfs_auth
    if os.path.exists('xfs_globals.json'):
        with open('xfs_globals.json') as f:
            globals_json = json.load(f)
        xfs_url = globals_json['xfs_url']
        xfs_auth = globals_json['xfs_auth']
    else:
        with open('xfs_globals.json', 'w') as f:
            json_to_dump = {"xfs_url": "http://localhost:5000",
                            "xfs_auth": {"username": None, "auth": None}}
            json.dump(json_to_dump, f)
            xfs_url = "http://localhost:5000"
            xfs_auth = {"username": None, "auth": None}


def change_xfs_url(url):
    """Changes the 'xfs_url' value in xfs_globals.json.

    Parameter:
    url (str): New 'xfs_url' value to save to xfs_globals.json.
    """
    globals_json['xfs_url'] = url
    with open('xfs_globals.json', 'w') as f:
        json.dump(globals_json, f)


def change_xfs_auth(auth_dict):
    """Changes the 'xfs_auth' value in xfs_globals.json.

    Parameter:
    auth_dict (dict): New 'xfs_auth' dictionary in format
    {"username": "", "auth": ""} to save to xfs_globals.json.
    """
    globals_json['xfs_auth'] = auth_dict
    with open('xfs_globals.json', 'w') as f:
        json.dump(globals_json, f)


setup()