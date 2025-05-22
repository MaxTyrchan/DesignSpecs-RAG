# Use the latest version of langflow
FROM langflowai/langflow:latest

# Create accessible folders and set the working directory in the container
RUN mkdir /app/flows
RUN mkdir /app/langflow-config-dir
WORKDIR /app

# Copy the flows, optional components, and langflow-config-dir folders to the container
COPY flows /src/flows
COPY components /src/components
COPY langflow-config-dir /src/langflow-config-dir

# copy docker.env file
COPY .env /app/.env

# Set environment variables
ENV PYTHONPATH=/app
ENV LANGFLOW_LOAD_FLOWS_PATH=/app/flows
ENV LANGFLOW_CONFIG_DIR=/app/langflow-config-dir
ENV LANGFLOW_COMPONENTS_PATH=/app/components
ENV LANGFLOW_LOG_ENV=container

# Command to run the server
EXPOSE 7860
CMD ["langflow", "run", "--backend-only", "--env-file","/app/.env","--host", "0.0.0.0", "--port", "7860"]
