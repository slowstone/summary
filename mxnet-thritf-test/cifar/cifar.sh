#!/bin/bash

THIS_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $THIS_DIR

VALUE=""

while [ -n "$1" ]            
do
    VALUE=$VALUE" "$1
    shift
done

echo "VALUE:" $VALUE

python cifar.py $VALUE