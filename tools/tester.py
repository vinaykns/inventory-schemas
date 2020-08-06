import cProfile
import fastjsonschema
import yaml
import json
import re
import sys
import statistics
import time
from jsonschema import validate
import jsonschema
from cerberus import Validator

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

def cerberus_validation(plain_schema_path, sample_path, result1):
    result5 = []
    print("Execute cerberus validation")
    for _ in range(25):
        with open(plain_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = Validator(schema_dict)
            result = validation2(sample_path, instance)
        
        result5.append(result)
    
    print("Completed running the validation with cerberus library")
    result5 = helper.get_validation_overhead(result1, result5)
    print(result5)
    helper.print_stats(result5)
    return result5

def validate3(sample_path, instance):
    start = time.time()
    with open(sample_path, 'r') as sample_data:
        sample_dict = json.load(sample_data)
        write_to_null = open('/dev/null', 'w')
        write_to_null.write(json.dumps(sample_dict))
        samples = sample_dict['system_profiles']
        data = {}
        for sample in samples:
            data['system_profile'] = sample
            instance(data)

        end = time.time()
        return (end-start) * 1000


def fastjsonschema_validation(plain_schema_path, sample_path, result1):
    result6 = []
    print("Execute fastjsonschema validation")
    for _ in range(25):
        with open(plain_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            validate = fastjsonschema.compile(schema_dict)
            result = validate3(sample_path, validate)

        result6.append(result)
    
    print("Completed running the validation with fastjson library")
    print(result6)
    result6 = helper.get_validation_overhead(result1, result6)
    print(result6)
    helper.print_stats(result6)
    return result6


# dryrun runs the dry run which is used to compute just the validation overhead.
def dryrun(sample_path):
    result1 = []
    print("Execute donothing codeblock")
    for _ in range(25):
        result = helper.donothing(sample_path)
        result1.append(result)
    
    print("Completed running donothing function")
    print(result1)
    helper.print_stats(result1)
    return result1

def plainvalidation(plain_schema_path, sample_path, result1):
    print("Execute validation with primitive schema")
    result2 = []
    for _ in range(25):
        with open(plain_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result2.append(result)

    print("Completed running the validation with primitive schema")
    result2 = helper.get_validation_overhead(result1, result2)
    print(result2)
    helper.print_stats(result2)
    return result2


def regexvalidation(regex_schema_path, sample_path, result1):
    print("Execute validation with regex schema")
    result3 = []
    for _ in range(25):
        with open(regex_schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result3.append(result)
    
    print("Completed running the validation with regex schema")
    result3 = helper.get_validation_overhead(result1, result3)
    print(result3)
    helper.print_stats(result3)
    return result3

def marshmallow_schema(sample_path, result1):
    print("Execute validation with marshmallow schema")
    result4 = []
    for _ in range(25):
        result4.append(marshmallow_validation(sample_path))
    
    print("Completed running the validation with marshmallow")
    result4 = helper.get_validation_overhead(result1, result4)
    print(result4)
    helper.print_stats(result4)
    return result4

def get_statistics(donothing_result, plain_result, regex_result, marshmallow_result, fastschema_result):
    count = 0
    for i in range(25):
        if regex_result[i] > plain_result[i]:
            count +=1 
    
    print(f'Number of samples where regex validation is taking more time {count} \
        vs primitive validation {25 - count}')
    
    primistomarsh = statistics.mean(plain_result) / statistics.mean(marshmallow_result)
    regexistomarsh = statistics.mean(regex_result) / statistics.mean(marshmallow_result)
    primistofast = statistics.mean(plain_result) / statistics.mean(fastschema_result)
    marshmallowistofast = statistics.mean(marshmallow_result) / statistics.mean(fastschema_result)
    print(f'prim:marsh: {primistomarsh}, regex:marsh: {regexistomarsh}, prim:fast: {primistofast}, marshmallow:fast: {marshmallowistofast}')


def main():
    plain_schema_path = sys.argv[1]
    regex_schema_path = sys.argv[2]
    sample_path = sys.argv[3]
    print(plain_schema_path, regex_schema_path, sample_path)

    result1 = dryrun(sample_path)

    result2 = plainvalidation(plain_schema_path, sample_path, result1)
    
    result3 = regexvalidation(regex_schema_path, sample_path, result1)

    result4 = marshmallow_schema(sample_path, result1)

    result6 = fastjsonschema_validation(plain_schema_path, sample_path, result1)

    get_statistics(result1, result2, result3, result4, result6)

if __name__ == "__main__":
    main()