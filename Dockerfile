# Deriving the latest base image
FROM python:latest

# Labels as key value pair
LABEL Maintainer="abhay8330"

# to COPY the remote file at working directory in container
COPY . ./assignment

# Set working directory
WORKDIR /assignment

# Install Python Modules
RUN pip install -r requirements.txt

#ENTRYPOINT instruction should be used to run the software contained by your image, along with any arguments.

ENTRYPOINT [ "python", "/assignment/assignment.py"]