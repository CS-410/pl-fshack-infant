#!/bin/bash

if [ -z "$1" ]; then
	echo "no argument supplied"
	exit 1
elif [ "$1" == "-d" ]; then
	if [ -d "freesurfer" ]; then                                                                                                              
		echo "FreeSurfer directory already exists"                                                                                            
      	exit 1
	else
		local FILENAME="freesurfer-linux-centos7_x86_64-7.1.1-infant.tar"
		wget -c "https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/infant/$FILENAME"
		tar -xvf $FILENAME
	fi
elif [ "$1" == "-b" ]; then
	docker build -t local/pl-fshack-infant-dev .
elif [ "$1" == "-r" ]; then
	docker run -v "$PWD/freesurfer:/usr/local/freesurfer" --rm local/pl-fshack-infant-dev fshack_infant.py --help
fi