#!/bin/bash
set -e

cd ./tools/
source venv/bin/activate

python tester4.py ../samples/data.json
#python tester3.py ../schemas/system_profile/v1.yaml ../samples/data.json
#python tester2.py ../schemas/system_profile/v1.yaml ../samples/data.json