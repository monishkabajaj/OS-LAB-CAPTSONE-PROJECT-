#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
rm -f reports/*.csv logs/activity.log
echo "Generated reports and activity log removed. Source files preserved."
