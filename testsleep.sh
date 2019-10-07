#!/bin/bash
if [ "$1" == "" ] ; then TIME=10 ; else TIME=$1 ; fi
echo -e "Going to sleep for $TIME seconds\n"
sleep $TIME
echo -e "Wake up! $TIME seconds has been slept"
