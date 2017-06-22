#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 09/11/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, updates Android app config data in VAMS.

This script assumes it is being run from the root of the code directory.
"""
import requests
import sys
import os
import subprocess
import vams_common as vams
import colorcodes as ccodes
from xml.etree import ElementTree

# Supress compiled files
sys.dont_write_bytecode = True

_VAMS_POST_ENDPOINT = '/api/app/update_android_config_data'
_VAMS_GET_ENDPOINT = '/api/app/app_by_build_name'
_CONSOLE_OUTPUT = False


def BackfillConfigData(config_folder):
    """
    Sweeps through config folder and parses the config.xml file

    """
    print config_folder
    _WORKING_DIRECTORY = '%s/%s' % (vams._DEFAULT_CONFIG_DIRECTORY, config_folder)
    config_file = '%s/%s' % (_WORKING_DIRECTORY, 'config.xml')
    if os.path.isfile(config_file):
        print 'Parsing Configuration Data for %s' % config_folder
        ParseAppConfig(config_folder, config_file)
    else:
        print ccodes.ColorCodes.FAIL + 'No Config Exists' + ccodes.ColorCodes.ENDC

    print ''


def ParseAppConfig(config_folder, config_file):
    """
    Parses a xml file that is passed in and posts it's contents to VAMS

    :param config_folder:
        The name of the folder associated with the app config data to parse

    :param config_file:
        The full path to the config.xml file to parse
    """

    app_data = ElementTree.parse(config_file).getroot()
    post_data = PackageData(app_data)
    PostToVams(config_folder, post_data)


def PostToVams(app_name, postData):
    """
    Posts app data to VAMS

    :param app_name:
        Folder name of config data

    :param postData:
        Dictionary of app values to post to VAMS
    """

    print 'Using host: %s' % _DEFAULT_HOST

    app_id = RetrieveAppData(app_name)
    if app_id == 0:
        print 'No app with a build name of \'%s\' was found in VAMS' % app_name
        return 1

    # Add app id to app update object
    postData['app_id'] = app_id

    print 'Posting to VAMS...'

    uri = '%s/%s' % (_VAMS_POST_ENDPOINT, app_name)
    url = '%s%s' % (_DEFAULT_HOST, uri)
    date = vams.createDateString()
    req_hash = vams.calcAuthHash(uri, 'POST', date)

    auth_header = 'BASIC %s:%s' % (vams._DEFAULT_VAMS_USERID, req_hash)
    headers = {
        'Authorization': auth_header,
        'User-Agent': vams._DEFAULT_USERAGENT,
        'Date': date
    }
    response = requests.post(url, data=postData, headers=headers)

    json = response.json()
    error_code = json['error']

    if not error_code == 0:
        print 'An error occurred posting config data to VAMS for %s' % app_name
        print json['message']
    else:
        print 'Config data posted successfully to VAMS for %s' % app_name


def RetrieveAppData(build_name):
    """
    Retrieve the app details from VAMS

    :param build_name:
        The folder / build_name of the app to retrieve from VAMS

    :return:
        Integer value associated with the app id of the specified app (returns 0 if app is not found)
    """

    # Calculate request hash
    uri = '%s/%s' % (_VAMS_GET_ENDPOINT, build_name)
    url = '%s%s' % (_DEFAULT_HOST, uri)
    date = createDateString()
    req_hash = vams.calcAuthHash(uri, 'GET', date)

    auth_header = 'BASIC %s:%s' % (vams._DEFAULT_VAMS_USERID, req_hash)
    headers = {
        'Authorization': auth_header,
        'User-Agent': vams._DEFAULT_USERAGENT,
        'Date': date
    }
    response = requests.get(url, headers=headers)
    json = response.json()
    error_code = json['error']

    if not error_code == 0:
        print 'An error occurred posting config data for app: %s' % build_name
        print json['message']
        return 0

    payload = json['payload']
    app_id = payload['app_id']

    return app_id


def PackageData(app_data):
    """
    Stuffs app data into a dictionary

    :param resource:
        The XML node to parse through for app values

    :return:
        A dictionary of key / value pairs
    """

    search_pattern = './/string[@name="%s"]'
    build_qa_id = app_data.find(search_pattern % 'qa_app_id').text
    build_staging_id = app_data.find(search_pattern % 'staging_app_id').text
    build_prod_id = app_data.find(search_pattern % 'prod_app_id').text
    gcm_project_number = app_data.find(search_pattern % 'gcm_project_number').text
    google_play_key = app_data.find(search_pattern % 'google_play_key').text

    if build_qa_id is None:
        build_qa_id = 1

    if build_staging_id is None:
        build_staging_id = 1

    if build_prod_id is None:
        build_prod_id = 1

    postData = {
        'build_qa_id': build_qa_id,
        'build_staging_id': build_staging_id,
        'build_prod_id': build_prod_id,
        'gcm_project_number': gcm_project_number,
        'google_play_key': google_play_key
    }

    return postData



def CleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def ShowProperUsage():
    print ''
    print 'Updates a list of currently active apps in VAMS'
    print 'Usage: ./backfill.py <app_folder> <environment>'
    print ''
    print '<app_folder>: Is the name of the app folder config environment to retrieve the application data from.'
    print '<environment> OPTIONAL: Is the server environment to retrieve the application data from.'
    print '<environment> choices are: dev, qa, staging, production or localhost'
    print ''
    print 'NOTE: '
    print 'If no <environment> parameter is provided, the script will use DEV.'
    print ''
    print 'examples:'
    print './backfill.py RyanHiga         <-- will use PRODUCTION'
    print './backfill.py RyanHiga qa      <-- will use QA'
    print './backfill.py        <-- Displays this help screen'
    print './backfill.py h      <-- Displays this help screen'
    print './backfill.py help   <-- Displays this help screen'

    sys.exit(1)


def main(argv):

    vams.init()

    if len(argv) == 1:
        ShowProperUsage()
    else:
        if argv[1] == 'h' or argv[1] == 'help':
            ShowProperUsage()
        else:
            app_folder = argv[1]
            if len(argv) == 3:
                server = argv[2]
            else:
                server = 'dev'

    global _DEFAULT_HOST
    _DEFAULT_HOST = vams.GetVictoriousHost(server)

    if vams.authenticateUser(_DEFAULT_HOST):
        BackfillConfigData(app_folder)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    CleanUp()
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
