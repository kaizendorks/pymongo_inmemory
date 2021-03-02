#!/bin/bash

# test_mongod_cleanup.sh
#
# This test checks if the main python process can properly clean up after being
# terminated.

echo "============================================================================================="
echo "  Starting clean up test."
echo "---------------------------------------------------------------------------------------------"

WAIT_TO_KILL=30
WAIT_FOR_SPINDOWN=2

MONGOD_BEFORE=$(pgrep mongod)
echo "All mongod processes running before we kick off: $MONGOD_BEFORE"

$(which python3) -m pymongo_inmemory.mongod > /dev/null &
PYTHON_PROCESS_ID=$!
echo "Started python process with PID $PYTHON_PROCESS_ID. Waiting to kill in $WAIT_TO_KILL seconds."
sleep $WAIT_TO_KILL
echo "Killing python process, $PYTHON_PROCESS_ID"
kill $PYTHON_PROCESS_ID
echo "Waiting, $WAIT_FOR_SPINDOWN, to allow shutoff"
sleep $WAIT_FOR_SPINDOWN

MONGOD_AFTER=$(pgrep mongod)
echo "All mongod processes running after we kill main thread: $MONGOD_AFTER"

echo "---------------------------------------------------------------------------------------------"
if [ "$MONGOD_BEFORE" == "$MONGOD_AFTER" ]; then
  echo "Clean up test successful."
  exit 0
else
  echo "Clean up test failed!"
  exit 1
fi
