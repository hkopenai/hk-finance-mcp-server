# Multi-stage build for a slimmer image
# Stage 1: Build dependencies
FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml .
COPY hkopenai/ ./hkopenai/
RUN pip install --user --no-cache-dir .

# Stage 2: Runtime image
FROM python:3.13-slim
WORKDIR /app
# Copy only the necessary files from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy the application code
COPY hkopenai/ ./hkopenai/
COPY LICENSE .
COPY README.md .
# Set PATH to include user-installed packages
ENV PATH=/root/.local/bin:$PATH
# Expose the port the app runs on
EXPOSE 8000
# Command to run the MCP server in SSE
CMD ["python", "-m", "hkopenai.hk_finance_mcp_server", "--sse", "--host", "0.0.0.0"]
