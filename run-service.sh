#!/bin/bash
THIS_DIR=$(dirname $(readlink -f $0))

nohup python3 ${THIS_DIR}/src/App.py &

