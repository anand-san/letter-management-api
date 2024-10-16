# Paiperless API

This is a production-level Deno-based API server using Hono and Firebase Admin.

## Prerequisites

- [Deno](https://deno.land/#installation) installed on your machine
- Firebase project set up with service account credentials

## Setup

1. Clone this repository:

   ```
   git clone https://github.com/your-username/paiperless-api.git
   cd paiperless-api
   ```

2. Set up your Firebase service account:
   - Go to your Firebase Console
   - Navigate to Project settings > Service Accounts
   - Generate a new private key and download the JSON file
   - Set the contents of this JSON file as an environment variable:
     ```
     export FIREBASE_SERVICE_ACCOUNT='{"type": "service_account", ...}'
     ```

## Running the server

To start the server, run:

```
deno task start
```

The server will start on `http://localhost:8000`.

## API Endpoints

- `GET /`: Returns a "Hello Hono!" message
- `GET /api/data`: Returns a placeholder message (to be replaced with actual Firebase data)

## Development

This project uses Deno for runtime and package management. The main application file is `src/main.ts`.

To add new routes or functionality, modify the `src/main.ts` file.

## Production Deployment

For production deployment, consider the following:

1. Set up proper environment variable management for your production environment.
2. Use a process manager like PM2 to keep your application running.
3. Set up a reverse proxy (like Nginx) to handle SSL termination and load balancing.
4. Implement proper logging and monitoring solutions.

## License

[MIT License](LICENSE)
