# docker/javascript/Dockerfile
FROM node:18-slim

WORKDIR /app

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create function directory
RUN mkdir -p /app/function

ENTRYPOINT ["/entrypoint.sh"]
