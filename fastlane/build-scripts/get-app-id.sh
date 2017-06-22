#!/bin/bash -e
###########
# Finds the appropriate app ID for a given build configuration.
###########

FOLDER=$1        # Folder containing app resources including, crucially, an Info.plist file
CONFIGURATION=$2 # Build configuration (e.g. Debug, Staging, Stable, Release)

if [ "$FOLDER" == "" ]; then
    exit 0
fi

# Default App ID key: the plist key that contains the app ID that corresponds to the configuration we're building.
if [ "$CONFIGURATION" == "Release" ]; then
    DEFAULT_APP_ID_KEY="VictoriousAppID"
elif [ "$CONFIGURATION" == "Staging" ]; then
    DEFAULT_APP_ID_KEY="StagingAppID"
else
    DEFAULT_APP_ID_KEY="VictoriousAppID"
fi

DEFAULT_APP_ID=$(/usr/libexec/PlistBuddy -c "Print $DEFAULT_APP_ID_KEY" "$FOLDER/Info.plist" 2> /dev/null)

echo $DEFAULT_APP_ID
