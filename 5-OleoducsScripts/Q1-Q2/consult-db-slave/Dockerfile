# Stage 1: Build the TypeScript application
FROM node:24 AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Create a lean production image
FROM node:24-slim

# Install redis
RUN apt-get update && apt-get install -y redis-server redis-tools

# Configure Redis to start in the background
RUN sed -i 's/^daemonize no/daemonize yes/' /etc/redis/redis.conf

# Configure Redis to run on 0.0.0.0
RUN sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf

# Remove protected-mode
RUN sed -i 's/^protected-mode yes/protected-mode no/' /etc/redis/redis.conf

WORKDIR /app

# Copy compiled JavaScript from the builder stage
EXPOSE 3000
COPY --from=builder /app/dist ./dist
COPY package.json package-lock.json my-deployment-configs.json ./
RUN npm install --production

## HINT: you need /dist/index.js...

# TODO STUDENT: Start the apps
#ENTRYPOINT [ "echo", "hello from my app" ]
CMD ["node", "./dist/index.js"]
