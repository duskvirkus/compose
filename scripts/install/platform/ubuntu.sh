#!/usr/bin/env bash

if [ $EUID != 0 ]; then
	echo "this script must be run using sudo"
	echo ""
	echo "usage:"
	echo "sudo "$0
	exit $exit_code
    exit 1
fi

apt-get install build-essential ffmpeg nvidia-cuda-toolkit cmake