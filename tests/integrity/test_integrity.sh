#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# echo $DIR
bash $DIR/test_mongod_cleanup.sh

RESULT=$?
if [ $RESULT == 0 ]; then
  echo "All integrity tests successful."
  exit 0
else
  echo "Some tests failed."
  exit 1
fi
