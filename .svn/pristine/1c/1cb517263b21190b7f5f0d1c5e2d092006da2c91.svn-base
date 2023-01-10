import json


# For new images, simualtes user adding a label to detect image in the future
def add_label(name, matching_text):
    # local json database for testing adding labels
    label_database = "mock_label_database.json"

    with open(label_database) as pf:
        prev_database = json.load(pf)

    new_label = {"label": {"name": name, "matchingText": matching_text}}
    prev_database.append(new_label)
    with open(label_database, 'w') as f:
        json.dump(prev_database, f, indent=4)


# user passes in label name
label_name = "Wisconsin"
# user passes in text to help identify this image in future
matching_text = ["wisconsin"]
add_label(label_name, matching_text)