[Overview](README.md) > Web App

# Monitoring Web Application

The monitoring web application module is the main user-facing interface for managing various projects, entering model training information, and controlling/ monitoring the state of the classifications made by the Raspberry PI system.

## Codebase Location

The code for the monitoring web application resides in the [classifier](../classifier/) directory.

### Tech Stack Overview

- **Front-end Framework**: Angular [https://angular.io/](https://angular.io/)
    - We used Angular as our front-end Javascript framework. Angular is an easy-to-use opinionated framework that allows you get a jumpstart on any front-end project with its built features such as routing, state management, robust CLI, and many more. A large motivation for choosing Angular was for prior team experience with the framework.
- **UI Library**: Angular Material [https://material.angular.io/](https://material.angular.io/)
    - In order to accelerate the UI development process, we used the Angular Material library which was specifically designed for use with Angular components and comes pre-packaged with opinionated style choices based on UX research performed by the Google Material Design team which allowed us to focus on the front-end logic rather than styling and design.
- **Language**: Typescript [https://www.typescriptlang.org/](https://www.typescriptlang.org/) 
    - Our front-end web application code is majorly implemented using Typescript aside from various boilerplate configuration files. Typescript builds on Javascript as a strongly typed programming language which gives us better tooling such as code completiona and development time type-checking.

## Codebase Organization

The main front-end app code resides in the [`src/app`](../classifier/src/app/)

The state of the app is managed by various services implemented in the [`core`](../classifier/src/app/core) directory.

- **Database Service**: The database service interfaces with our AWS managed database (AWS Amplify Datastore). This service provides end-points for front-end components to query projects and various images relating to projects in real-time. This service provides implementation for CRUD actions for projects.
- **Storage Service**: The storage service interfaces with AWS S3 which is our main storage repository for all project assets. While image locations are stored inside the database we specifically need to make calls to AWS S3 to retrieve the image base-64 encoded bytes to display to the user.
- **Safe Resource Pipe**: The safe resource pipe provides implementation to bypass built-in Angular script injection prevention. In our case we make use of this pipe in the training and monitoring front-end components to mark the base 64 encoding as safe once it is returned from AWS S3.

The rest of the directories in the [`src/app`](../classifier/src/app/) directory relate to specific front-end components. All of our routing and app bootstrapping occurs in [app-routing.module.ts](../classifier/src/app/app-routing.module.ts) and [app.module.ts](../classifier/src/app/app.module.ts) respectively.

- **Create Project Dialog** `src/app/create-project-dialog`
    - The Create Project Dialog component provides a pop-up dialog component for the user to enter in a project name.
- **Delete Project Dialog** `src/app/create-project-dialog`
    - The Create Project Dialog component provides a pop-up dialog component for the user to confirm the deletion of a project.
- **Dashboard** `src/app/dashboard`
    - The Dashboard component provides is the entry-point for all **authenticated** users. It provides the application toolbar and menus as well as manages which routed component is being shown.
- **app.component.ts** `src/app/app.component.ts`
    - The App component is the main component and entry-point for all users of the app. This component conditionally displays the user with an authenticator component provides by the AWS Amplify UI library for Angular. The authenticator component provides a standard UI that allows users to create accounts and login.
- **Project** `src/app/project`
    - The Project directory contains all the UI components relating to a singular project.
        - **Overview** `src/app/project/overview`
            - The Overview component is the main entry point for the single project view route and contains a tab list that houses the rest of the components that allow the user to view the status of their project (Monitoring) and add training data (Training).
        - **Training** `src/app/project/training`
            - The Training component provides the user with the latest consumed training image and allows them to enter in label/ meta information to be used later during the classification step.
        - **Monitoring** `src/app/project/monitoring`
            - The monitoring component provides the user with the latest consumed monitoring image and it's corresponding classification as determined by our text recognition and corresponding matching algorithms performed on the Raspberry PI.
- **Project List** `src/app/project-list`
    - The project list component displays all the current projects created and provides links to each of their overview pages.

## AWS Amplify Integration

The AWS Amplify CLI takes care of most the integrating boilerplate code. Once you have setup your Amplify project following the steps outlined in the [AWS Installation](AWS.md) procedure you can run the following commands in the `classifier` directory.

```
amplify pull --appId APP_ID --envName staging
```
Note: Replace `APP_ID` with your actual AWS Amplify app id you obtained while setting up your Amplify project.

Running this command will ask you to authenticate to your AWS account using your browser and may ask you various questions about your environment. If you have any trouble getting this setup a good starting point is looking at the AWS Amplify documentation for web apps using Angular: [https://docs.amplify.aws/start/q/integration/angular/](https://docs.amplify.aws/start/q/integration/angular/).

## Configuration and Installation

System Requirements:
- Node.js (Angular requires an active LTS or maintenance LTS version of Node.js)
- npm [Node Package Manager] (Angular depends on npm packages for many features and functions)

Node.js and npm can be installed using the latest installation instructions available on [https://nodejs.org/en/](https://nodejs.org/en/).

As a first step you will want to install the Angular CLI. This will allow you to build, serve, and test your front-end application.

1. Install the Angular CLI. Inside the `classifier` directory run `npm install -g @angular/cli`
    - Note: for some machines using the -g flag which installs the Angular CLI globally requires a sudo prefix.
1. Configure the web app environment variables

### S3 Buckets
Currently, this program stores every users' images in one S3 bucket named 'mycoins'. Because of this, this program makes calls to AWS using the string literal, 'mycoins', to retrieve and edit the contents that are within this bucket. If a user would like to use an S3 bucket of their own, they'd have to head to these files and change each 'mycoins' string to instead read their own buckets name:\
>[/src/app/core/database.service.ts](../classifier/src/app/core/database.service.ts)\
>[src/app/core/storage.service.ts](../classifier/src/app/core/storage.service.ts)\
>[src/app/project/monitoring/monitoring.component.ts](../classifier/src/app/project/monitoring/monitoring.component.ts)\
>[src/aws.js](../classifier/src/aws.js)

### Launching the Site

Run the `ng serve` command to serve your static site with hot reload or the `ng build` command to compile your typescript assets, styles, html into the `dist/classifier` directory ready for production.

