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
    timediffs = []
    with open(sample_path, 'r') as sample_data:
        with open(schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            sample_dict = json.load(sample_data)
            start = time.time()
            samples = sample_dict['system_profiles']
            for sample in samples:
                instance = get_instance(schema_dict)
                instance.validate(sample)
                end = time.time()
                timediffs.append((end-start) * 1000)
                start = end
            
            print("Total samples:", len(samples), "Total time diffs:", len(timediffs))
            return timediffs

# validation2 does validation with caching
def validation2(sample_path, instance):
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
    result3 = []
    schema_path = sys.argv[1]
    sample_path = sys.argv[2]

    for _ in range(25):
        with open(schema_path, 'r') as schema_data:
            schema_dict = yaml.safe_load(schema_data)
            instance = get_instance(schema_dict)
            result = validation2(sample_path, instance)
        
        result3.append(result)

    print("Running the validation with regex schema and caching along with")
    print(result3)
    print_stats(result3)

if __name__ == "__main__":
    main()