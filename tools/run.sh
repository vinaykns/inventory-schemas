#!/bin/bash
set -e

cd ./tools/
source venv/bin/activate

python tester.py ../schemas/system_profile/v1.yaml ../schemas/system_profile/v2.yaml ../samples/data.json