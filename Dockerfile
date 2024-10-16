FROM denoland/deno:2.0.0

WORKDIR /app

# Copy only necessary files
COPY deno.json .
COPY deno.lock .
COPY deps.json .
COPY main.ts .
COPY env.ts .

COPY src src
COPY templates templates

# Cache dependencies
RUN deno cache deps.json

RUN deno cache main.ts

CMD ["deno", "run", "--allow-net", "--allow-env", "--allow-read", "--allow-run", "--env", "main.ts"]
