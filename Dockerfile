FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY src ./src
COPY templates ./templates
COPY tsconfig.json ./tsconfig.json

RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/node_modules ./node_modules

# Run the application
CMD ["node", "dist/main.js"]