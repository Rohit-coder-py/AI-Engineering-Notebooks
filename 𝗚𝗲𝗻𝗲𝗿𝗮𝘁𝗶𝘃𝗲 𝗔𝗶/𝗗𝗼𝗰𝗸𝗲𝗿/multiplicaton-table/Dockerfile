
# Base image

FROM python:3.12

# Working directory

WORKDIR /table

# Copy project files

COPY . /table

# Install dependencies

RUN pip install -r requirements.txt

# Expose Streamlit port

EXPOSE 8501

# Run Streamlit application
CMD ["streamlit", "run", "table.py", "--server.address=0.0.0.0", "--server.port=8501"]
