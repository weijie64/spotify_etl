FROM apache/airflow:2.7.2-python3.10

# Copy your project files into the container
COPY ./scripts /opt/airflow/scripts

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/scripts"
