#!/usr/bin/env bash
###########
# Modifies an .xcarchive according to
# an individual app configuration.
###########

APP_NAME=$1
HAS_MESSAGES_EXTENSION=false
HAS_STANDALONE_MESSAGES_APP=false
CONFIGURATION=""
ENVIRONMENT="production"

show_usage () {
    echo "Usage: `basename $0` <app name> [-c <build configuration> -e <VAMS environment> -m -s]"
    echo ""
    echo "If -c is specified, it will use the provisioning profile for the configuration, otherwise no provisioning profile will be copied."
    echo ""
    echo "If -e is specified, it will use the provided environment, otherwise the production VAMS API is used."
    echo ""
    echo "If -m is specified, fields in the iMessage extension's plist will be setup for deployment automatically."
    echo ""
    echo "If -s is specified, fields in the standalone Message extension's plist will be setup for deployment automatically."
    echo ""
}

# Parse command line arguments
OPTIND=2
while getopts "e:c:ms" opt; do
    case $opt in
        c)
            CONFIGURATION=$OPTARG
            ;;
        e)
            ENVIRONMENT=$OPTARG
            ;;
        m)
            HAS_MESSAGES_EXTENSION=true
            ;;
        s)
            HAS_STANDALONE_MESSAGES_APP=true
            ;;
        *)
            show_usage
            exit 1
    esac
done

if [ "$APP_NAME" == "" ]; then
  show_usage
  exit 1
fi

# Grab the latest assets and configuration data from VAMS.
RESPONSE=$(python build-scripts/VAMS/vams_prebuild.py $APP_NAME ios $ENVIRONMENT 2>&1)
RESPONSE_CODE=$(echo "$RESPONSE" | cut -f1 -d '|')
RESPONSE_MESSAGE=$(echo "$RESPONSE" | cut -f2 -d '|')
# If no working folder is returned then exit
if [ "$RESPONSE_CODE" -ne 0 ]; then
    echo $RESPONSE_MESSAGE
    exit 1
else
    FOLDER="$RESPONSE_MESSAGE"
fi

DEST_PATH="victorious/AppSpecific"
MESSAGES_PLIST="victorious/EmbeddedMessagesExtension/Info.plist"
STANDALONE_MESSAGES_PLIST="victorious/StandaloneMessagesExtension/Info.plist"
STANDALONE_CONTAINER_PLIST="victorious/StandaloneMessagesApp/Info.plist"
SHARED_PLIST="victorious/VictoriousIOSSDK/SharedInfo.plist"

if [ ! -d "$DEST_PATH" ]; then
    echo "Nothing found at expected path: \"$DEST_PATH\""
    exit 1
fi

### Modify Info.plist and project.pbxproj

APP_PLIST="$DEST_PATH/Info.plist"
MAIN_APP_IDENTIFIER=$(./build-scripts/copy-plist.sh "$FOLDER/Info.plist" "$APP_PLIST" 2> /dev/null)

# Find and replace all PRODUCT_BUNDLE_IDENTIFIER across the project
PROJECT_FILE_PATH="victorious/victorious.xcodeproj/project.pbxproj"
git checkout $PROJECT_FILE_PATH
sed -i '' 's/com.getvictorious.${ProductPrefix}victorious/'"$MAIN_APP_IDENTIFIER/g" $PROJECT_FILE_PATH

# Copy Info.plist fields for Embedded Messages Extension
if [ $HAS_MESSAGES_EXTENSION == true ]; then
    DISPLAY_NAME=$(/usr/libexec/PlistBuddy -c "Print CFBundleDisplayName" "$APP_PLIST")
    /usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $DISPLAY_NAME" "$MESSAGES_PLIST"

    STICKER_ENDPOINT=$(/usr/libexec/PlistBuddy -c "Print EmbeddedStickerFetchEndpoint" "$APP_PLIST")
    /usr/libexec/PlistBuddy -c "Set :StickerFetchEndpoint $STICKER_ENDPOINT" "$MESSAGES_PLIST"
fi

# Copy Info.plist fields for Standalone Messages Extension
if [ $HAS_STANDALONE_MESSAGES_APP == true ]; then    
    DISPLAY_NAME=$(/usr/libexec/PlistBuddy -c "Print CFBundleDisplayName" "$APP_PLIST")
    /usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $DISPLAY_NAME" "$STANDALONE_CONTAINER_PLIST"
    /usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $DISPLAY_NAME" "$STANDALONE_MESSAGES_PLIST"

    STICKER_ENDPOINT=$(/usr/libexec/PlistBuddy -c "Print StandaloneStickerFetchEndpoint" "$APP_PLIST")
    /usr/libexec/PlistBuddy -c "Set :StickerFetchEndpoint $STICKER_ENDPOINT" "$STANDALONE_MESSAGES_PLIST"
fi

### Set App IDs

STAGING_APP_ID=$(./build-scripts/get-app-id.sh "$FOLDER" "Staging" 2> /dev/null)
if [ $? != 0 ]; then
    echo "Could not read app ID from Info.plist"
    exit 1
fi

PRODUCTION_APP_ID=$(./build-scripts/get-app-id.sh "$FOLDER" "Production" 2> /dev/null)
if [ $? != 0 ]; then
    echo "Could not read app ID from Info.plist"
    exit 1
fi

setAppIDs(){
    ENVIRONMENTS_PLIST="$1"
    N=0
    while [ 1 ]
    do
        NAME=$(/usr/libexec/PlistBuddy -c "Print :$N:name" "$ENVIRONMENTS_PLIST" 2> /dev/null)
        if [ "$NAME" == "" ]; then
            break
        elif [ "$NAME" == "Staging" ]; then
            /usr/libexec/PlistBuddy -c "Set :$N:appID $STAGING_APP_ID" "$ENVIRONMENTS_PLIST"
        elif [ "$NAME" == "Production" ]; then
            /usr/libexec/PlistBuddy -c "Set :$N:appID $PRODUCTION_APP_ID" "$ENVIRONMENTS_PLIST"
        fi

        let N=$N+1
    done
}

PLIST_FILES=$(find "$DEST_PATH" -name environments\*.plist)
IFS=$'\n'

for PLIST_FILE in $PLIST_FILES
do
    setAppIDs "$PLIST_FILE"
done


### Copy Files

copyFile(){
    if [ -a "$FOLDER/$1" ]; then
        cp "$FOLDER/$1" "$DEST_PATH/$1"
    elif [ -a "$DEST_PATH/$1" ]; then
        rm "$DEST_PATH/$1"
    fi
}

copyFile "LaunchImage@2x.png"
copyFile "Icon-29@2x.png"
copyFile "Icon-40@2x.png"
copyFile "Icon-60@2x.png"

PROVISIONING_PROFILE_DESTINATION_PATH="./custom.mobileprovision"
if [ -e "$PROVISIONING_PROFILE_DESTINATION_PATH" ]; then
    rm "$PROVISIONING_PROFILE_DESTINATION_PATH"
fi

if [ "$CONFIGURATION" != "" ]; then
    CONFIGURATION_LOWERCASE=$(echo $CONFIGURATION | tr '[:upper:]' '[:lower:]')
    PROVISIONING_PROFILE_PATH="$FOLDER/${CONFIGURATION_LOWERCASE}.mobileprovision"
    if [ -e "$PROVISIONING_PROFILE_PATH" ]; then
        cp "$PROVISIONING_PROFILE_PATH" "$PROVISIONING_PROFILE_DESTINATION_PATH"
    fi
fi

### Remove Temp Directory

rm -rf $FOLDER
