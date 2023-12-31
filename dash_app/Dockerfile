# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-buster

# Copy local code to the container image.
ENV APP_HOME /dash_app
ENV PYTHONUNBUFFERED True
ENV GOOGLE_APPLICATION_CREDENTIALS /dash_app/firebase_creds/tasm-visitor-signin-firebase-adminsdk-2yhi8-de7e26b1da.json
WORKDIR $APP_HOME

# Install Python dependencies and Gunicorn
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn
RUN groupadd -r app && useradd -r -g app app

# Copy the rest of the codebase into the image
COPY --chown=app:app . ./
USER app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
CMD exec gunicorn --bind :8080 --log-level info --workers 1 --threads 8 --timeout 0 app:server
