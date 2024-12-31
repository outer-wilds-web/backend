FROM python:3.10

# Alllow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the web service on container startup.
#CMD exec fastapi run --port 8000
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]

#FROM python:3.11
#
#WORKDIR /app
#
## Copy requirements file
#COPY requirements.txt .
#
## Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the rest of the application
#COPY . .
#
## Expose the port the app runs on
#EXPOSE 8001
#
## Command to run the application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]