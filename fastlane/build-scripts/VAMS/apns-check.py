#!/usr/bin/python

# Author: Lawrence H. Leach - Sr. Software Engineer
# Date: 08/05/2015
# Copyright 2015 Victorious Inc. All Rights Reserved.

"""
Performs an APNS verification procedure to ensure that any IPA submitted has the APNS entitlement.

"""
import sys
import subprocess
import shutil
from subprocess import call
import xml.etree.ElementTree as ET
from plist_parser import XmlPropertyListParser
import tempfile
import vams_common as vams

_WORKING_DIRECTORY = ''

def showProperUsage():
        print ''
        print 'Usage: ./apns-check.py <plist-file>'
        print ''
        print '<plist-file> is the plist file to check for apns enablement.'
        print ''
        print 'example usage:'
        print './apns-check.py Jess-Lizama_codesign.plist'
        print ''
        sys.exit(1)

def cleanUp():
    shutil.rmtree(_WORKING_DIRECTORY)

def main(argv):
    if len(argv) < 2:
        showProperUsage()

    vams.init()

    global _WORKING_DIRECTORY
    plist_path = tempfile.mkdtemp()
    _WORKING_DIRECTORY = plist_path

    plist_file = argv[1]
    plist_call = '/usr/libexec/PlistBuddy -c "Print aps-environment" %s' % plist_file
    #resp = subprocess.call(['/usr/libexec/PlistBuddy', '-c "Print aps-environment" %s' % plist_file ])
    resp = subprocess.call(plist_call)
    print resp


    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
