# Getting Started

Welcome to your new project.

It contains these folders and files, following our recommended project layout:

| File or Folder | Purpose                              |
| -------------- | ------------------------------------ |
| `app/`         | content for UI frontends goes here   |
| `db/`          | your domain models and data go here  |
| `srv/`         | your service models and code go here |
| `package.json` | project metadata and configuration   |
| `readme.md`    | this getting started guide           |

## Next Steps

- Open a new terminal and run `cds watch`
- (in VS Code simply choose _**Terminal** > Run Task > cds watch_)
- Start adding content, for example, a [db/schema.cds](db/schema.cds).

## Deployment

This section explains how to deploy the application to your SAP BTP subaccount.
First, the Cloud-Foundry-native deployment using `cf-push` is shown. Then the MTA-based deployment is explained. Please ensure to log on to the Cloud Foundry environment using the Cloud Foundry CLI using [this guide](https://help.sap.com/docs/btp/sap-business-technology-platform/log-on-to-cloud-foundry-environment-using-cloud-foundry-command-line-interface).

### CF-native deployment

#### Prerequisites

Install the Create-Service-Push plugin:

```sh
cf install-plugin Create-Service-Push
```

#### Build the project

This reference applications already comes with all neccessary files for the deployment. However, you have to build the application for production first:

```sh
cds build --production
```

The `--production` parameter ensures that the cloud deployment-related artifacts are created by `cds build`.

#### Push the application

Then push the application to the SAP BTP. This will also ensure to bind the services to the application with a single call:

```sh
cf create-service-push
```

Read more about the deployment via `cf-push` in the official [CAP documentation](https://cap.cloud.sap/docs/guides/deployment/to-cf#deploy-using-cf-push).

### MTA-based deployment

#### Build the project

This reference applications already comes with all neccessary files for the deployment. However, you have to build the application for production first:

```sh
mbt build -t gen --mtar mta.tar
```

#### Deploy the application

```sh
cf deploy gen/mta.tar
```

This process can take some minutes and finally creates a log output like this:

[…]
Application "bookshop" started and available at
"[org]-[space]-bookshop.landscape-domain.com"
[…]

## Learn More

- [Getting Started with CAP](https://cap.cloud.sap/docs/get-started/)
- [Deploy to Cloud Foundry Guide](https://cap.cloud.sap/docs/guides/deployment/to-cf)
- https://developers.sap.com/tutorials/deploy-to-cf.html

## Contributing

If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License

Copyright (c) 2024 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
