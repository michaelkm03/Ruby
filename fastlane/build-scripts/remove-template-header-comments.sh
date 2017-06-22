# Removes all of the header comments from Xcode file templates.
# This must be run locally on each dev machine each time a new version of Xcode is installed.
# Make sure to use the xcode-select command to choose the correct Xcode version before running this script.

XCODE_DIR=$(xcode-select -p)
DIR1="$XCODE_DIR/Platforms/iPhoneOS.platform/Developer/Library/Xcode/Templates"
DIR2="$XCODE_DIR/Library/Xcode/Templates"

find -E "$DIR1" -type f \( -regex '.*\.[chm]' -or -regex '.*\.swift' \) -exec sed -i '' '1,/^$/d' '{}' ';'
find -E "$DIR2" -type f \( -regex '.*\.[chm]' -or -regex '.*\.swift' \) -exec sed -i '' '1,/^$/d' '{}' ';'
