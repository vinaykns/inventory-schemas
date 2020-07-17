#!/bin/bash
set -e

cd ./tools/
source venv/bin/activate
python tester.py ../schemas/system_profile/v1.yaml ../samples/sample.json
