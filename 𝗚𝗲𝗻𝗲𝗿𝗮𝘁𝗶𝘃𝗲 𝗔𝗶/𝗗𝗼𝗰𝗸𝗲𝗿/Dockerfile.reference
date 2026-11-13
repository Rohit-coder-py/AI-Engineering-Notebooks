
# 1. Select the base image
FROM python:3.12-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements file
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all project files
COPY . .

# 6. Expose application port
EXPOSE 8501

# 7. Run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
