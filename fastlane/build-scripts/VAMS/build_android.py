#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 07/22/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Runs an Android Jenkins build job

"""
import sys
import subprocess
import vams_common as vams

sys.path.append('/Library/Python/2.7/site-packages')

import jenkins

# Supress compiled files
sys.dont_write_bytecode = True


def generateJenkinsBuild(app_name):
    job = jenkins.Jenkins(vams._JENKINS_ANDROID_URL, vams._JENKINS_ANDROID_USER, vams._JENKINS_ANDROID_API_KEY)
    job.build_job(vams._JENKINS_ANDROID_JOB, {'APP_FOLDER': app_name}, vams._JENKINS_ANDROID_API_KEY)
    cleanUp()


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def showProperUsage():
        print ''
        print 'Usage: ./build_android.py <app_name>'
        print ''
        print '<app_name> is the name of the application to request Jenkins to build.'
        print ''
        print 'examples:'
        print './build_android.py awesomenesstv     <-- Would generate a build for Awesomeness TV.'
        print ''
        return 1


def main(argv):
    if len(argv) < 2:
        showProperUsage()

    vams.init()

    app_name = argv[1]

    generateJenkinsBuild(app_name)

    return 0


if __name__ == '__main__':
    main(sys.argv)
