#!/bin/bash
OS=$(uname -o)
BUILD="docker build"

if [[ $OS == "Msys" ]]; then
    BUILD="winpty ${BUILD}"
fi

${BUILD} -t registry.blacklibrary.ru/face-check:dev -f Dockerfile . $@

