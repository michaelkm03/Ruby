#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 08/08/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Retrieves a list of iOS Jenkins build jobs

"""
import sys
import subprocess
import vams_common as vams
import color_codes as ccodes

sys.path.append('/Library/Python/2.7/site-packages')

import jenkins

# Supress compiled files
sys.dont_write_bytecode = True


def getJenkinsJobList():
    j = jenkins.Jenkins(vams._JENKINS_IOS_URL, vams._JENKINS_IOS_USER, vams._JENKINS_IOS_API_KEY)
    job_list = j.get_jobs()

    for job in job_list:
        status = ccodes.color_codes.OKGREEN + 'OK' + ccodes.color_codes.ENDC
        if job['color'] == 'red':
            status = ccodes.color_codes.FAIL + 'FAIL' + ccodes.color_codes.ENDC
        print 'Job: %s\nStatus: %s' % (job['name'], status)
        print ''

    print 'Type ./VAMS/jenkins_job_detail.py "<JOB_NAME>" to get detail on a specific job.'

    # Clean up remnant files
    cleanUp()


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)


def main(argv):

    vams.init()
    getJenkinsJobList()

    return 0


if __name__ == '__main__':
    main(sys.argv)
