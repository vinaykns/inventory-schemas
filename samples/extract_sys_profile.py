#!/usr/bin/env python3

import json

profiles = []
sys_profiles = {}
f = open('sample.original.json', 'r').read()
data = json.loads(f)
for each in data:
    _system_profile = each['_system_profile']
    result = _system_profile['results'][0]
    system_profile = result['system_profile']
    profiles.append(system_profile)

sys_profiles['system_profiles'] = profiles

f = open('data.json', 'w')
f.write(json.dumps(sys_profiles))
f.close()
