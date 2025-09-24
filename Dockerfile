# --- Stage 1: The Builder ---
# This stage installs dependencies and downloads the heavy ML model
FROM python:3.11-slim as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install all dependencies
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Run the download script to fetch the model into the /app/models/ directory
RUN python download_model.py

# --- Stage 2: The Final Image ---
# This stage creates the final, lean image for running the application
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# This command now works because we explicitly created the 'models' folder
COPY --from=builder /app/models /app/models

# Copy your application code
COPY --from=builder /app /app

# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# The command to run when the container starts
# It starts both the backend API and the frontend UI
# NOTE: For production, a process manager like supervisord is recommended.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"]
