# `pl-fshack-infant`

Table of Contents
  * [Abstract](#abstract)
  * [Synopsis](#synopsis)
  * [Description](#description)
  * [Run](#run)
    * [Pull DICOM](#pull-dicom)
    * [Pull NIFTI](#pull-nifti)
  * [Examples](#examples)
    * [`recon-all`](#recon-all)
    * [`mri_convert`](#mri_convert)

## Abstract

## Synopsis

## Description


## Run

While `pl-fshack-infant` is meant to be run as a containerized docker image, typcially within ChRIS, it is quite possible to run the plugin directly from the command line as well. The following instructions are meant to be a psuedo- jupyter-notebook inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

First, let's create a directory, say `devel` where-ever you feel like it. We will place some test data in this directory to process with this plugin.
```
cd ~/
mkdir devel
cd devel
export DEVEL=$(pwd)
```
Now, we need to fetch sample data.

## Pull DICOM

- We provide a sample directory of anonymous `.dcm` images here: (https://github.com/FNNDSC/SAG-anon.git)
- Clone this repository (`SAG-anon`) to your local computer.
```
git clone https://github.com/FNNDSC/SAG-anon.git
```
Make sure the `SAG-anon` directory is placed in the `devel` directory (you should be there already if you are following along)

## Pull NIFTI

- We provide a sample directory of a `.nii` volume here. (https://github.com/FNNDSC/SAG-anon-nii.git)
- Clone this repository (`SAG-anon-nii`) to your local computer.

```
git clone https://github.com/FNNDSC/SAG-anon-nii.git
```
Make sure the `SAG-anon-nii` directory is placed in the `devel` directory.

Using `docker run`

To run using `docker`, be sure to assign an "input" directory to `/incoming` and an output directory to `/outgoing`. Make sure that the `/out` directory is world writable!

- Make sure your current working directory is `devel`. At this juncture it should contain `SAG-anon` and `SAG-anon-nii`.
- Create an output directory named `results` in `devel`.

```
mkdir results && chmod 777 results
```
## Examples

Copy and modify the different commands below as needed.
### `recon-all`

For `NifTI` inputs:
```
docker run --rm                                                         \
    -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing   
    -v $PWD/freesurfer:/usr/local/freesurfer                            \
    local/pl-fshack-infant-dev fshack_infant.py                         \
    -i SAG-anon.nii                                                     \
    -o recon-of-SAG-anon-nii                                            \
    --exec recon-all                                                    \
    --args 'ARGS: -all -notalairach'                                    \
    /incoming /outgoing
```
NOTE: In the `--args` flag, choose one of the arguments to run, not both. 

For `DICOM` inputs:
```
docker run --rm                                                         \
    -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing   
    -v $PWD/freesurfer:/usr/local/freesurfer                            \
    local/pl-fshack-infant-dev fshack_infant.py                         \
    -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm    \
    -o recon-of-SAG-anon-dcm                                            \
    --exec recon-all                                                    \
    --args 'ARGS: -all -notalairach'                                    \
    /incoming /outgoing
```
NOTE: The `recon-all` commands will take multiple hours to run to completion!
### `mri_convert`

```
docker run --rm                                                         \
    -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing  \
    -v $PWD/freesurfer:/usr/local/freesurfer                            \
    local/pl-fshack-infant-dev fshack_infant.py                         \
    -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm    \
    -o DCM2NII.nii                                                      \
    --exec mri_convert                                                  \
    /incoming /outgoing
```

