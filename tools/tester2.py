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

# validation2 does validation with caching
def validation2(sample_path, instance):
    #timediffs = []
    with open(sample_path, 'r') as sample_data:
        sample_dict = json.load(sample_data)
        start = time.time()
        samples = sample_dict['system_profiles']
        for sample in samples:
            instance.validate(sample)

        end = time.time()
        return (end-start) * 1000           

def print_stats(numbers):
    print("\tBEST  ", min(numbers))
    print("\tMEDIAN", statistics.median(numbers))
    print("\tMEAN  ", statistics.mean(numbers))
    print("\tSTDEV ", statistics.stdev(numbers))

def main():
    result2 = []
    schema_path = sys.argv[1]
    sample_path = sys.argv[2]

    for _ in range(25):
        with open(schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result2.append(result)
    
    print("Running the validation with caching")
    print(result2)
    print_stats(result2)

if __name__ == "__main__":
    main()