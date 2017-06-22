#!/bin/bash
###########
# Runs unit and automation tests of the app built for a device in the specific scheme and configuration.
# Sets up a simple python server to receive POSTs from the UIAutomationTests target that collections test summary data.
# Uses collected test summary data to update the UI Test Automation page of the VictoriousIOS wiki.
# See https://github.com/Victorious/VictoriousiOS/wiki/UI-Automation-Tests
###########

SCHEME=$1
DEVICE_NAME=$2
DEFAULT_PROVISIONING_PROFILE_PATH="build-scripts/tests.mobileprovision"
EMBEDDED_MESSAGES_EXTENSION_SCHEME="EmbeddedMessagesExtension"
STUDIO_SCHEME="debug-studio"

# Check input
if [ "$SCHEME" == "" ]; then
    echo "Usage: `basename $0` <xcode scheme> [<configuration name>] [<device name>]"
    exit 1
fi

# Copy provisioning profile into Xcode
DEFAULT_PROVISIONING_PROFILE_UUID=`/usr/libexec/PlistBuddy -c 'Print :UUID' /dev/stdin <<< $(security cms -D -i "$DEFAULT_PROVISIONING_PROFILE_PATH")`
cp "$DEFAULT_PROVISIONING_PROFILE_PATH" "$HOME/Library/MobileDevice/Provisioning Profiles/$DEFAULT_PROVISIONING_PROFILE_UUID.mobileprovision"

if [ "$DEVICE_NAME" == "" ]; then
    echo "No device specified, will run tests on iPhone 6 Simulator."
    DESTINATION="platform=iOS Simulator,name=iPhone 6"
else
    DESTINATION="platform=iOS,name=${DEVICE_NAME}"
fi

# Test

# The MAX_FUNCTION_COMPILE_TIME parameter specifies the maximum time allowed to be taken to compile a function in
# milliseconds before a warning is generated. We raise the value much higher than the default to prevent CI builds from
# failing inconsistently, since the compile times will vary depending on the system load. These warnings are intended
# to be found and addressed locally.

# Build the iMessage Extension
xcodebuild GCC_TREAT_WARNINGS_AS_ERRORS=YES \
    SWIFT_TREAT_WARNINGS_AS_ERRORS=YES \
    MAX_FUNCTION_COMPILE_TIME=5000 \
    -workspace victorious/victorious.xcworkspace \
    -scheme $EMBEDDED_MESSAGES_EXTENSION_SCHEME \
    -destination "$DESTINATION" \
    -quiet

IMESSAGE_BUILD_RESULT=$?

if [[ $IMESSAGE_BUILD_RESULT -ne 0 ]]; then
    exit $IMESSAGE_BUILD_RESULT
fi

# Build Studio broadcaster
xcodebuild GCC_TREAT_WARNINGS_AS_ERRORS=YES \
    SWIFT_TREAT_WARNINGS_AS_ERRORS=YES \
    MAX_FUNCTION_COMPILE_TIME=5000 \
    -workspace victorious/victorious.xcworkspace \
    -scheme $STUDIO_SCHEME \
    -destination "$DESTINATION" \
    -quiet

IMESSAGE_BUILD_RESULT=$?

if [[ $IMESSAGE_BUILD_RESULT -ne 0 ]]; then
    exit $IMESSAGE_BUILD_RESULT
fi

# Run tests
xcodebuild GCC_TREAT_WARNINGS_AS_ERRORS=YES \
    SWIFT_TREAT_WARNINGS_AS_ERRORS=YES \
    MAX_FUNCTION_COMPILE_TIME=5000 \
    test \
    -workspace victorious/victorious.xcworkspace \
    -scheme $SCHEME \
    -destination "$DESTINATION" \
    -quiet

exit $?
