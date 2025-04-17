FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv pip install -e .

# Expose port if needed
# EXPOSE 8000

# Run the server
CMD ["python", "run_server.py"] 