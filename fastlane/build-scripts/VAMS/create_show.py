#!/usr/bin/python

# Author: Michael Sena - Oxygen breather.
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 06/26/2016
# Copyright 2016 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, creates a show for later scheduling in the stage.
"""
import requests
import json
import argparse
import sys
import vams_common as vams

# Supress compiled files
sys.dont_write_bytecode = True

_STAGE_PATH = '/v1/stage/stage_show'


def createShow(showName, appID):
    # This should be updated to be the correct host (hardcoded for now)
    url = '%s%s' % (_VAPI_ENVIRONMENT, _STAGE_PATH)
    headers = vams.headersWith(_STAGE_PATH, 'POST')
    headers['content-type'] = 'application/json'
    data = {
        "title": showName,
        "app_id": appID
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == requests.codes.ok:
        print 'Success!'
        print response.json()
    else:
        print 'failure: '
        print response.status_code


def main(argv):

    vams.init()

    parser = argparse.ArgumentParser(description='Creates a new show to be scheduled and updated at a later time.')
    parser.add_argument('--showName', required=True, help="The name of the show to be created.")
    parser.add_argument('--appID', default='24', help="The app id of for where this show should be created. Defaults to 11 (Victorians).")
    parser.add_argument('--environment', default='staging', help='The environment for which we are targeting.', choices=['dev', 'staging', 'production'])
    args = parser.parse_args()

    global _VAPI_ENVIRONMENT
    _VAPI_ENVIRONMENT = vams.GetVictoriousVAPI(args.environment)

    if vams.authenticateUser(vams.GetVictoriousHost(args.environment)):
        createShow(args.showName, args.appID)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
