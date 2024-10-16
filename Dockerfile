FROM denoland/deno:latest

WORKDIR /app

COPY . .

RUN deno cache main.ts

CMD ["deno", "run", "--allow-net", "--allow-env", "--allow-read", "--allow-run", "main.ts"]
