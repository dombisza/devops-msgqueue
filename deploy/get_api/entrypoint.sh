#!/bin/bash
# https://docs.docker.com/config/containers/multi-service_container/
set -m

exec flask run -h 0.0.0.0 -p 5001 --reload &

fg %1
