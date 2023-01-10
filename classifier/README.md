# Classifier

This is the front-end monitoring and configuration application for interfacing with AWS services in order to run text-detection and classification on images consumed from a Raspberry PI in realtime.

## Dev Setup

Follow the steps below to get started.
1. Make sure you have access to the project's AWS account and appropriate IAM credentials.
1. (Not required) Install the AWS CLI 
1. Make sure you have the AWS Amplify CLI installed on your local device. (https://docs.amplify.aws/cli/start/install/)
1. Install Node on your local development machine.
1. Run `npm install` to install all the necessary Javascript libraries and packages.
1. Run `amplify pull --appId d7akvp4cm6n2i --envName staging`
1. This should open your browser to verify your auth credentials.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
