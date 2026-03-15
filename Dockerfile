# ============================================================
# AWS DevOps Lab - Dockerfile (SOLUTION)
# ============================================================
# This is the SOLUTION file. Students should try writing
# their own Dockerfile first before looking at this!
# ============================================================

# Step 1: Use a lightweight Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file first (for Docker layer caching)
COPY app/requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code
COPY app/ .

# Step 6: Expose the port that the app listens on
EXPOSE 5000

# Step 7: Set environment variables
ENV FLASK_APP=app.py
ENV PORT=5000

# Step 8: Run the application using gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
