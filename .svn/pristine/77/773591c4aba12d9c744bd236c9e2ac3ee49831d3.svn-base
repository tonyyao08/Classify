[Overview](README.md) > AWS

# Amazon Web Services Configuration

Our project uses AWS as cloud provider. AWS provides us with various ML and realtime system services.

## AWS Services Used
- **AWS Rekognition** [AWS Rekognition Developer Guide](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html)
    - We used AWS Rekognition to perform text recognition on our captured images in order to perform text matching in order to match user entered labels/ meta information to the retrieved text from the AWS ML model. We chose Rekognition after playing around with various other libraries and services. We found that Amazon's pre-trained text recongition service returned the highest accuracy text detection out of all of libraries we tried.
- **AWS Amplify** [AWS Amplify Developer Guide for Angular Projects](https://docs.amplify.aws/start/q/integration/angular/)
    - AWS Amplify is an all-in-one full-stack app development provider which provides layered abstractions for interfacing with various other AWS services to provide a large subset of functionality commonly used by web applications. We used AWS Amplify for our database, api, and authentication.
        - **Datastore**
            - We used the Amplify Datastore to host all of the data pertaining to our projects and their corresponding images. The Amplify Datastore service is great because it provided us with out-of-the-box serverless functionality which got rid of the need for us to write our own backend and manage its runtime as well as the ability to subscribe and listen to changes in our data in realtime.
            - Datastore is an abstraction that works with the AWS DynamoDB database. This is a serverless document-based database hosted by AWS. DynamoDB is widely used in industry and is one of the leading document based database options available today.
        - **Authentication**
            - We used Amplify's authentication service to allow user to authenticate with our web app. It was necessary for our users to authenticate in order to ensure traceability as they interacted with other paid AWS services (mainly S3). Once a user authenticated with our app we were able to attach a policy to their account which gave them full read/write access to our S3 buckets.
            - The Authentication service makes use of AWS Cognito which interfaces nicely with AWS IAM to allow you to setup authentication pools and federated identities and attach various IAM roles and policies to users. In our case, Amplify automatically created an AWS Cognito Authentication pool for all newly created user accounts to which we were able to attach an all access policy to make requests to our AWS services. This way, users can make these requests using their own credentials. This makes it easy to restrict access to specific users at any time as well as trace back the requests each user is making since all of their requests are tied to their specific Cognito credentials.
        - **API**
            - AWS Amplify automatically creates a GraphQL endpoint so that you can easily perform CRUD operations on your database documents. This allowed our Raspberry PI application to interface with our database without the need for us to manage our own API/ server and implement various CRUD operation endpoints.
            - The AWS Amplify API service uses AWS AppSync behind the scenes to setup a serverless API and makes use of auto-generated AWS Lambda functions to implement the GraphQL api.
            - Our GraphQL endpoint uses API key authentication which allows us to distribute a single API key to any Raspberry PI device that wants to interface with our system.
- **AWS Simple Storage Service (S3)**
    - AWS S3 is a data storage service that handles storage for a large variety of different file formats. We specifically use S3 to manage the upload and storage of various images captured by the Raspberry Pi so that they can be consumed by the monitoring web application.

## Configuration and Installation


### Creating your AWS Amplify App

1. Start by creating an AWS developer account at [https://aws.amazon.com/](https://aws.amazon.com/).
1. Once you have created an AWS account, sign-in to the console and search for AWS Amplify.
1. Inside the AWS Amplify console click on the hamburger menu and click on "All apps"
1. Click on "New app" > "Build an app"
1. Give your app a name. In our case we used "classify" but you can use any name.
![create new amplify app](images/new-app-name.png)
1. Click "Confirm Deployment"
    - This may take a few moments while AWS provisions the various aforementioned AWS underlying services.
1. Once the app is done being created, click "Launch Studio"
1. In the Amplify Studio dashboard we will need to setup the Data schema as well as the app authentication.
![blank data model page](images/data-model.png)
    1. We need to add two models to our Amplify app. Click on "Add model"
    1. Create a Project and Image model with the following fields:
![project model fields](images/project-model.png)
![image model fields](images/image-model.png)
**Note:** It is very important that you enter the field information exactly as shown. The front end code is expecting these specific fields to be established.
    1. After you have entered in the field information click "Save and Deploy"
1. Next, we will setup the Amplify Authentication service.
    1. To setup our Authentication click on the "Authentication" tab on the left side menu.
    1. Choose the "Start from scratch" option
    1. For our login mechanism we will stick with Email login. However, Amplify provides interfaces for various popular social logins that may be added in the future if desired.
    1. In the "Configure sign up" card add the name as an attribute we will require from users upon sign up.
    1. Click "Deploy" at the bottom of the page.
1. After both the Data and Authentication modules have been deployed you are ready to import those changes into your front-end code using the Amplify CLI.
1. Inside the `classifier` directory enter in the following commmands:
Install the Amplify CLI on your local machine:
```
curl -sL https://aws-amplify.github.io/amplify-cli/install | bash && $SHELL
```
Pull your Amplify project:
```
amplify pull --appId APP_ID --envName staging
```
Add the GraphQL app:
```
amplify add api
```
This last command will present you with various options. When it asks you if you plan to make changes to your backend say No.


### AWS Rekognition Setup

The AWS Text Rekognition service uses a pre-trained text detection model that takes no configuration parameters. As such, this AWS service does not require any configuration and is ready to accept requests at any time.


### AWS S3 Setup

1. In the AWS developer console search for S3.
1. Once you land on the S3 console click on "Buckets" in the left-hand sidebar.
1. Click "Create bucket"
1. Give your bucket a name and assign it a region near your physical device.
1. For all of the rest of the settings leave them as their default.
1. Click "Create bucket"
1. Once your bucket has been created click on it to view its settings.
1. Under the "Permissions" tab scroll down to the Cross-origin resource sharing (CORS) settings and copy-paste the following CORS policy.
```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "HEAD",
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```
This enables our browser to request data from the S3 bucket. By default, AWS implements a strict no cross-origin sharing policy. This CORS policy changes that default.


### AWS IAM/ Cognito Setup

After Amplify has created a new Cognito authentication pool you are ready to assign a policy to allow authenticated web app users to read from your AWS S3 buckets.
1. Search for "IAM" in the developer console.
1. Click on "Policies" in the left-hand navigation menu.
1. Click on "Create Policy"
1. For "Service" choose "S3"
1. For "Actions" choose "Read"
1. For "Resources" choose your newly created S3 bucket or click "All resources" to allow generic read access to all S3 buckets in your AWS account.
1. Leave both options under "Request Conditions" unchecked.
1. Click "Next: Tags"
1. Click "Next: Review"
1. Give your policy a name and click "Create Policy"
1. Go to "Roles" and find the role that related to authenticated Amplify users. It should be something similar to "amplify-{{AMPLIFY_PROJ_NAME}}-authRole"
1. Under the Permissions policies add the newly created policy.

Next, we need to attach our newly created IAM policy to all authenticated Amplify users.
1. Search for "Cognito" in the developer console.
1. Find the user pool relating to your Amplify app. It should be named the same as your Amplify project.
1. Click on "Groups"
1. Click "Create Group"
1. Enter in "s3access" as the group name.
1. For the IAM role select "Cognito_WebAppAuth_Role"

As a last step for our AWS Setup, you need to create an IAM user for the Raspberry PI to use to interface with your AWS services.

1. Search for "IAM" in the developer console.
1. Click on "Users"
1. Click "Add users"
1. Give your user a name (e.g. "raspberry-pi")
1. Choose "Access key" for the AWS access type
1. For Permissions, assign your user to the "Administrators" group. This is the most straightforward way of configuring your IAM user. However, be aware that anyone who obtains the resulting Access Key will have full access to your AWS account.
1. Click "Next: Tags"
1. Click "Next: Review"
1. Click "Create user"
1. Copy down the Raspberry PI Access Key ID and Secret access key for future use.

### AWS GraphQL API Access Key

1. The Raspberry PI will need an API access key. Search for "App Sync" in the developer console.
1. Click on the app relating to your Amplify project.
1. Click on setup and copy down the `API_URL`
1. Under the "Default authorization mode" settings choose "API Key"
1. Create a new key
1. Copy down the newly created key. Take note of the expiration date.
1. You will want to set your Expiration date to a date sufficiently far in the future. After this date, the Raspberry PI will lose connection to the GraphQL endpoint in AWS.

### Next Steps

Congratulations! If you are reading this you have configured your AWS account and environment and are now ready to setup/ build the web app and raspberry pi environment.
