# Use a Red Hat UBI 8 image as the base, which is compatible with RHEL 9.
FROM redhat/ubi8

# Set the working directory inside the container.
WORKDIR /app

# Copy the application and test files into the container.
COPY app.py .
COPY test.py .

# Install Python 3, pip, and the required Python libraries.
# The 'yum' command is used for package management on RHEL-based systems.
RUN yum install -y python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip

# Install Flask and pytest, which are needed for your application and tests.
RUN pip3 install flask pytest

# Set the ENTRYPOINT to run the tests.
# This is specifically for the test stage of your pipeline.
# The `Jenkinsfile` will override this entrypoint for the final deployment.
ENTRYPOINT ["pytest", "test.py"]

# Expose port 5000, which is the default port for your Flask application.
EXPOSE 5000