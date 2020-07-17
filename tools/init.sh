#!/bin/bash
set -e

cd ./tools/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
