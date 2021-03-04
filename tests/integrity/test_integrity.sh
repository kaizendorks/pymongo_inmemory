#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

bash $DIR/test_mongod_cleanup.sh
RESULT=$?
if [ $RESULT == 0 ]; then
  bash $DIR/test_mongod_port_override.sh
  RESULT=$?
  if [ $RESULT == 0 ]; then
    echo "============================================================================================="
    echo "All integrity tests successful."
    exit 0
  fi
fi

echo "============================================================================================="
echo "Some tests failed."
exit 1
