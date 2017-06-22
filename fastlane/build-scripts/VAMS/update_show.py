#!/usr/bin/python

# Author: Michael Sena - Oxygen breather.
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 06/26/2016
# Copyright 2016 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, updates a shows playlist.
"""
import requests
import argparse
import json
import csv
import sys
import vams_common as vams

# Supress compiled files
sys.dont_write_bytecode = True

_STAGE_PATH = '/v1/stage/show/'
_STAGE_PLAYLIST_PATH_PART = '/playlist/'


def updateShow(showID, appID, file):
    path = '%s%s%s' % (_STAGE_PATH, showID, _STAGE_PLAYLIST_PATH_PART)
    # This should be updated to be the correct host (hardcoded for now)
    url = '%s%s' % (_VAPI_ENVIRONMENT, path)

    headers = vams.headersWith(path, 'POST')
    headers['content-type'] = 'application/json'
    data = []

    with file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            rowPayload = {
                'priority': 0,
                'stage_content_rule_id': 2,
                'args': row['contentID'],
                'duration': row['duration']
            }
            data.append(rowPayload)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == requests.codes.ok:
        print 'Success!'
        print response.json()
    else:
        print 'failure: '
        print response.status_code
    
    
def main(argv):

    vams.init()

    parser = argparse.ArgumentParser(description='Updates a show from a given csv file.')
    parser.add_argument('--file', type=argparse.FileType('r'), required=True, help='The csv file to read from.')
    parser.add_argument('--showID', type=int, required=True, help='The id of the show to update.')
    parser.add_argument('--appID', type=int, default=24, help='The appID for the show we are updating.')
    parser.add_argument('--environment', default='staging', help='The environment for which we are targeting.', choices=['dev', 'staging', 'production'])
    args = parser.parse_args()

    global _VAPI_ENVIRONMENT
    _VAPI_ENVIRONMENT = vams.GetVictoriousVAPI(args.environment)

    if vams.authenticateUser(vams.GetVictoriousHost(args.environment)):
        updateShow(args.showID, args.appID, args.file)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
