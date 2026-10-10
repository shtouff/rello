#!/bin/bash -e

# extract version from python
tag=$(python -c 'from rello.info import info_data; print(info_data["version"])')
name=rello

docker buildx build --output type=docker --provenance=false -t shtouff/$name:$tag .

echo docker push shtouff/$name:$tag
