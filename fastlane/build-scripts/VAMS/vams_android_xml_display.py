# --------------------
# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 08/05/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Parses a Jenkins credentials xml file to display the credential id used to generate an Android build.

"""

import sys
import xmltodict
import vams_common as vams


def parseJenkinsCredentials(filename):
    f = open(filename, 'r')
    xml_doc = f.read()
    dict = xmltodict.parse(xml_doc)

    for app in dict['com.cloudbees.plugins.credentials.SystemCredentialsProvider']['domainCredentialsMap']['entry'][
                'java.util.concurrent.CopyOnWriteArrayList']['org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl']:
        print 'ID: %s\nDescription: %s\n\n' % (app['id'], app['description'])


def showProperUsage():
        print ''
        print 'Usage: ./vams_parse_creds_xml.py <xml_file>'
        print ''
        print '<xml_file> is the name of the Jenkins Credentials XML file to parse.'
        print ''
        print 'example:'
        print './vams_parse_creds_xml.py my_file.xml'
        print ''
        return 1


def main(argv):
    if len(argv) < 2:
        showProperUsage()

    vams.init()

    xml_filename = argv[1]

    if len(argv) == 3:
        vams._JENKINS_SEND_NOTIFICATIONS = argv[2]

    parseJenkinsCredentials(xml_filename)

    return 0


if __name__ == '__main__':
    main(sys.argv)
