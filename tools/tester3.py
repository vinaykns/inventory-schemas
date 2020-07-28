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
    start = time.time()
    with open(sample_path, 'r') as sample_data:
        sample_dict = json.load(sample_data)
        write_to_null = open('/dev/null', 'w')
        write_to_null.write(json.dumps(sample_dict))
        samples = sample_dict['system_profiles']
        for sample in samples:    
            instance.validate(sample['system_profile'])

        end = time.time()
        print(f'validation took {(end-start)*1000} ms')
        return (end-start) * 1000           

def print_stats(numbers):
    print("\tBEST  ", min(numbers))
    print("\tMEDIAN", statistics.median(numbers))
    print("\tMEAN  ", statistics.mean(numbers))
    print("\tSTDEV ", statistics.stdev(numbers))

def main():
    result3 = []
    schema_path = sys.argv[1]
    sample_path = sys.argv[2]

    for _ in range(25):
        with open(schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result3.append(result)

    print("Completed running the validation with regex schema")
    print(result3)
    print_stats(result3)

if __name__ == "__main__":
    main()