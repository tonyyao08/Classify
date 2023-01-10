import requests
import json
import pandas as pd

apiKey = "da2-tkzuvhzfe5etrmisvfchmr7sia"

query = """query {
  listProjects {
    items {
      createdAt
      id
      imageBucket
      isTraining
      labels
      owner
      projectName
      updatedAt
    }
  }
}"""

create_image_query = """mutation {
  createImage(input: {imageKey: "wisconsin-quarter.jpg", projectID: "5a9d5546-a6f5-4be1-851d-fa704435e674"}) {
    id
    _version
    createdAt
    updatedAt
    _lastChangedAt
    projectID
    _deleted
    imageKey
  }
}"""

final_image = "wisconsin-quarter.jpg"
proj_id = "2a478f48-2a93-4501-9627-bcad74587cf5"
label_name = "NEW COIN 8"
user_generated = "false"

create_image_query = f"""mutation {{ 
            createImage(input: {{imageKey: "{final_image}", projectID: "{proj_id}", label: "{label_name}", userGenerated: {user_generated}}}) {{ 
                id 
                _version
                createdAt
                updatedAt
                _lastChangedAt
                projectID
                _deleted
                imageKey
                label
                rekognitionMeta
                userGenerated
            }}
            }}"""

url = 'https://ztgryu55q5hs3o6tff5lh3qovq.appsync-api.us-east-1.amazonaws.com/graphql'

data = {"query": create_image_query}
json_data = json.dumps(data)
header = {'X-API-Key': apiKey}

response = requests.post(url=url, headers=header, data=json_data)

# print(r.status_code)
# print(r.text)

json_data = json.loads(response.text)

print(json_data)


# send

url = 'https://ztgryu55q5hs3o6tff5lh3qovq.appsync-api.us-east-1.amazonaws.com/graphql'
r = requests.post(url, data=query)
