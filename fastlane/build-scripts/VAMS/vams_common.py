# --------------------
# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 07/13/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
A set of global variables to be shared and set between the vams_prebuild and vams_postbuild programs.

The Hash calculating code was "borrowed" from Frank Zhao (frank@getvictorious.com).
https://github.com/Victorious/TestAutomation/blob/master/backEndApiDriver.py
"""

import hashlib
import requests
import subprocess
import sys
import uuid

def init():
    # Supress compiled files
    sys.dont_write_bytecode = True

    global _LOGIN_ENDPOINT
    global _DEFAULT_CONFIG_DIRECTORY
    global _DEFAULT_DEST_DIRECTORY
    global _DEFAULT_VAMS_USERID
    global _DEFAULT_VAMS_USER
    global _DEFAULT_VAMS_PASSWORD
    global _DEBUG_VAMS_USER
    global _DEBUG_VAMS_PASSWORD
    global _DEBUG_USERAGENT
    global _DEFAULT_USERAGENT
    global _DEFAULT_HEADERS
    global _DEFAULT_PLATFORM
    global _PRODUCTION_HOST
    global _PRODUCTION_VAPI
    global _STAGING_HOST
    global _STAGING_VAPI
    global _DEV_HOST
    global _DEV_VAPI
    global _LOCAL_HOST
    global _DEFAULT_LOCAL_PORT
    global _AUTH_TOKEN
    global _PLATFORM_ANDROID
    global _PLATFORM_IOS
    global _STATE_ARCHIVED
    global _STATE_LOCKED
    global _STATE_UNLOCKED
    global _QA_PROVISIONING_PROFILE
    global _STAGING_PROVISIONING_PROFILE

    _LOGIN_ENDPOINT = '/api/login'

    _DEFAULT_CONFIG_DIRECTORY = 'app/configuration'
    _DEFAULT_DEST_DIRECTORY = 'victorious/AppSpecific'

    _DEFAULT_VAMS_USERID = 0
    _DEFAULT_VAMS_USER = 'autobuild@victorious.com'
    _DEFAULT_VAMS_PASSWORD = 'tGrg9qtxgdRBbbPwiRDNbRJkjwTxXFmEphCbdrdoePdoHdKs3m'
    _DEBUG_VAMS_USER = 'vicky@example.com'
    _DEBUG_VAMS_PASSWORD = 'abc123456'

    device_id = str(uuid.uuid4())
    _DEFAULT_USERAGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/43.0.2357.130 Safari/537.36 aid:11 uuid:%s build:1' % device_id)
    _DEBUG_USERAGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/43.0.2357.130 Safari/537.36 aid:1 uuid:%s build:1' % device_id)
    _DEFAULT_HEADERS = ''

    _PLATFORM_ANDROID = 'android'
    _PLATFORM_IOS = 'ios'

    _STATE_ARCHIVED = 'archived'
    _STATE_LOCKED = 'locked'
    _STATE_UNLOCKED = 'unlocked'

    _DEFAULT_PLATFORM = _PLATFORM_ANDROID
    _PRODUCTION_HOST = 'https://api.getvictorious.com'
    _PRODUCTION_VAPI = 'https://vapi.getvictorious.com'
    _STAGING_HOST = 'https://staging.getvictorious.com'
    _STAGING_VAPI = 'https://vapi-staging.getvictorious.com'
    _DEV_HOST = 'http://dev.getvictorious.com'
    _DEV_VAPI = 'https://vapi-dev.getvictorious.com'
    _LOCAL_HOST = 'http://localhost'
    _DEFAULT_LOCAL_PORT = '8887'

    _AUTH_TOKEN = ''

    _QA_PROVISIONING_PROFILE = 'qa.mobileprovision'
    _STAGING_PROVISIONING_PROFILE = 'staging.mobileprovision'


def createDateString():
    """
    Creates a date string

    :return:
        A date formatted string
    """

    date_obj = subprocess.Popen(['date'], stdout=subprocess.PIPE)
    date_list = date_obj.communicate()[0].split()

    return ' '.join(date_list)

def GetVictoriousVAPI(host):
    """
    Retrieves a VAPI host url

    :param host:
        The corresponding VAPI environment.

    :return:
        A string of a VAPI url

    """

    if host.lower() == 'dev':
        hostURL = _DEV_VAPI
    elif host.lower() == 'staging':
        hostURL = _STAGING_VAPI
    elif host.lower() == 'production':
        hostURL = _PRODUCTION_VAPI
    elif host.lower() == 'localhost':
        hostURL = "%s:%s" % (_LOCAL_HOST, _DEFAULT_LOCAL_PORT)
    elif host.lower() == 'local':
        hostURL = "%s:%s" % (_LOCAL_HOST, _DEFAULT_LOCAL_PORT)
    else:
        hostURL = _PRODUCTION_VAPI

    return hostURL

def GetVictoriousHost(host):
    """
    Retrieves a Victorious host url

    :param host:
        The environment to retrieve the Victorious host url for

    :return:
        A string of a Victorious host url
    """

    if host.lower() == 'dev':
        hostURL = _DEV_HOST
    elif host.lower() == 'staging':
        hostURL = _STAGING_HOST
    elif host.lower() == 'production':
        hostURL = _PRODUCTION_HOST
    elif host.lower() == 'localhost':
        hostURL = "%s:%s" % (_LOCAL_HOST, _DEFAULT_LOCAL_PORT)
    elif host.lower() == 'local':
        hostURL = "%s:%s" % (_LOCAL_HOST, _DEFAULT_LOCAL_PORT)
    else:
        hostURL = _PRODUCTION_HOST

    return hostURL

def authenticateUser(host):
    """
    Authenticates a user against the Victorious backend API.

    :return:
        A JSON object of details returned by the Victorious backend API.
    """
    url = '%s%s' % (host, _LOGIN_ENDPOINT)

    global _DEFAULT_USERAGENT

    email = _DEFAULT_VAMS_USER
    pwd = _DEFAULT_VAMS_PASSWORD
    useragent = _DEFAULT_USERAGENT

    if host != _PRODUCTION_HOST:
        email = _DEBUG_VAMS_USER
        pwd = _DEBUG_VAMS_PASSWORD
        useragent = _DEBUG_USERAGENT
        _DEFAULT_USERAGENT = _DEBUG_USERAGENT

    postData = {
        'email': email,
        'password': pwd
    }
    headers = {
        'User-Agent': useragent,
        'Date': createDateString()
    }
    response = requests.post(url, data=postData, headers=headers)
    json = response.json()
    error_code = json['error']
    status_code = response.status_code

    if not (error_code == 0 and status_code == 200):
        return False

    # Return the authentication JSON object
    setAuthenticationToken(json)

    return True


def setAuthenticationToken(json_object):
    """
    Checks to see if there is a user token in the JSON response object
    of a login call. If there is, the script stores it in the global
    variable

    :param json_object:
        The response object from a authentication call. (May be blank.)

    :return:
        Nothing - If token object exists in JSON payload, then it is saved
        to a global variable.
    """
    global _AUTH_TOKEN
    global _DEFAULT_VAMS_USERID

    payload = json_object['payload']
    if 'token' in payload:
        _AUTH_TOKEN = payload['token']

    if 'user_id' in json_object:
        _DEFAULT_VAMS_USERID = json_object['user_id']


def calcAuthHash(endpoint, reqMethod, date):
    """
    Calculates the Victorious backend authentication hash

    :param endpoint:
        The API endpoint being called

    :param reqMethod:
        The request method type 'GET' or 'POST'

    :param date:
        Date string sent as the Date HTTP header

    :return:
        A SHA1 hash used to authenticate subsequent requests
    """
    return hashlib.sha1(
            date + endpoint + _DEFAULT_USERAGENT + _AUTH_TOKEN +
            reqMethod).hexdigest()

def headersWith(path, requestType):
    """
    Calculates the appropriate headers for the given path and request type.

    :param path:
        The API path being called.

    "param requestType:
        The RESTful HTTP method that these headers will be part of.
    """
    date = createDateString()
    req_hash = calcAuthHash(path, requestType, date)
    auth_header = 'BASIC %s:%s' % (_DEFAULT_VAMS_USERID, req_hash)

    return {
        'Authorization': auth_header,
        'User-Agent': _DEFAULT_USERAGENT,
        'Date': date
    }

def assetFetcher(url, filename):
    """
    Requests an asset using a provided url and writes it to a folder
    :param url:
        The url of the asset to download

    :param filename:
        The filename / location to write the downloaded asset to
    """

    response = requests.get(url)
    if len(response.content) > 0:
        with open(filename, 'wb') as outfile:
            outfile.write(response.content)
