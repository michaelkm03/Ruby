#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 07/15/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Runs an iOS Jenkins build job

"""
import sys
import subprocess
import vams_common as vams

sys.path.append('/Library/Python/2.7/site-packages')

import jenkins

# Supress compiled files
sys.dont_write_bytecode = True


def generateJenkinsBuild(app_name):
    job = jenkins.Jenkins(vams._JENKINS_IOS_URL, vams._JENKINS_IOS_USER, vams._JENKINS_IOS_API_KEY)
    job.build_job(vams._JENKINS_IOS_JOB, {'APP_NAMES': app_name,'SEND_NOTIFICATIONS': vams._JENKINS_IOS_SEND_NOTIFICATIONS}, vams._JENKINS_IOS_API_KEY)
    cleanUp()


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def showProperUsage():
        print ''
        print 'Usage: ./build_ios.py <app_name> <notifications>'
        print ''
        print '<app_name> is the name of the application to request Jenkins to build.'
        print '<notifications> OPTIONAL: \'True\' if notification emails should be sent upon completion. \'False\' if not.'
        print ''
        print 'NOTE: If no <notifications> parameter is provided, the system WILL send email notifications.'
        print ''
        print 'examples:'
        print './build_ios.py awesomeness        <-- will send email notifications'
        print '  -- OR --'
        print './build_ios.py awesomeness False  <-- will NOT send email notifications'
        print ''
        return 1


def main(argv):
    if len(argv) < 2:
        showProperUsage()

    vams.init()

    app_name = argv[1]

    if len(argv) == 3:
        vams._JENKINS_SEND_NOTIFICATIONS = argv[2]

    generateJenkinsBuild(app_name)

    return 0


if __name__ == '__main__':
    main(sys.argv)
