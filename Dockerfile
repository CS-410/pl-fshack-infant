# Docker file for fshack_infant ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-fshack-infant .
#
# In the case of a proxy (located at say 10.41.13.4:3128), do:
#
#    export PROXY="http://10.41.13.4:3128"
#    docker build --build-arg http_proxy=${PROXY} --build-arg UID=$UID -t local/pl-fshack-infant .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-fshack-infant
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-fshack-infant
#



FROM fnndsc/ubuntu-python3:latest
# FROM fnndsc/centos-python3:latest
LABEL maintainer="dev@babymri.org"

ARG UID=1001
ARG IFSURL="https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/infant/freesurfer-linux-centos7_x86_64-7.1.1-infant.tar.gz"
ENV APPROOT="/usr/src/fshack_infant"
ENV IFSROOT="/usr/local/infant_freesurfer"
ENV UID=$UID DEBIAN_FRONTEND=noninteractive
COPY ["fshack_infant/", "requirements.txt", "license.txt", "${APPROOT}/"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt                           \
    && apt-get update -q                                      \
    && apt-get -qq install bc binutils libgomp1 perl psmisc   \
    curl tar tcsh uuid-dev vim-common libjpeg62-dev libxmu6   \
    libglu1-mesa libglib2.0-0 qt5-default                     \
    && curl $IFSURL | tar -C /usr/local -xz                   \
    && mv license.txt $IFSROOT                                \
    && apt-get install -y locales                             \
    && export LANGUAGE=en_US.UTF-8                            \
    && export LANG=en_US.UTF-8                                \
    && export LC_ALL=en_US.UTF-8                              \
    && locale-gen en_US.UTF-8                                 \
    && dpkg-reconfigure locales                               \
    && useradd -u $UID -ms /bin/bash localuser

ENV PATH="$IFSROOT/bin: $IFSROOT/fsfast/bin:$IFSROOT/tktools:$IFSROOT/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:" \
    FREESURFER_HOME="$IFSROOT"                                \
    SUBJECTS_DIR="/outgoing"                                  \
    MINC_LIB_DIR="$IFSROOT/mni/lib"                           \
    MNI_DATAPATH="$IFSROOT/mni/data"                          \
    PERL5LIB="$IFSROOT/mni/share/perl5"                       \
    MINC_BIN_DIR="$IFSROOT/mni/bin"                           \
    MNI_PERL5LIB="$IFSROOT/mni/share/perl5"                   \
    FMRI_ANALYSIS_DIR="$IFSROOT/fsfast"                       \
    FUNCTIONALS_DIR="$IFSROOT/sessions"                       \
    LOCAL_DIR="$IFSROOT/local"                                \
    FSFAST_HOME="$IFSROOT/fsfast"                             \
    MNI_DIR="$IFSROOT/mni"                                    \
    FSF_OUTPUT_FORMAT="nii.gz"

CMD ["fshack_infant.py", "--help"]
