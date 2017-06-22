#!/bin/bash
###########
# Copies plist settings from one plist to another
###########

SOURCE=$1
DESTINATION=$2
P_FLAG=$3
PRODUCT_PREFIX=$4

if [ "$SOURCE" == "" -o "$DESTINATION" == "" ]; then
    echo "Usage: $0 <source> <destination> [-p <PRODUCT_PREFIX>]"
    echo ""
    echo "PRODUCT_PREFIX, if supplied, will be used to replace instances of \${ProductPrefix}."
    exit 1
fi

if [ ! -f "$SOURCE" ]; then
    pwd
    echo "\"$SOURCE\" not found."
    exit 1
fi

if [ ! -f "$DESTINATION" ]; then
    echo "\"$DESTINATION\" not found."
    exit 1
fi

# Make sure plist is readable
/usr/libexec/PlistBuddy -c "Print" "$SOURCE" > /dev/null
if [ $? != 0 ]; then
    echo "Error reading \"$SOURCE\""
    exit 1
fi

copyPListValue(){
    if [ "$P_FLAG" == "-p" ]; then
        local VAL=$(/usr/libexec/PlistBuddy -c "Print $1" "$SOURCE" | sed -e "s/\${ProductPrefix}/$PRODUCT_PREFIX/g")
    else
        local VAL=$(/usr/libexec/PlistBuddy -c "Print $1" "$SOURCE" 2> /dev/null)
    fi
    /usr/libexec/PlistBuddy -c "Set $1 $VAL" "$DESTINATION"
}

returnBundleIdentifier() {
    if [ "$P_FLAG" == "-p" ]; then
        local BUNDLE_IDENTIFIER=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$SOURCE" | sed -e "s/\${ProductPrefix}/$PRODUCT_PREFIX/g")
    else
        local BUNDLE_IDENTIFIER=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$SOURCE" 2> /dev/null)
    fi
    echo $BUNDLE_IDENTIFIER
}

copyPListValue 'CFBundleDisplayName'
copyPListValue 'FacebookAppID'
copyPListValue 'FacebookDisplayName'
copyPListValue 'CreatorSalutation'
copyPListValue 'AnonymousAccountUserID'
copyPListValue 'AnonymousAccountUserToken'
copyPListValue 'TokBoxApiKey'
copyPListValue 'LeanPlumAppId'
copyPListValue 'LeanPlumDevKey'
copyPListValue 'LeanPlumProdKey'
copyPListValue 'branch_app_domain'
copyPListValue 'branch_key:live'
copyPListValue 'VictoriousDeeplinkURLScheme'
copyPListValue 'EmbeddedStickerFetchEndpoint'
copyPListValue 'StandaloneStickerFetchEndpoint'

returnBundleIdentifier
