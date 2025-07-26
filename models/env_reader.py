from pathlib import Path

def env_reader(environment_dict):

    dataset_path = Path(environment_dict["DATASET_PATH"])
    frequency = environment_dict["FREQUENCY"]
    seasonality = int(environment_dict["SEASONALITY"])
    if environment_dict.get("OUTPUT_DIR", None) is not None:
        OUTPUT_DIR = Path(environment_dict["OUTPUT_DIR"])
    else:
        OUTPUT_DIR = Path().resolve().parent.parent / "_output"
    if environment_dict.get("TEST_SPLIT", None) is not None:
        # Seasonal mode would instruct the classes to calculate test_split
        # such that the testing data is just the last season of values
        # and the rest is used as training data.
        if environment_dict["TEST_SPLIT"] == "seasonal":
            test_split = "seasonal"
        else:
            test_split = float(environment_dict["TEST_SPLIT"])
    else:
        test_split = 0.2
    
    return (dataset_path, frequency, seasonality, OUTPUT_DIR, test_split)