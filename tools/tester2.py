import yaml
import json
import sys
import statistics
import time
from jsonschema import validate
import jsonschema

# get_instance returns the schema instance from schema object.
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

# donothing does nothing much except loading a file, reading it and streaming data to /dev/null
def donothing(sample_path):
    start = time.time()
    sample_data = open(sample_path, 'r').read()
    sample_dict = json.loads(sample_data)
    write_to_null = open('/dev/null', 'w')
    write_to_null.write(json.dumps(sample_dict))
    end = time.time()
    diff = (end - start) * 1000
    print(f'function donothing took {diff} ms')
    return diff

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
    _ = sys.argv[1]
    sample_path = sys.argv[2]
    
    # this block basically invokes the donothing function.
    for _ in range(25):
        result = donothing(sample_path)
        result2.append(result)

    print("Completed running donothing function")
    print(result2)
    print_stats(result2)

if __name__ == "__main__":
    main()