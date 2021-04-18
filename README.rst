pl-fshack-infant
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-fshack-infant?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-fshack-infant

.. image:: https://img.shields.io/github/license/fnndsc/pl-fshack-infant
    :target: https://github.com/FNNDSC/pl-fshack-infant/blob/master/LICENSE


.. contents:: Table of Contents


Abstract
--------

An app to ...


Description
-----------

This ChRIS DS plugin contains a complete Infant FreeSurfer distribution.

Not all FreeSurfer internal applications are exposed at the plugin level, however. Currently, the following Infant FreeSurfer applications are directly accessible from the plugin CLI:

* :code:`recon-all`
* :code:`mri_convert`
* :code:`mri_info`
* :code:`mris_info`

This plugin is meant to demonstrate certain design patterns and provide some utility for running Infant FreeSurfer within the context of ChRIS. It is not meant nor intended to be a canonical Infant FreeSurfer
ChRIS plugin — as explicitly indicated by the name, FreeSurfer 'hack'. Colloquially, this plugin is also known as *f-shack-infant*.


Usage
-----

.. code::

    python fshack_infant.py
           [-i|--inputFile <file>]
	   [-o|--outputFile <file>]
           [-e|--exec <command>]
	   [-a|--args <arguments>]
	   [-h|--help]
	   [--man]
	   [--meta]
	   [--json]
	   [--savejson <directory>]
	   [-v|--verbosity <level>]
	   [--version]
	   <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 


Run
~~~

While :code:`pl-fshack-infant` is meant to be run as a containerized Docker image — typically within ChRIS — it is possible to run the plugin directly from the command line as well.

If using :code:`docker run`, you must specify input and output directories using the volume :code:`-v` flag.

.. code:: bash

    docker run --rm -u $(id -u)                                \
               -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
               fnndsc/pl-fshack-infant fshack_infant.py        \
               /incoming /outgoing


Examples
~~~~~~~~

First, we will create a :code:`devel` directory and a globally accessible :code:`results` directory inside it.

.. code:: bash

    cd ~
    mkdir devel
    cd devel
    export DEVEL=$(pwd)
    mkdir results && chmod 777 results

Now, we will fetch test data.

* A sample directory containing anonymous :code:`.dcm` images is provided here: https://github.com/FNNDSC/SAG-anon
* A sample directory containing an anonymous :code:`.nii` volume is provided here: https://github.com/FNNDSC/SAG-anon-nii

Clone either or both of these repositories into the newly created :code:`devel` directory.

.. code:: bash

    git clone https://github.com/FNNDSC/SAG-anon.git
    git clone https://github.com/FNNDSC/SAG-anon-nii.git


:code:`recon-all`
****************

It should be noted that the :code:`recon-all` command will take multiple hours to finish!

Moreover, using both the :code:`-all` and :code:`-notailarach` flags will result in an error; as such, they must not be used together.

For :code:`NifTI` inputs:

.. code:: bash

    docker run --rm                                                                \
               -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing  \
               fnndsc/pl-fshack-infant fshack_infant.py                            \
               -i SAG-anon.nii                                                     \
               -o recon-of-SAG-anon-nii                                            \
               --exec recon-all                                                    \
               --args 'ARGS: -all'                                                 \
               /incoming /outgoing

For :code:`DICOM` inputs:

.. code:: bash

    docker run --rm                                                                \
               -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing  \
		fnndsc/pl-fshack-infant fshack_infant.py                           \
                -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm   \
                -o recon-of-SAG-anon-dcm                                           \
                --exec recon-all                                                   \
                --args 'ARGS: -all'                                                \
                /incoming /outgoing


:code:`mri_convert`
******************

.. code:: bash

    docker run --rm                                                                \
               -v ${DEVEL}/SAG-anon-nii/:/incoming -v ${DEVEL}/results/:/outgoing  \ 
               fnndsc/pl-fshack-infant fshack_infant.py                            \
               -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm    \
               -o DCM2NII.nii                                                      \
               --exec mri_convert                                                  \
               /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-fshack-infant .


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
