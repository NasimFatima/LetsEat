FROM python:3.7.4

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies.
RUN pip install --no-cache-dir -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

#set permission for our bash file
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]  # we run django through this bashfile later

# RUN python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

# CMD export ENV_Setting=development && python manage.py makemigrations && python manage.py migrate && python manage.py runserver
