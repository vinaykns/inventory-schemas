import yaml
import json
import re
import sys
import statistics
import time
from jsonschema import validate
import jsonschema

import helper

def get_instance(schema_dict):
    validator = jsonschema.validators.validator_for(schema_dict)
    validator.check_schema(schema_dict)
    instance = validator(schema_dict)
    return instance

# validation2 does validation with caching
def validation2(sample_path, instance):
    start = time.time()
    with open(sample_path, 'r') as sample_data:
        sample_dict = json.load(sample_data)
        write_to_null = open('/dev/null', 'w')
        write_to_null.write(json.dumps(sample_dict))
        samples = sample_dict['system_profiles']
        data = {}
        for sample in samples:
            data['system_profile'] = sample
            instance.validate(data)

        end = time.time()
        return (end-start) * 1000

# marshmallow_validation function runs the validation test against the schema.
def marshmallow_validation(sample_path):
    schema = helper.SystemProfileSchema()
    start = time.time()
    f = open(sample_path, 'r').read()
    data = json.loads(f)
    samples = data['system_profiles']
    for sample in samples:
        result = schema.validate(sample)
        if result:
            print(result)

    write_to_null = open('/dev/null', 'w')
    write_to_null.write(json.dumps(data))
    end = time.time()
    diff = (end - start) * 1000
    print(f'Completed validation test, took {diff} ms')
    return diff


def main():
    plain_schema_path = sys.argv[1]
    regex_schema_path = sys.argv[2]
    sample_path = sys.argv[3]

    print(plain_schema_path, regex_schema_path, sample_path)
    result1 = []
    print("Execute donothing codeblock")
    for _ in range(10):
        result = helper.donothing(sample_path)
        result1.append(result)
    
    print("Completed running donothing function")
    print(result1)
    helper.print_stats(result1)

    print("Execute validation with primitive schema")
    result2 = []
    for _ in range(10):
        with open(plain_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result2.append(result)

    print("Completed running the validation with primitive schema")
    result2 = helper.get_validation_overhead(result1, result2)
    helper.print_stats(result2)

    print("Execute validation with regex schema")
    result3 = []
    for _ in range(10):
        with open(regex_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result3.append(result)
    
    print("Completed running the validation with regex schema")
    result3 = helper.get_validation_overhead(result1, result3)
    helper.print_stats(result3)

    count = 0
    for i in range(10):
        if result3[i] > result2[i]:
            count +=1 
    
    print(f'Number of samples where regex validation is taking more time {count} \
        vs primitive validation {10 - count}')
    
    print("Execute validation with marshmallow schema")
    result4 = []
    for _ in range(10):
        result4.append(marshmallow_validation(sample_path))
    
    print("Completed running the validation with marshmallow")
    result4 = helper.get_validation_overhead(result1, result4)
    helper.print_stats(result4)

    primistomarsh = statistics.mean(result2) / statistics.mean(result4)
    regexistomarsh = statistics.mean(result3) / statistics.mean(result4)
    print(f'primistomarsh: {primistomarsh}, regexistomarsh: {regexistomarsh}')

        
if __name__ == "__main__":
    main()