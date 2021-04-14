# Docker file for the pl-fshack-infant ChRIS plugin app
#
# To build locally, do:
#   docker build -t local/pl-fshack-infant .
#
# In the case of a proxy, do:
#    docker build --build-arg http_proxy=http://<IP>:<URL> --build-arg UID=$UID -t local/pl-fshack-infant .
#
# To run an interactive shell inside this container, do:
#   docker run -ti --entrypoint /bin/bash local/pl-fshack-infant
#
# To pass an env var HOST_IP to container, do:
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-fshack-infant

FROM fnndsc/ubuntu-python3:latest
LABEL maintainer="FNNDSC <dev@babymri.org>"

ENV FREESURFER_HOME="/usr/local/freesurfer"

ARG UID=1001
ENV UID=$UID
ARG LOCALE="en_US.UTF-8"
ENV DEBIAN_FRONTEND=noninteractive

ENV APPROOT="/usr/src/fshack_infant"
COPY ["fshack_infant/", "requirements.txt", "license.txt", "$APPROOT/"]
WORKDIR $APPROOT

RUN pip install -r requirements.txt                                                \
    && apt-get update -q                                                           \
    && apt-get -qq install bc binutils libgomp1 perl psmisc curl tar tcsh uuid-dev \
       vim-common libjpeg62-dev libglu1-mesa libxmu6 libglib2.0-0 qt5-default      \
    && apt-get install -y locales                                                  \
    && export LANGUAGE="$LOCALE"                                                   \
    && export LANG="$LOCALE"                                                       \
    && export LC_ALL="$LOCALE"                                                     \
    && locale-gen "$LOCALE"                                                        \
    && dpkg-reconfigure locales                                                    \
    && useradd -u "$UID" -ms /bin/bash localuser

ENV PATH="$FREESURFER_HOME/bin:$FREESURFER_HOME/fsfast/bin:$FREESURFER_HOME/tktools:$FREESURFER_HOME/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:" \
    MNI_DIR="$FREESURFER_HOME/mni"                                                 \
    MINC_LIB_DIR="$FREESURFER_HOME/mni/lib"                                        \
    MNI_DATAPATH="$FREESURFER_HOME/mni/data"                                       \
    MINC_BIN_DIR="$FREESURFER_HOME/mni/bin"                                        \
    PERL5LIB="$FREESURFER_HOME/mni/share/perl5"                                    \
    MNI_PERL5LIB="$FREESURFER_HOME/mni/share/perl5"                                \
    FUNCTIONALS_DIR="$FREESURFER_HOME/sessions"                                    \
    LOCAL_DIR="$FREESURFER_HOME/local"                                             \
    FMRI_ANALYSIS_DIR="$FREESURFER_HOME/fsfast"                                    \
    FSFAST_HOME="$FREESURFER_HOME/fsfast"                                          \
    SUBJECTS_DIR="/outgoing"                                                       \
    FSF_OUTPUT_FORMAT="nii.gz"

CMD ["fshack_infant.py", "--help"]
