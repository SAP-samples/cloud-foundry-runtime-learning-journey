# Getting Started
[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/cloud-foundry-runtime-learning-journey)](https://api.reuse.software/info/github.com/SAP-samples/cloud-foundry-runtime-learning-journey)

## How to install

This section explains how to deploy the application to your SAP BTP subaccount.
First, the Cloud-Foundry-native deployment using `cf-push` is shown. Then the MTA-based deployment is explained. Please ensure to log on to the Cloud Foundry environment using the Cloud Foundry CLI using [this guide](https://help.sap.com/docs/btp/sap-business-technology-platform/log-on-to-cloud-foundry-environment-using-cloud-foundry-command-line-interface).

#### Prerequisites

- You have access to an SAP BTP, Cloud Foundry environment and have the necessary permissions to deploy applications into a Cloud Foundry space.
- You have installed the following tools:
  -  [git CLI](https://git-scm.com/downloads)
  -  [cds CLI](https://cap.cloud.sap/docs/tools/cds-cli)
  -  [Cloud Foundry CLI](https://docs.cloudfoundry.org/cf-cli/)
  -  [Cloud MTA Build Tool (MBT)](https://sap.github.io/cloud-mta-build-tool/)


### Task 1: Clone the sample application

1. Clone the sample application from the GitHub repository.

Clone the sample application from the GitHub repository using the following command:

```bash
git clone https://github.com/SAP-samples/cloud-foundry-runtime-learning-journey
```

2. Open the cloned project in your preferred IDE.

### Task 2: Deploy the application using native Cloud Foundry deployment

1. Build the project

This reference applications already comes with all neccessary files for the deployment. However, you have to build the application for production first:

```bash
cds build --production
```

The `--production` parameter ensures that the cloud deployment-related artifacts are created by cds build.

2. Login to your Cloud Foundry instance and target an organization and space

Use the following command to login to your Cloud Foundry instance:

```bash
cf login
```

Provide the API endpoint, which you can find in the SAP BTP cockpit, and your credentials. Once authenticated, target an organization and space by choosing the respective values from the list. 

Alternatively, you can also use the following command to target an organization and space:

```bash
cf target -o <organization> -s <space>
```

4. Push the application to Cloud Foundry

Use the following command to deploy the application to Cloud Foundry:

```bash
cf push
```

Read more about the deployment via cf-push in the official [[CAP documentation](https://cap.cloud.sap/docs/guides/deployment/to-cf#deploy-using-cf-push)].

4. Access the application

In your Terminal, you will see the URL of the deployed application. Open the URL in your browser to access the application.
Alternatively, you can also navigate into your application that is now deployed inside your Cloud Foundry space on the SAP BTP cockpit and access the application from there.

### Task 2: Deploy the application using Multi-Target Application (MTA) deployment

1. Build the project
This reference applications already comes with all neccessary files for the deployment. However, you have to build the application for production first:

```bash
mbt build -t gen --mtar mta.tar
```

This will create a `mta.tar` file in the `gen` folder. This file contains the deployment artifacts for the MTA deployment.

2. Deploy the application

Use the following command to deploy the application to Cloud Foundry:

```bash
cf deploy gen/mta.tar
```

Wait until the process is finished. You can check the status of the deployment in the terminal. Once the deployment is finished, you should see something like this:

```bash
[…] Application "hello-cloud-foundry-srv" started and available at "[org]-[space]-hello-cloud-foundry-srv.landscape-domain.com" […]
```

## Learn More

- [Getting Started with CAP](https://cap.cloud.sap/docs/get-started/)
- [Deploy to Cloud Foundry Guide](https://cap.cloud.sap/docs/guides/deployment/to-cf)
- https://developers.sap.com/tutorials/deploy-to-cf.html

## Contributing

If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License

Copyright (c) 2024 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
