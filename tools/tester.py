import yaml
import json
import sys
import statistics
import time
from jsonschema import validate
import jsonschema

def get_instance(schema_dict):
    validator = jsonschema.validators.validator_for(schema_dict)
    validator.check_schema(schema_dict)
    instance = validator(schema_dict)
    return instance

# validation1 does validation without caching
def validation1(sample_path, schema_path):
    with open(sample_path, 'r') as sample_data:
        with open(schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            sample_dict = json.load(sample_data)
            start = time.time()
            validator = jsonschema.validators.validator_for(schema_dict)
            validator.check_schema(schema_dict)
            instance = validator(schema_dict)
            instance.validate(sample_dict)
            end = time.time()
            diff = (end - start) * 1000
            return diff

# validation2 does validation with caching
def validation2(sample_path, instance):
    with open(sample_path, 'r') as sample_data:
        sample_dict = json.load(sample_data)
        start = time.time()
        instance.validate(sample_dict)
        end = time.time()
        diff = (end - start) * 1000
        return diff

def print_stats(numbers):
    print("\tBEST  ", min(numbers))
    print("\tMEDIAN", statistics.median(numbers))
    print("\tMEAN  ", statistics.mean(numbers))
    print("\tSTDEV ", statistics.stdev(numbers))

def main():
    result1 = []
    result2 = []
    schema_path = sys.argv[1]
    sample_path = sys.argv[2]
    with open(schema_path, 'r') as schema_data:
        schema_dict = yaml.safe_load(schema_data)
        instance = get_instance(schema_dict)
    for _ in range(10):
        result1.append(validation1(sample_path, schema_path))
        result2.append(validation2(sample_path, instance))
    
    print("Running the validation without caching")
    print_stats(result1)
    print('\n')
    print("Running the validation with caching")
    print_stats(result2)
    change = min(result1) / min(result2)
    print("Improved by:", change, "times")

if __name__ == "__main__":
    main()
