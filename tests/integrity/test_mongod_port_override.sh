#!/bin/bash

# test_mongod_port_override.sh
#
# This test checks if we can override cound mongod port with an environmental variable.

echo "============================================================================================="
echo "  Starting port override test."
echo "---------------------------------------------------------------------------------------------"

export PYMONGOIM__MONGOD_PORT=27019

WAIT_FOR_SPINUP=10
WAIT_FOR_SPINDOWN=2

MONGOD_BEFORE=$(pgrep mongod)
echo "All mongod processes running before we kick off: $MONGOD_BEFORE"

$(which python3) -m pymongo_inmemory.mongod > /dev/null &
PYTHON_PROCESS_ID=$!
echo "Started python process with PID $PYTHON_PROCESS_ID. Waiting $WAIT_FOR_SPINUP seconds to allow bootup."
sleep $WAIT_FOR_SPINUP
echo "Checking bound port"
lsof -iTCP -sTCP:LISTEN | grep mongod | grep $PYMONGOIM__MONGOD_PORT
RESULT=$?
echo "Killing python process, $PYTHON_PROCESS_ID"
kill $PYTHON_PROCESS_ID
echo "Waiting, $WAIT_FOR_SPINDOWN, to allow shutoff"
sleep $WAIT_FOR_SPINDOWN
unset PYMONGOIM__MONGOD_PORT

MONGOD_AFTER=$(pgrep mongod)
echo "All mongod processes running after we kill main thread: $MONGOD_AFTER"

echo "---------------------------------------------------------------------------------------------"
if [ $RESULT == 1 ]; then
  echo "Port override failed!"
  exit 1
else
  echo "Port override successful"
  exit 0
fi
