from datetime import date
import json
from marshmallow import Schema, fields, pprint
from marshmallow import validate
from marshmallow import validates
from marshmallow import ValidationError
import os
import sys
import statistics
import time


def check_empty_keys(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "":
                return False
            if not check_empty_keys(value):
                return False
    elif isinstance(data, list):
        for value in data:
            if not check_empty_keys(value):
                return False

    return True

class DiskDeviceSchema(Schema):
    device = fields.Str(validate=validate.Length(max=2048))
    label = fields.Str(validate=validate.Length(max=1024))
    options = fields.Dict(validate=check_empty_keys)
    mount_point = fields.Str(validate=validate.Length(max=2048))
    type = fields.Str(validate=validate.Length(max=256))


class YumRepoSchema(Schema):
    id = fields.Str(validate=validate.Length(max=256))
    name = fields.Str(validate=validate.Length(max=1024))
    gpgcheck = fields.Bool()
    enabled = fields.Bool()
    base_url = fields.Str(validate=validate.Length(max=2048))


class DnfModuleSchema(Schema):
    name = fields.Str(validate=validate.Length(max=128))
    stream = fields.Str(validate=validate.Length(max=128))


class InstalledProductSchema(Schema):
    name = fields.Str(validate=validate.Length(max=512))
    id = fields.Str(validate=validate.Length(max=64))
    status = fields.Str(validate=validate.Length(max=256))


class NetworkInterfaceSchema(Schema):
    ipv4_addresses = fields.List(fields.Str())
    ipv6_addresses = fields.List(fields.Str())
    state = fields.Str(validate=validate.Length(max=25))
    mtu = fields.Int()
    mac_address = fields.Str(validate=validate.Length(max=59))
    name = fields.Str(validate=validate.Length(min=1, max=50))
    type = fields.Str(validate=validate.Length(max=18))


class SystemProfileSchema(Schema):
    number_of_cpus = fields.Int()
    number_of_sockets = fields.Int()
    cores_per_socket = fields.Int()
    system_memory_bytes = fields.Int()
    infrastructure_type = fields.Str(validate=validate.Length(max=100))
    infrastructure_vendor = fields.Str(validate=validate.Length(max=100))
    network_interfaces = fields.List(fields.Nested(NetworkInterfaceSchema()))
    disk_devices = fields.List(fields.Nested(DiskDeviceSchema()))
    bios_vendor = fields.Str(validate=validate.Length(max=100))
    bios_version = fields.Str(validate=validate.Length(max=100))
    bios_release_date = fields.Str(validate=validate.Length(max=50))
    cpu_flags = fields.List(fields.Str(validate=validate.Length(max=30)))
    os_release = fields.Str(validate=validate.Length(max=100))
    os_kernel_version = fields.Str(validate=validate.Length(max=100))
    arch = fields.Str(validate=validate.Length(max=50))
    kernel_modules = fields.List(fields.Str(validate=validate.Length(max=255)))
    last_boot_time = fields.Str(validate=validate.Length(max=50))
    running_processes = fields.List(fields.Str(validate=validate.Length(max=1000)))
    subscription_status = fields.Str(validate=validate.Length(max=100))
    subscription_auto_attach = fields.Str(validate=validate.Length(max=100))
    katello_agent_running = fields.Bool()
    satellite_managed = fields.Bool()
    cloud_provider = fields.Str(validate=validate.Length(max=100))
    yum_repos = fields.List(fields.Nested(YumRepoSchema()))
    dnf_modules = fields.List(fields.Nested(DnfModuleSchema()))
    installed_products = fields.List(fields.Nested(InstalledProductSchema()))
    insights_client_version = fields.Str(validate=validate.Length(max=50))
    insights_egg_version = fields.Str(validate=validate.Length(max=50))
    captured_date = fields.Str(validate=validate.Length(max=32))
    installed_packages = fields.List(fields.Str(validate=validate.Length(max=512)))
    installed_services = fields.List(fields.Str(validate=validate.Length(max=512)))
    enabled_services = fields.List(fields.Str(validate=validate.Length(max=512)))
    sap_system = fields.Bool()

def print_stats(numbers):
    print("\tBEST  ", min(numbers))
    print("\tMEDIAN", statistics.median(numbers))
    print("\tMEAN  ", statistics.mean(numbers))
    print("\tSTDEV ", statistics.stdev(numbers))

# validation function runs the validation test against the schema.
def validation(sample_path):
    schema = SystemProfileSchema()
    f = open(sample_path, 'r').read()
    data = json.loads(f)
    samples = data['system_profiles']
    start = time.time()

    for sample in samples:
        result = schema.validate(sample['system_profile'])
        if result:
            print(result)
    
    write_to_null = open('/dev/null', 'w')
    write_to_null.write(json.dumps(data))
    end = time.time()
    diff = (end - start) * 1000
    print(f'Completed validation test, took {diff} ms')
    return diff

# this script validates the sample data against the marshmallow schema.
def main():
    sample_path = sys.argv[1]
    results = []
    for _ in range(25):
        results.append(validation(sample_path))
    
    print(results)
    print_stats(results)


if __name__ == "__main__":
    main()

