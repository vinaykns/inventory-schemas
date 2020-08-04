# Cloud Platform Inventory Schemas #

This is a place to store API specifications and schemas for the [Host Inventory]. Currently it is used only for [System
Profile].

This is an initial draft and any technical details may change over time. Published early to allow work and discussion on
the actual System Profile shape.

## Technical Details ##

[System Profile] specification is written in YAML containing an [OpenAPI 3.0](https://swagger.io/specification/) definition schema. All entities are under _$def_ root key, internal references (_$ref_) use relative referencing (_#/$def/entity_).

Document version is reflected in the filename (_v1.yaml_) and under _$version_ root key. _$id_ is a file name used in
the Host Inventory.

## To do ##

- [ ] Write more to do items


[Host Inventory]: https://github.com/RedHatInsights/insights-host-inventory/
[System Profile]: schemas/system_profile/
[OpenAPI 3.0]: https://swagger.io/specification/


## How to run ##
1. Please check your email for the host record generator data.
1. From a massive host record generator data file extract all the system_profiles by running `cd $(pwd)/inventory-schemas/samples && python3 extract_sys_profile.py $path_to_massive_file`
2. Initialize venv by running `bash tools/init.sh` after entering into the `inventory-schemas` directory.
3. Then do `bash tools/run.sh` to see the performance comparision results with using regex patterns, jsonschema and marshmallow libraries.
