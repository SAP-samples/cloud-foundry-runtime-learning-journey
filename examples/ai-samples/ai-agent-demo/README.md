# AI Agent - SAP AI Core Orchestration Service with Tool Calling

A web-based chat interface with AI tool calling capabilities for SAP AI Core's Orchestration Service, built with [Mesop CLI](https://mesop-dev.github.io/mesop/).

> **⚠️ DISCLAIMER**
>
> This application is a **reference application** for learning and demonstration purposes only. It showcases the integration of SAP Business Technology Platform (BTP) services including SAP AI Core, XSUAA authentication, and App Router.

>This is **not a production-ready application** and can be used as a starting point for understanding BTP service capabilities and deployment patterns.

## Available Tools

The AI assistant has access to 4 tools:

1. **Web Search** - Live web search using DuckDuckGo (no API key needed)
2. **Wikipedia Search** - Retrieve Wikipedia article summaries
3. **Dictionary** - Get word definitions, pronunciations, and examples
4. **Weather** - Get real-time weather using Open-Meteo API (no API key needed)

## Features

- AI assistant with tool calling capabilities
- Automatic tool execution and result formatting
- Easy deployment to Cloud Foundry
- Secure credential management
- Clean, modern chat interface

## Authentication Architecture

When deployed to Cloud Foundry, the application uses SAP's enterprise authentication:

```text
┌──────┐         ┌───────────────┐         ┌──────────────┐         ┌─────────┐
│ User │────────▶│ App Router    │────────▶│ Tools Chat   │────────▶│ AI Core │
│      │  HTTPS  │ + XSUAA       │  AuthN  │ UI Backend   │   API   │ Service │
└──────┘         └───────────────┘         └──────────────┘         └─────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ XSUAA       │
                  │ Service     │
                  └─────────────┘
```


**How it works:**

1. User accesses URL → Redirected to SAP BTP login
2. User logs in → XSUAA validates credentials
3. XSUAA issues token → App Router receives OAuth2 token
4. App Router forwards request → Backend processes with authentication

## Quick Start (Local Development)

> **📍 Working Directory**: All commands below should be run from `examples/ai-samples/ai-agent-demo/`

### 1. Install Dependencies

#### Using uv (Recommended - Fast)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

#### Using pip (Traditional)

```bash

cd examples/ai-samples/ai-agent-demo

pip install -r requirements.txt
```

**Note:** Both `pyproject.toml` (for uv) and `requirements.txt` (for Cloud Foundry) are maintained.

To sync requirements.txt after updating dependencies in pyproject.toml:

```bash
make sync-requirements
```

Or manually:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

### 2. Configurations

#### 1. Update OAuth Redirect URI (REQUIRED for Security)

⚠️ **IMPORTANT SECURITY STEP**: The default `xs-security.json` contains a placeholder redirect URI that must be updated before deployment.

**Steps to configure**

1. **Determine your region and route**
   ```bash
   # Check your CF API endpoint to identify your region
   cf api
   # Example outputs:
   # https://api.cf.eu12.hana.ondemand.com (EU - Frankfurt)
   # https://api.cf.us10.hana.ondemand.com (US - East)
   ```

2. **Update `xs-security.json`** with your specific route

   Edit `deploy/xs-security.json`:

   ```json
   "redirect-uris": [
     "https://ai-agent-demo.cfapps.<YOUR-REGION>.hana.ondemand.com/**"
   ]
   ```

   **Region examples**
   - EU (Frankfurt): `eu12`
   - US (East): `us10`
   - Asia Pacific (Singapore): `ap21`
   - See full list: https://help.sap.com/docs/btp/sap-business-technology-platform/regions

3. **Update approuter actual route in `deploy/mta.yaml`**:

   Edit `mta.yaml` to change the application URL:

   ```yaml
   routes:
      - route: ai-agent-demo.cfapps.eu12.hana.ondemand.com  # Update route https://ai-agent-demo.cfapps.<YOUR-REGION>.hana.ondemand.com
   ```


#### 2. Update AI Core Service configuration


- Copy the example environment file and add your SAP AI Core credentials:

    ```bash
       cp .env.example .env
       # Edit .env with your credentials
    ```
- Edit `mta.yaml` to match your AI Core service instance name:

    ```yaml
       resources:
       - name: aicore
       type: org.cloudfoundry.existing-service
       parameters:
       service-name: default_aicore  # Change this to YOUR SAP AI CORE service instance name
    ```


### 3. Run Locally

```bash
cd examples/ai-samples/ai-agent-demo
mesop app.py
```

The application will open in your browser at **http://localhost:32123**

## Example Queries

Try these queries to see the tools in action:

- "What's the weather in Tokyo?"
- "Search the web for latest SAP AI news"
- "Tell me about machine learning from Wikipedia"
- "What does serendipity mean?"
- "Search for Python programming tutorials"

## Deploy to Cloud Foundry

⚠️ **REQUIRED CONFIGURATION**: Before deployment, you must update the OAuth redirect URI in `deploy/xs-security.json` to match your specific region and route. See [`deploy/README.md`](deploy/README.md#1-update-oauth-redirect-uri-required-for-security) for detailed instructions.

**For detailed deployment instructions, see [`deploy/README.md`](deploy/README.md)**

### Quick Deploy

Using Make (Recommended):

```bash
cd examples/ai-samples/ai-agent-demo
make deploy

# Or step by step:
make build    # Sync requirements + build MTA archive
cd deploy && cf deploy mta_archives/ai-agent-demo_1.0.0.mtar
```

Manual method:

```bash
cd examples/ai-samples/ai-agent-demo/deploy

# Build MTA archive
mbt build

# Deploy to Cloud Foundry
cf deploy mta_archives/ai-agent-demo_1.0.0.mtar
```

### What Gets Deployed

1. **App Router** (with XSUAA authentication)
2. **Python Backend** (Mesop chat UI with Gunicorn + WSGI)
3. **Service Bindings** (AI Core + XSUAA)

## Troubleshooting

### No credentials found

Ensure `.env` file exists with valid credentials for local development, or verify AI Core service is bound in Cloud Foundry.

### Authentication Error: "BTP shadow user not found"

**Error Message:**
```
There was an error when authenticating against the external identity provider:
User couldn't authenticate against external identity provider.
BTP shadow user not found for user provided by external identity provider.
Pre-create the user or enable shadow user creation in your BTP subaccount.
```

**Root Cause:** When users authenticate via an external identity provider (e.g., SAP corporate IDP), XSUAA requires a "shadow user" to be created in the BTP subaccount. By default, shadow user creation is disabled.

**Solution:**

1. Navigate to **BTP Cockpit** → Your Subaccount
2. Go to **Security** → **Trust Configuration**
3. Select your Identity Provider (e.g., `sap.default` or your custom IDP)
4. Enable **"Create Shadow Users on First Logon"**
5. Save the configuration
6. Try accessing the application URL again

**Reference:** [SAP Help - Authentication Error with External Identity Provider](https://help.sap.com/docs/btp/sap-business-technology-platform/there-was-error-when-authenticating-against-external-identity-provider?locale=en-US)

**Note:** This is a **subaccount-level configuration**, not an application-level setting.

### Deployment issues

For Cloud Foundry deployment problems, see detailed troubleshooting in [`deploy/README.md`](deploy/README.md).


For deployment details, see [`deploy/README.md`](deploy/README.md)

## Learn More

- [SAP AI Core Documentation](https://help.sap.com/docs/sap-ai-core)
- [Orchestration Service Reference](https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/_reference/orchestration-service2.html)