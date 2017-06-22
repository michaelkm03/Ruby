#!/bin/bash
###########
# Adds URL schemes for Facebook and Victorious app deep linking to Info.plist
###########

APP_BUNDLE=$1

if [ "$APP_BUNDLE" == "" ]; then
    echo "Usage: `basename $0` <path/to/bundle.app>"
    echo ""
    exit 1
fi

INFOPLIST="$APP_BUNDLE/Info.plist"

# Clean the slate

/usr/libexec/PlistBuddy -c "Delete FacebookUrlSchemeSuffix" "$INFOPLIST" 2> /dev/null

# Facebook

FB_APPID=$(/usr/libexec/PlistBuddy -c "Print :FacebookAppID" "$INFOPLIST" 2> /dev/null)
DISPLAY_NAME=$(/usr/libexec/PlistBuddy -c "Print :CFBundleDisplayName" "$INFOPLIST" 2> /dev/null | sed 's/[^a-zA-Z0-9]//g')
/usr/libexec/PlistBuddy -c "Add CFBundleURLTypes:1:CFBundleURLSchemes Array" "$INFOPLIST"
/usr/libexec/PlistBuddy -c "Add CFBundleURLTypes:1:CFBundleURLSchemes: string fb${FB_APPID}${DISPLAY_NAME}" "$INFOPLIST"
/usr/libexec/PlistBuddy -c "Add FacebookUrlSchemeSuffix string $DISPLAY_NAME" "$INFOPLIST"

# App Deep Linking

CUSTOM_SCHEME=$(/usr/libexec/PlistBuddy -c "Print :VictoriousDeeplinkURLScheme" "$INFOPLIST" 2> /dev/null)
/usr/libexec/PlistBuddy -c "Add CFBundleURLTypes:0:CFBundleURLSchemes: string $CUSTOM_SCHEME" "$INFOPLIST"
