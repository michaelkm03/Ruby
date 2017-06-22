#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 08/08/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Retrieves the detail of a specific iOS Jenkins build job

"""
import sys
import subprocess
import vams_common as vams

sys.path.append('/Library/Python/2.7/site-packages')

import jenkins

# Suppress compiled files
sys.dont_write_bytecode = True


def getJenkinsJobDetail(job_name):
    j = jenkins.Jenkins(vams._JENKINS_IOS_URL, vams._JENKINS_IOS_USER, vams._JENKINS_IOS_API_KEY)
    job_list = j.get_jobs()

    for job in job_list:
        status = 'BLUE'
        if job['color'] == 'red':
            status = 'RED'
        print "Job: %s (%s)" % (job['name'], status)


    # Clean up remnant files
    cleanUp()


def cleanUp():
    subprocess.call('find . -name \'*.pyc\' -delete', shell=True)

def showProperUsage():
        print ''
        print 'Usage: ./jenkins_job_detail.py "<job_name>"'
        print ''
        print '<job_name> is the name of the Jenkins job you want details for.'
        print ''
        print 'example usage:'
        print './jenkins_job_detail.py "iOS Stable Build"'
        print ''
        return 1


def main(argv):
    if len(argv) < 2:
        showProperUsage()

    job_name = argv[1]

    getJenkinsJobDetail(job_name)

    return 0


if __name__ == '__main__':
    main(sys.argv)
