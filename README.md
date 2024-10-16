# Paiperless API

This is the API server for paperless using Hono and Firebase.

## Prerequisites

- [Node.js](https://nodejs.org/) (version 20 or later) installed on your machine
- Firebase project set up with service account credentials
- Google Cloud account - For documennt ocr

## Setup

1. Clone this repository:

```
git clone https://github.com/anand-san/paiperless-api.git

cd paiperless-api
```

2. Install dependencies:

```
npm install
```

3. Set up your Firebase service account:

- Go to your Firebase Console
- Navigate to Project settings > Service Accounts
- Generate a new private key and download the JSON file
- Create a `.env` file in the project root and add the following:
  ```
  FIREBASE_SERVICE_ACCOUNT='{"type": "service_account", ...}'
  ```

## Running the server locally

To start the server in development mode, run:

npm run dev

For production, build and start:

npm run build npm start

The server will start on `http://localhost:port`
