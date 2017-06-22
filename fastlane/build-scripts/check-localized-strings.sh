#!/bin/bash
###########
# Scans source files for use of NSLocalizedString and compares the result 
# to the Localizable.strings file to find missing or unused strings.
###########

find victorious/victorious -name *.m -print0 | xargs -0 genstrings 
find victorious/victorious -name *.swift -print0 | xargs -0 genstrings -a
find victorious/VictoriousIOSSDK -name *.m -print0 | xargs -0 genstrings -a
find victorious/VictoriousIOSSDK -name *.swift -print0 | xargs -0 genstrings -a
find victorious/iMessageExtension -name *.m -print0 | xargs -0 genstrings -a
find victorious/iMessageExtension -name *.swift -print0 | xargs -0 genstrings -a
mv Localizable.strings actually-in-use-unsorted-utf16.strings

iconv -f UTF-16 -t UTF-8 actually-in-use-unsorted-utf16.strings > actually-in-use-unsorted.strings
rm actually-in-use-unsorted-utf16.strings

cp "victorious/victorious/Supporting Files/Base.lproj/Localizable.strings" Localizable-unsorted.strings

cat actually-in-use-unsorted.strings | grep = | cut -d \" -f2 | sort | uniq > actually-in-use.strings
cat Localizable-unsorted.strings | grep = | cut -d \" -f2 | sort > Localizable.strings

rm actually-in-use-unsorted.strings
rm Localizable-unsorted.strings

opendiff Localizable.strings actually-in-use.strings

rm Localizable.strings
rm actually-in-use.strings
