#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 07/01/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, retrieves the latest app configuration data,
app assets and writes them to a temporary directory.

This script assumes it is being run from the root of the code directory.

This script is used by the following Victorious repositories:
https://github.com/Victorious/VictoriousAndroid
https://github.com/Victorious/VictoriousiOS

NOTE: Because this script returns a folder string for iOS, CONSOLE_OUTPUT for this script is isolated to Android only.
"""
import requests
import sys
import subprocess
import shutil
import os
import tempfile
import vams_common as vams

# Supress compiled files
sys.dont_write_bytecode = True

_ASSETS_ENDPOINT = '/api/app/appassets_by_build_name'
_DEFAULT_HOST = ''

_WORKING_DIRECTORY = ''

_CONSOLE_OUTPUT = False


def proccessAppAssets(app_name, json):
    """
    Processes the app design assets for a given platform.

    :param json:
        JSON object of app assets to process

    """

    payload = json['payload']
    app_title = payload['app_title']

    assets = payload['assets']
    platform_assets = assets[vams._DEFAULT_PLATFORM]

    current_cnt = 0

    global _WORKING_DIRECTORY

    if vams._DEFAULT_PLATFORM == vams._PLATFORM_ANDROID:
        _WORKING_DIRECTORY = '%s/%s' % (vams._DEFAULT_CONFIG_DIRECTORY, app_name)

    if not os.path.exists(_WORKING_DIRECTORY):
        os.makedirs(_WORKING_DIRECTORY)


    if _CONSOLE_OUTPUT:
        print '\nUsing Directory: %s' % _WORKING_DIRECTORY
        print u'\nDownloading the Most Recent Art Assets for %s...' % app_title

    for asset in platform_assets:

        if not platform_assets[asset] == None:
            img_url = platform_assets[asset]
            asset_name = asset.replace('_', '-')
            new_file = '%s/%s.png' % (_WORKING_DIRECTORY, asset_name)

            if _CONSOLE_OUTPUT:
                print '%s (%s)' % (asset_name, platform_assets[asset])

            vams.assetFetcher(img_url, new_file)

            current_cnt = current_cnt+1

    if _CONSOLE_OUTPUT:
        print '\n%s images downloaded' % current_cnt
        print ''

    # Now set the app config data
    setAppConfig(app_name, json)


def retrieveAppDetails(app_name):
    """
    Collects all of the design assets for a given app

    :param app_name:
        The app name of the app whose assets to be downloaded.

    :return:
        0 = Success
        1 = Error
    """

    # Calculate request hash
    uri = '%s/%s' % (_ASSETS_ENDPOINT, app_name)
    url = '%s%s' % (_DEFAULT_HOST, uri)
    date = vams.createDateString()
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

    if error_code == 0:
        proccessAppAssets(app_name, json)

    else:
        response_message = (
                'Backend failed retrieving data for %s with error code "%s" and message: "%s"' %
                (app_name, error_code, json['message']))
        if _CONSOLE_OUTPUT:
            print response_message

        cleanUp()

        if vams._DEFAULT_PLATFORM == vams._PLATFORM_IOS:
            shutil.rmtree(_WORKING_DIRECTORY)
            sys.exit('1|%s' % response_message)

        sys.exit(1)


def setAppConfig(app_name, json_obj):
    """
    Parses a JSON object for app configuration data and writes it out to
    an app configuration file

    :param app_name:
        The app to generate config data for

    :param json_obj:
        The JSON object to parse that contains the app configuration data
    """
    payload = json_obj['payload']
    app_config = payload['configuration'][vams._DEFAULT_PLATFORM]
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_ANDROID:
        app_config = payload['configuration'][vams._DEFAULT_PLATFORM]['config']

    app_title = payload['app_title']
    app_title = app_title.replace(' ','')

    file_name = 'config.xml'
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_IOS:
        file_name = 'Info.plist'
    config_file = '%s/%s' % (_WORKING_DIRECTORY, file_name)

    if _CONSOLE_OUTPUT:
        print u'Applying Most Recent App Configuration Data to %s' % app_title
        print ''
        # Uncomment out the following line to display the retrieved config data
        print app_config.encode('utf-8')

    # Write config file to disk
    f = open(config_file, 'w')
    f.write(app_config.encode('utf-8').strip())
    f.close()

    # Download any additional platform-specific app data
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_ANDROID:
        downloadKeystoreFile(app_name, payload['configuration'][vams._PLATFORM_ANDROID])

    if vams._DEFAULT_PLATFORM == vams._PLATFORM_IOS:
        downloadProvisioningProfiles(payload['provisioning_profiles'])

    # Clean-up compiled python files off the disk
    cleanUp()

    if _CONSOLE_OUTPUT:
        print 'Configuration and assets downloaded successfully!'
        print ''



def downloadProvisioningProfiles(json):
    """
    Downloads the Staging Provisioning Profile from VAMS and writes it to a local location.

    :param json:
        The json object containing the provisioning profile assets
    """

    staging_proifle_url = json['staging']
    if staging_proifle_url:
        if _CONSOLE_OUTPUT:
            print 'Downloading Staging Provisioning Profile...'
        staging_profile = '%s/%s' % (_WORKING_DIRECTORY, vams._STAGING_PROVISIONING_PROFILE)
        vams.assetFetcher(staging_proifle_url, staging_profile)


def downloadKeystoreFile(app_build_name, json):
    """
    Downloads the Android keystore file for a given app and writes it to local location
    :param app_build_name:
        The short name of the app to download the keystore file for. (old folder name)

    :param json:
        The json object containing the keystore file asset
    :return:
    """

    keystore_url = json['keystore']
    if keystore_url:
        new_file = '%s.keystore' % app_build_name

        if _CONSOLE_OUTPUT:
            print 'Downloading %s keystore file' % new_file
            print ''

        keystore_file = '%s/%s' % (_WORKING_DIRECTORY, new_file)
        vams.assetFetcher(keystore_url, keystore_file)


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def showProperUsage():
        print ''
        print 'Usage: ./vams_prebuild.py <app_name> <platform> <environment> <port>'
        print ''
        print '<app_name> is the name of the application data to retrieve from VAMS.'
        print '<config_path> is the path on disk where the application data is to be written to.'
        print '<platform> is the OS platform for which the assets need to be downloaded for. Choices = android OR ios'
        print '<environment> OPTIONAL: Is the server environment to retrieve the application data from.'
        print '<port> OPTIONAL: Will only be used if <environment> is set to local'
        print ''
        print 'NOTES: '
        print '* If no <platform> parameter is provided, the script will assume ANDROID.'
        print '* If no <environment> parameter is provided, the script will use PRODUCTION.'
        print ''
        print 'examples:'
        print './vams_prebuild.py awesomeness ios     <-- will use PRODUCTION'
        print '  -- OR --'
        print './vams_prebuild.py awesomeness ios staging  <-- will use STAGING'
        print ''
        sys.exit(1)


def main(argv):
    if len(argv) < 3:
        showProperUsage()

    vams.init()

    app_name = argv[1]

    global _WORKING_DIRECTORY
    _WORKING_DIRECTORY = vams._DEFAULT_CONFIG_DIRECTORY

    platform = argv[2]
    if platform == vams._PLATFORM_IOS:
        vams._DEFAULT_PLATFORM = vams._PLATFORM_IOS
        app_path = tempfile.mkdtemp()
        _WORKING_DIRECTORY = app_path


    if len(argv) == 4:
        server = argv[3]
    else:
        server = ''

    if len(argv) == 5:
        vams._DEFAULT_LOCAL_PORT = argv[4]

    global _DEFAULT_HOST
    _DEFAULT_HOST = vams.GetVictoriousHost(server)

    global _CONSOLE_OUTPUT
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_ANDROID:
        _CONSOLE_OUTPUT = True


    # Uncomment the following twolines to display the host being accessed
    if _CONSOLE_OUTPUT:
        print 'Using host: %s' % _DEFAULT_HOST

    if vams.authenticateUser(_DEFAULT_HOST):
        retrieveAppDetails(app_name)
    else:
        exit_message = 'There was a problem authenticating with the Victorious backend. Exiting now...'
        if _CONSOLE_OUTPUT:
            print exit_message

        error_string = '1|%s' % exit_message
        sys.exit(error_string)

    response_message = 'App Data & Assets Downloaded from VAMS Successfully'
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_IOS:
        response_message = '0|%s' % _WORKING_DIRECTORY
        sys.exit(response_message)
    elif vams._DEFAULT_PLATFORM == vams._PLATFORM_ANDROID:
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
