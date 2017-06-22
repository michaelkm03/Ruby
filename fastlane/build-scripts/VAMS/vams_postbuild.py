#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 07/12/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Posts a Test Fairy build url for a specific app to the Victorious backend.

This script is used by the following Victorious repositories:
https://github.com/Victorious/VictoriousAndroid
https://github.com/Victorious/VictoriousiOS
"""

import requests
import sys
import subprocess
import vams_common as vams

# Supress compiled files
sys.dont_write_bytecode = True

_VICTORIOUS_ENDPOINT = '/api/app/update_testfairy_url'
_DEFAULT_HOST = ''
_CONSOLE_OUTPUT = False


def postTestFairyURL(app_name, testfairy_url):
    """
    Post Test Fairy url to Victorious backend

    :param app_name:
        The name of the app to upload the Test Fairy url for.

    :param testfairy_url:
        The Test Fairy url to send to the backend.

    :return:
        0 - For success
        1 - For error
    """

    # Calculate request hash
    uri = '%s/%s' % (_VICTORIOUS_ENDPOINT, app_name)
    url = '%s%s' % (_DEFAULT_HOST, uri)
    date = vams.createDateString()
    req_hash = vams.calcAuthHash(uri, 'POST', date)

    field_name = 'android_testfairy_url'
    if vams._DEFAULT_PLATFORM == vams._PLATFORM_IOS:
        field_name = 'ios_testfairy_url'

    auth_header = 'BASIC %s:%s' % (vams._DEFAULT_VAMS_USERID, req_hash)
    headers = {
        'Authorization': auth_header,
        'User-Agent': vams._DEFAULT_USERAGENT,
        'Date': date
    }
    postData = {
        'build_name': app_name,
        'name': field_name,
        'platform': vams._DEFAULT_PLATFORM,
        'value': testfairy_url
    }
    response = requests.post(url, data=postData, headers=headers)
    json = response.json()
    error_code = json['error']

    if error_code != 0:
        error_message = (
                'Error occurred posting the Test Fairy URL for %s: %s %s' %
                (app_name, error_code, json['message']))
        if _CONSOLE_OUTPUT:
            print error_message
        sys.exit('1|%s' % error_message)

    # Clean-up compiled python files
    cleanUp()

    if _CONSOLE_OUTPUT:
        print 'Test Fairy URL posted successfully for %s!' % app_name
        print ''


def cleanUp():
    subprocess.call("find . -name '*.pyc' -delete", shell=True)


def showProperUsage():
    print ''
    print 'Usage: ./vams_postbuild.py <app_name> <platform> <url> <environment> <port>'
    print ''
    print '<app_name> is the name of the application in VAMS that you want to post data to.'
    print '<platform> is the OS platform for which this data is applicable.'
    print '<url> is the Test Fairy project url to be sent to backend'
    print '<environment> OPTIONAL: Is the server environment to post the data to.'
    print '<port> OPTIONAL: Will only be used if <environment> is set to localhost'
    print ''
    print 'NOTE: If no <environment> parameter is provided, the system will use PRODUCTION.'
    print ''
    print 'examples:'
    print './vams_postbuild.py awesomenesstv ios http://my-url     <-- will use PRODUCTION'
    print '  -- OR --'
    print './vams_postbuild.py awesomenesstv ios http://my-url qa  <-- will use QA'
    print ''

def main(argv):

    global _CONSOLE_OUTPUT

    if len(argv) < 4:
        if _CONSOLE_OUTPUT:
            showProperUsage()
        exit_message = 'Wrong parameters were passed to vams_postbuild.py'
        sys.exit(exit_message)

    vams.init()


    app_name = argv[1]
    platform = argv[2]
    if platform == vams._PLATFORM_IOS:
        vams._DEFAULT_PLATFORM = vams._PLATFORM_IOS

    _CONSOLE_OUTPUT = False


    url = argv[3]

    if len(argv) == 5:
        server = argv[4]
    else:
        server = ''

    if len(argv) == 6:
        vams._DEFAULT_LOCAL_PORT = argv[5]

    global _DEFAULT_HOST
    _DEFAULT_HOST = vams.GetVictoriousHost(server)

    if _CONSOLE_OUTPUT:
        print ''
        print 'Using host: %s' % _DEFAULT_HOST
        print ''

    if vams.authenticateUser(_DEFAULT_HOST):
        postTestFairyURL(app_name, url)
    else:
        exit_message = 'There was a problem authenticating with the Victorious backend. Exiting now...'
        if _CONSOLE_OUTPUT:
            print exit_message
        sys.exit(exit_message)

    if _CONSOLE_OUTPUT:
        print '\nTest Fairy URL Posted to VAMS Successfully for %s\n' % app_name
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
