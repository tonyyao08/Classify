from queue import Queue
import threading
from threading import Thread, Event
from typing import Union, List
from typing_extensions import TypedDict
import websocket
import requests
import json
import rel
import boto3
from botocore.exceptions import ClientError
import io
from image import Image
from base64 import b64encode, decode
from datetime import datetime
from uuid import uuid4
import logging
from concurrent.futures import ThreadPoolExecutor


class ClassifyProject(TypedDict):
    projectName: str
    id: str
    isTraining: bool
    _version: int


class QueryBuilder:

    @staticmethod
    def buildListProjectsQuery():
        query = """query {
            listProjects {
                items {
                    id
                    projectName
                    isTraining
                    _version
                }
            }
        }"""
        return query

    @staticmethod
    def buildCreateImageQuery(projectID: str, imageKey: str, label: Union[str, None] = None, userGenerated: Union[bool, None] = None):
        label_attr = f", label: \"{label}\"" if label != None else ""
        userGenerated_val = (
            "true" if userGenerated else "false") if userGenerated is not None else ""
        userGenerated_attr = f""", userGenerated: {userGenerated_val}""" if userGenerated != None else ""
        query = f"""mutation {{ 
            createImage(input: {{imageKey: "{imageKey}", projectID: "{projectID}"{label_attr}{userGenerated_attr}}}) {{ 
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
        return query

    @staticmethod
    def buildListImageQuery(projectID: str, userGenerated: Union[bool, None] = None):
        userGenerated_attr = f""", userGenerated: {{eq: {"true" if userGenerated else "false"}}}""" if userGenerated != None else ""
        labelAndMetaExists = f""", label: {{size: {{gt: 0}} }}, rekognitionMeta: {{size: {{gt: 0}}, attributeExists: true}}"""
        # listImages(filter: {{projectID: {{eq: "{projectID}"}}{userGenerated_attr}{labelAndMetaExists}}}) {{
        #         items {{
        #             id
        #             userGenerated
        #             label
        #             rekognitionMeta
        #         }}
        #     }}

        query = f"""query {{
            getProject(id: "{projectID}") {{
                images(filter: {userGenerated_attr}{labelAndMetaExists}) {{
                    items {{
                        rekognitionMeta
                        label
                    }}
                }}
            }}
        }}"""
        return query

    @staticmethod
    def buildUpdateTrainingQuery(projectID: str, projectVersion: int, isTraining: bool):
        query = f"""mutation {{
            updateProject(input: {{isTraining: {"true" if isTraining else "false"}, id: "{projectID}", _version:{projectVersion}}}) {{
                _deleted
                _lastChangedAt
                _version
                createdAt
                id
                imageBucket
                isTraining
                labels
                owner
                projectName
                updatedAt
            }}
        }}
        """
        return query


class Communicator:

    def __init__(self):
        self.projectName = None
        self.mode = None
        self.s3Client = boto3.client('s3')
        self.projectID = None
        self.projectVersion = None
        self.apiKey = "da2-tkzuvhzfe5etrmisvfchmr7sia"
        self.s3Bucket = "mycoins"
        self.endpoint = "https://ztgryu55q5hs3o6tff5lh3qovq.appsync-api.us-east-1.amazonaws.com/graphql"
        self.projectListener = None
        self.queue = Queue()
        self.stopEvent = Event()
        self.workerThread = Thread(target=self.processQueue)
        self.workerThread.setDaemon(True)
        self.workerThread.start()
        self.projectListener = self.ProjectListener(self)

    # METHODS FOR PROCESSING REQUESTS TO THE GRAPHQL ENDPOINT

    def processQueue(self):
        while not self.stopEvent.isSet() or not self.queue.all_tasks_done:
            try:
                element = self.queue.get(block=False)
                if type(element) == str:
                    # Database Request
                    query = element
                    self.sendRequest(query)
                else:
                    # Upload to S3 Request
                    image = element
                    logging.info(f"BEGIN UPLOAD TO S3 ({image.imageKey})")
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        futures = [executor.submit(lambda version: self.uploadFileObject(
                            version, image), v) for v in image.versions]
                    logging.info(f"END UPLOAD TO S3 ({image.imageKey})")
                self.queue.task_done()
            except:
                pass

    def uploadFileObject(self, version, image: Image):
        (versionName, _) = version
        logging.info(f"BEGIN WRITE TO DISK ({image.imageKey}, {versionName})")
        image.writeToDisk(version=versionName)
        logging.info(f"END WRITE TO DISK ({image.imageKey}, {versionName})")
        logging.info(f"BEGIN UPLOAD TO S3 ({image.imageKey}, {versionName})")
        self.s3Client.upload_file(
            image.getFullPath(versionName), self.s3Bucket, image.getFilename(versionName))
        logging.info(f"END UPLOAD TO S3 ({image.imageKey}, {versionName})")

    def sendRequest(self, query: str) -> dict:
        data = {"query": query}
        header = {'X-API-Key': self.apiKey}
        response = requests.post(
            url=self.endpoint, headers=header, data=json.dumps(data))
        return json.loads(response.text)

    def processQuery(self, query: str, blocking: bool) -> Union[None, bool]:
        if blocking:
            return self.sendRequest(query)
        else:
            self.queue.put(query)
            return None

    def getAvailableProjects(self) -> List[ClassifyProject]:
        query = QueryBuilder.buildListProjectsQuery()
        response = self.processQuery(query, blocking=True)
        projects = response.get('data').get('listProjects').get('items')
        return projects

    def getProjectByID(self, projectID):
        projects = self.getAvailableProjects()
        return next((x for x in projects if x.get('id') == projectID), None)

    def getProjectByName(self, projectName) -> ClassifyProject:
        projects = self.getAvailableProjects()
        return next((x for x in projects if x.get('projectName') == projectName), None)

    def mapProjectNameToID(self, projectName: str) -> Union[str, None]:
        project = self.getProjectByName(projectName)
        return project.get('id') if project != None else None

    def setCurrentProjectByName(self, projectName: str):
        self.setCurrentProjectByID(self.mapProjectNameToID(projectName))

    def setProjectMode(self, isTraining: bool):
        self.mode = "TRAIN" if isTraining else "CLASSIFY"
        if not isTraining:
            self.labels = self.getImages(True)
        print(f"PROJECT IN {self.mode} MODE")

    def getProjectMode(self):
        return self.mode

    def updateProjectMode(self, isTraining: bool):
        query = QueryBuilder.buildUpdateTrainingQuery(
            self.projectID, self.projectVersion, isTraining)
        response = self.processQuery(query, blocking=True)
        if response is not None:
            self.projectVersion = response.get("_version")

    def setCurrentProjectByID(self, projectID: str):
        project = self.getProjectByID(projectID)
        self.projectID = project.get('id')
        self.projectVersion = project.get('_version')
        if project.get('isTraining') == None:
            self.updateProjectMode(True)
        else:
            self.setProjectMode(project.get('isTraining'))

    def getImages(self, userGenerated: Union[bool, None] = None) -> List[dict]:
        query = QueryBuilder.buildListImageQuery(
            projectID=self.projectID, userGenerated=userGenerated)
        response = self.processQuery(query, blocking=True)
        images = response.get('data').get(
            'getProject').get('images').get('items')
        return images

    def sendImageToDatabase(self, image: Image, label: Union[str, None], userGenerated: Union[bool, None] = None) -> None:
        query = QueryBuilder.buildCreateImageQuery(
            self.projectID, image.getFilename(), label, userGenerated)
        self.processQuery(query, blocking=False)

    def uploadToS3(self, image: Image, blocking=True):
        if blocking:
            logging.info(f"BEGIN UPLOAD TO S3 ({image.imageKey})")
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(lambda version: self.uploadFileObject(
                    version, image), v) for v in image.versions]
            logging.info(f"END UPLOAD TO S3 ({image.imageKey})")
        else:
            self.queue.put(image)

    def destroy(self):
        self.queue.join()
        self.stopEvent.set()
        self.workerThread.join()
        if self.projectListener:
            self.projectListener.closeListener()

    class ProjectListener:
        def __init__(self, communicator):
            self.communicator = communicator
            self.wsURL = communicator.endpoint.replace(
                'https', 'wss').replace('appsync-api', 'appsync-realtime-api')
            self.host = communicator.endpoint.replace(
                'https://', '').replace('/graphql', '')
            self.subscriptionID = str(uuid4())
            self.timeoutTimer = None
            self.timeoutInterval = 10

            self.header = {
                'host': self.host,
                'x-api-key': communicator.apiKey
            }

            self.connectionURL = self.wsURL + '?header=' + \
                self.encodeHeader(self.header) + '&payload=e30='
            self.webSocket = websocket.WebSocketApp(self.connectionURL,
                                                    subprotocols=[
                                                        'graphql-ws'],
                                                    on_open=lambda ws: self.onOpen(),
                                                    on_message=lambda ws, message: self.onMessage(
                                                        message),
                                                    on_error=lambda ws, err: self.onError(
                                                        err),
                                                    on_close=lambda ws: self.onClose())
            self.socketThread = Thread(target=self.run_socket)
            self.socketThread.setDaemon(True)
            self.socketThread.start()

        def run_socket(self):
            self.webSocket.run_forever()
            pass

        def getTrainingSubscription(self):
            return json.dumps({
                'query': "subscription { onUpdateProject { isTraining id } }",
                'variables': {}
            })

        def getHeaderTime(self):
            return datetime.utcnow().isoformat(sep='T', timespec='seconds') + 'Z'

        def encodeHeader(self, header):
            return b64encode(json.dumps(header).encode('utf-8')).decode('utf-8')

        def resetTimer(self):
            if self.timeoutTimer:
                self.timeoutTimer.cancel()
            self.timeoutTimer = threading.Timer(
                self.timeoutInterval, lambda: self.webSocket.close())
            self.timeoutTimer.setDaemon(True)
            self.timeoutTimer.start()

        def onMessage(self, message):
            message = json.loads(message)
            messageType = message.get('type')
            if(messageType == 'ka'):
                self.resetTimer()
            elif(messageType == 'connection_ack'):
                self.timeoutInterval = int(json.dumps(
                    message.get('payload').get('connectionTimeoutMs')))
                register = {
                    'id': self.subscriptionID,
                    'payload': {
                        'data': self.getTrainingSubscription(),
                        'extensions': {
                            'authorization': {
                                'host': self.host,
                                'x-api-key': self.communicator.apiKey
                            }
                        }
                    },
                    'type': 'start'
                }
                startSub = json.dumps(register)
                self.webSocket.send(startSub)
            elif(messageType == 'data'):
                projectUpdate = message.get('payload').get(
                    'data').get('onUpdateProject')
                projectID = projectUpdate.get('id')
                isTraining = projectUpdate.get('isTraining')
                if projectID == self.communicator.projectID and isTraining != None:
                    self.communicator.setProjectMode(isTraining)
            elif(messageType == 'error'):
                print('Error from AppSync: ' + message.get('payload'))

        def onError(self, error):
            print(error)

        def onClose(self):
            print(f"Project Listener {self.projectID} closed.")

        def onOpen(self):
            init = {
                'type': 'connection_init'
            }
            initConn = json.dumps(init)
            self.webSocket.send(initConn)

        def closeListener(self):
            deregister = {
                'type': 'stop',
                'id': self.subscriptionID
            }
            endSub = json.dumps(deregister)
            self.webSocket.send(endSub)
            self.webSocket.close()
            self.socketThread.join()
            if self.timeoutTimer:
                self.timeoutTimer.cancel()


if __name__ == "__main__":
    print("Communicator Test")
    communicator = Communicator()
    communicator.setCurrentProjectByName("purtilo-cdr")
    communicator.updateProjectMode(isTraining=False)
    # communicator.destroy()
