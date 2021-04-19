#!/bin/bash

set -e

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    exec jhsingle-native-proxy --destport {{ web_app.port }} -- {{ web_app.cmdline }}
else
    exec jhsingle-native-proxy --destport {{ web_app.port }} --authtype none -- {{ web_app.cmdline }}
fi
