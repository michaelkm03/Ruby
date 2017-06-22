#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 09/08/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, retrieves a list of the current active apps in VAMS.

This script assumes it is being run from the root of the code directory.

This script is used by the following Victorious repositories:
https://github.com/Victorious/VictoriousiOS
"""
import os
import requests
import sys
import subprocess
import vams_common as vams
import colorcodes as ccodes

# Supress compiled files
sys.dont_write_bytecode = True

_APPLIST_ENDPOINT = '/api/app/apps_list'
_GOOGLE_PLAY_STORE_PREFIX = 'https://play.google.com/store/apps/details?id='


def retrieveGooglePlayVersion(google_play_id):
    """Retrieves the Google Play version by scraping it from the web.

    Returns:
        Version string or empty string if failure.
    """
    version = ''
    play_store_response = requests.get(_GOOGLE_PLAY_STORE_PREFIX + google_play_id).text
    version_start_tag = '<div class="content" itemprop="softwareVersion">'
    version_end_tag = '</div>'

    start = play_store_response.find(version_start_tag)
    if start != -1:
        end = play_store_response.find(version_end_tag, start)
        if end != -1:
            version = play_store_response[(start + len(version_start_tag)):end].strip()
    return version


def fetchAppList(server):
    """Retrieves the list of ACTIVE (Locked or Unlocked) apps from VAMS.

    Returns:
        List of app info on active apps.
    """

    # Calculate request hash
    url = '%s%s' % (_DEFAULT_HOST, _APPLIST_ENDPOINT)
    date = vams.createDateString()
    req_hash = vams.calcAuthHash(_APPLIST_ENDPOINT, 'GET', date)

    auth_header = 'BASIC %s:%s' % (vams._DEFAULT_VAMS_USERID, req_hash)

    headers = {
        'Authorization': auth_header,
        'User-Agent': vams._DEFAULT_USERAGENT,
        'Date': date
    }
    response = requests.get(url, headers=headers)
    json_obj = response.json()
    error_code = json_obj['error']

    if error_code == 0:
        app_count = 0
        print '\nVAMS Active Apps List'
        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'id   Build Name                              Name                                    Live Version (Google)    Status'
        print '-----------------------------------------------------------------------------------------------------------------------'
        payload = json_obj['payload']
        for app in payload:
            app_id = app['app_id']
            app_state = app['app_state'] if 'app_state' in app else ''
            app_name = app['app_name'] if 'app_name' in app else ''
            build_name = app['build_name'] if 'build_name' in app else ''
            google_play_id = app['google_play_id'] if 'google_play_id' in app else ''

            version = ''
            if google_play_id is not None and google_play_id != '':
                version = retrieveGooglePlayVersion(google_play_id)

            if app_state == vams._STATE_LOCKED:
                state = ccodes.ColorCodes.FAIL + app_state.upper() + ccodes.ColorCodes.ENDC
            elif app_state == vams._STATE_UNLOCKED:
                state = ccodes.ColorCodes.OKGREEN + app_state.upper() + ccodes.ColorCodes.ENDC
            else:
                state = ccodes.ColorCodes.OKBLUE + app_state.upper() + ccodes.ColorCodes.ENDC
            print u' '.join((ccodes.ColorCodes.HEADER + app_id.ljust(5) + ccodes.ColorCodes.ENDC,
                                             build_name.ljust(40), app_name.ljust(40), version.ljust(25),
                                             state)).encode('utf-8').strip()
            app_count = app_count + 1

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'Total of %s Apps\nEnvironment: %s\n' % (app_count, server.upper())

        return payload

    else:
        print 'No app data found. Uhh... obviously, something went wrong.'
        cleanUp()
        sys.exit(1)


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def showProperUsage():
        my_name = os.path.basename(__file__)
        print ''
        print 'Displays a list of currently active apps in VAMS'
        print 'Usage: ' + my_name + ' <environment>'
        print ''
        print '<environment> OPTIONAL: Is the server environment to retrieve the application data from.'
        print '<environment> choices are: dev, qa, staging, production or localhost'
        print ''
        print 'NOTE: '
        print 'If no <environment> parameter is provided, the script will use PRODUCTION.'
        print ''
        print 'examples:'
        print my_name + '      <-- will use PRODUCTION'
        print my_name + ' qa   <-- will use QA'
        print my_name + ' h    <-- Displays this help screen'
        print my_name + ' help <-- Displays this help screen'
        print ''
        print 'search:'
        print my_name + ' dev | grep \'Ryan\'    <-- Simple case-sensitive search'
        print my_name + ' dev | grep -i \'ryan\' <-- Simple case-insensitive search'
        print ''
        sys.exit(1)


def main(argv):

    vams.init()

    if len(argv) == 1:
        server = 'production'
    else:
        if argv[1] == 'h' or argv[1] == 'help':
            showProperUsage()
        else:
            server = argv[1]

    global _DEFAULT_HOST
    _DEFAULT_HOST = vams.GetVictoriousHost(server)

    if vams.authenticateUser(_DEFAULT_HOST):
        fetchAppList(server)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
