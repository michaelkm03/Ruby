#!/usr/bin/python

# Author: Michael Sena - Oxygen breather.
# Note: Hash calculating code was "borrowed" from Frank Zhao.
# Date: 06/27/2016
# Copyright 2016 Victorious Inc. All Rights Reserved.

"""
Authenticates with the Victorious backend, schedules a show on a particular stage.
"""
import requests
import argparse
import json
import sys
import vams_common as vams
import time
import datetime

# Supress compiled files
sys.dont_write_bytecode = True

_STAGE_PATH = '/v1/stage/'
_STAGE_PATH_PART = '/stage/'
_STAGE_SCHEDULED_SHOWS_PATH_PART = '/scheduled_shows'


def scheduleShow(showID, appID, stage, startTime):
    path = '/v1/stage/schedule_show'
    url = '%s%s' % (_VAPI_ENVIRONMENT, path)

    headers = vams.headersWith(path, 'POST')
    headers['content-type'] = 'application/json'

    data = {
        'stage_show_id': showID,
        'stage': stage,
        'start_time': startTime
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

    parser = argparse.ArgumentParser(description='Sends a show to a particular stage.')
    parser.add_argument('--showID', type=int, required=True, help='The id of the show to update.')
    parser.add_argument('--stage', default='main', help='The stage for which we are scheduling.', choices=['main', 'vip'])
    parser.add_argument('--appID', type=int, default=24, help='The appID for the show we are updating.')
    parser.add_argument('--environment', default='staging', help='The environment for which we are targeting.', choices=['dev', 'staging', 'production'])
    parser.add_argument('--startOffset', type=int, default=0, help='The number of seconds in the future to schedule this show at.')
    args = parser.parse_args()

    global _VAPI_ENVIRONMENT
    _VAPI_ENVIRONMENT = vams.GetVictoriousVAPI(args.environment)

    if vams.authenticateUser(vams.GetVictoriousHost(args.environment)):
        
        currentSeconds = time.time()
        adjustedSeconds = currentSeconds + args.startOffset
        scheduledDate = datetime.datetime.fromtimestamp(adjustedSeconds)
        print('Scheulding show at: ' + scheduledDate.isoformat())

        startTimeInMillis = int(adjustedSeconds * 1000)
        scheduleShow(args.showID, args.appID, args.stage, startTimeInMillis)
    else:
        print 'There was a problem authenticating with the Victorious backend. Exiting now...'
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
