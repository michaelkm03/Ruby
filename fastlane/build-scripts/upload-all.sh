#!/bin/bash
###########
# Uploads all apps in the 'products' folder to TestFairy.
###########

TF_DISTRO_LIST="$1"
shift

CONFIGS=`find products -type f -iname *.ipa -depth 1 -exec basename {} \;`
IFS=$'\n'
for CONFIG in $CONFIGS
do
    CONFIG="${CONFIG%.*}"
    IFS=" "
    build-scripts/upload-to-testfairy.sh -a "$CONFIG" -t "$TF_DISTRO_LIST" $*
    if [ $? != 0 ]; then
        FAILED="yes"
    fi
done

if [ "$FAILED" != "" ]; then
    exit 1
else
    exit 0
fi
