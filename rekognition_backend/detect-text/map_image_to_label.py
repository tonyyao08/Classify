import json


def map_image_to_label(detect_text_response, image_file):
    # local json database for testing adding labels
    label_database = "add_label_database.json"
    # local json database for testing mapping images
    bucket_database = "map_image_database.json"

    with open(label_database) as lf:
        labels_list = json.load(lf)

    with open(bucket_database) as pf:
        prev_database = json.load(pf)

    name = "Unknown"
    labels = [d['label'] for d in labels_list]
    for entry in labels:
        text_arr = entry.get("matchingText")
        for text in text_arr:
            if text.upper() in detect_text_response:
                name = entry.get("name")
    
    new_bucket = {image_file:name}
    prev_database.append(new_bucket)
    
    with open(bucket_database, 'w', encoding='utf-8') as f:
        json.dump(prev_database, f, indent=4)


# example detect_text response ran on a new york coin image
detect_text_response = ['SARATOGA', 'MEN YORK', 'British', 'Surrender', '1777', '2015', 'SARATOGA', 'MEN', 'YORK', 'British', 'Surrender', '1777', '2015']
# name of new york image from detect_text response
image_file = "newyork-quarter.jpg"

# example call to map a new york image to a label
map_image_to_label(detect_text_response, image_file)