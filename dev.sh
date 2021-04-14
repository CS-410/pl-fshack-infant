#!/bin/bash

if [ -z "$1" ]; then
	echo "no argument supplied"
	exit 1
elif [ "$1" == "--download" ]; then
	if [ -d "freesurfer" ]; then
		echo "FreeSurfer directory already exists"
		exit 1
	else
		FILENAME="freesurfer-linux-centos7_x86_64-7.1.1-infant.tar"
		wget -c "https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/infant/$FILENAME"
		tar -xvf $FILENAME
		cp license.txt freesurfer
	fi
elif [ "$1" == "--build" ]; then
	docker build -f Dockerfile.dev -t local/pl-fshack-infant-dev .
elif [ "$1" == "--delete" ]; then
	docker image rm local/pl-fshack-infant-dev
	docker system prune
elif [ "$1" == "--run" ]; then
	docker run -v "$PWD/freesurfer:/usr/local/freesurfer" --rm local/pl-fshack-infant-dev fshack_infant.py --help
fi
