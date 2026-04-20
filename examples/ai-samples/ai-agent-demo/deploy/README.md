# SAP BTP Cloud Foundry Deployment Guide

This directory contains all Cloud Foundry deployment configuration for the AI Agent Chat UI application.

## Quick Start

### Prerequisites

1. **Cloud Foundry CLI**: `cf --version`
2. **MTA Plugin**: `cf install-plugin multiapps`
3. **MTA Build Tool**: `npm install -g mbt`
4. **Login to CF**: `cf login`
5. **Setup SAP AI Core**: [Step-by-step guide](https://developers.sap.com/tutorials/ai-core-genaihub-provisioning.html)

### Deploy

```bash
# From the deploy/ directory
cd examples/ai-samples/ai-agent-demo/deploy

# Build MTAR archive
mbt build

# Deploy to Cloud Foundry
cf deploy mta_archives/ai-agent-demo_1.0.0.mtar
```

### Access Application

After deployment, get the App Router URL:

```bash
cf app approuter
```

Access the URL in your browser - you'll be prompted to log in with SAP BTP credentials.

## Architecture

```text
┌──────────┐         ┌──────────────┐         ┌──────────────┐         ┌──────────┐
│ Internet │────────▶│ App Router   │────────▶│ Python       │────────▶│ AI Core  │
│          │  HTTPS  │ + XSUAA      │  AuthN  │ Backend      │   API   │ Service  │
└──────────┘         │ (Node.js)    │         │ (Mesop)      │         └──────────┘
                     └──────────────┘         └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ XSUAA        │
                     │ Service      │
                     └──────────────┘
```

### Deployed Components

1. **App Router** (`approuter`)
   - Handles XSUAA OAuth2 authentication
   - Reverse proxy to backend
   - Public route: `https://ai-agent-demo.cfapps.*.hana.ondemand.com`

2. **Python Backend** (`ai-agent-demo`)
   - Mesop chat UI
   - Gunicorn WSGI server
   - Custom middleware for CSRF handling
   - Internal route (not directly accessible)

3. **Services**
   - **ai-agent-demo-xsuaa**: XSUAA service for authentication
   - **aicore**: SAP AI Core service (existing)

## Troubleshooting

### View Logs

```bash
# App Router logs
cf logs approuter --recent

# Backend logs
cf logs ai-agent-demo --recent

# Tail logs in real-time
cf logs approuter
```

### Check Status

```bash
# View all applications
cf apps

# Check service bindings
cf services

# View environment variables
cf env approuter
cf env ai-agent-demo
```

### App Router Configuration (approuter/xs-app.json)

- Authentication: XSUAA
- CSRF Protection: Disabled (handled by backend middleware)
- Routes all requests to backend with authentication

## Security Notes

- **Authentication**: Required for all requests via XSUAA
- **CSRF Protection**: Handled by custom middleware in backend
- **Credentials**: Never commit `.env` files or credentials
- **Access**: Only App Router is publicly accessible, backend is internal

## Learn More

- [SAP BTP Cloud Foundry](https://help.sap.com/docs/btp/sap-business-technology-platform/cloud-foundry-environment)
- [SAP App Router](https://help.sap.com/docs/btp/sap-business-technology-platform/application-router)
- [XSUAA Service](https://help.sap.com/docs/btp/sap-business-technology-platform/authorization-and-trust-management-service)
- [MTA Development](https://help.sap.com/docs/BTP/65de2977205c403bbc107264b8eccf4b/d04fc0e2ad894545aebfd7126384307c.html)
- [SAP AI Core](https://help.sap.com/docs/sap-ai-core)
