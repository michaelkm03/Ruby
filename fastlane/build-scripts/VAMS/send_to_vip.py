#!/usr/bin/python

# Author: Michael Sena - Cat Owner and ATHF fan.
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 06/21/2016
# Copyright 2016 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, sends a content ID to the VIP stage.
"""
import requests
import argparse
import sys
import vams_common as vams

# Supress compiled files
sys.dont_write_bytecode = True

_STAGE_PATH_BEGINNING = '/v1/stage/'
_SEND_TO_VIP_PATH_PART = '/send_to_vip/'


def sendToVIP(appID, contentID):
    # Calculate request hash
    path = '%s%s%s%s' % (_STAGE_PATH_BEGINNING, appID, _SEND_TO_VIP_PATH_PART, contentID)
    url = '%s%s' % (_VAPI_ENVIRONMENT, path)
    
    headers = vams.headersWith(path, 'POST')
    response = requests.post(url, data=None, headers=headers)

    if response.status_code == requests.codes.ok:
        print 'Success!'
        print response.json()
    else:
        print 'failure: '
        print response.status_code


def main(argv):

    vams.init()

    parser = argparse.ArgumentParser(description='Creates a new show to be scheduled and updated at a later time. 11198596 is the content ID Star wars on victorians prod.')
    parser.add_argument('--contentID', required=True, type=int, help="The content id of the content to be sent to VIP Stage.")
    parser.add_argument('--appID', default='24', help="The app id of for where this show should be created. Defaults to 11 (Victorians).")
    parser.add_argument('--environment', default='staging', help='The environment for which we are targeting.', choices=['dev', 'staging', 'production'])
    args = parser.parse_args()

    global _VAPI_ENVIRONMENT
    _VAPI_ENVIRONMENT = vams.GetVictoriousVAPI(args.environment)

    if vams.authenticateUser(vams.GetVictoriousHost(args.environment)):
        sendToVIP(args.appID, args.contentID)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
