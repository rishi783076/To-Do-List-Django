# # The first instruction is what image we want to base our container on
# # We Use an official Python runtime as a parent image
# FROM python:3.10
# # The enviroment variable ensures that the python output is set straight
# # to the terminal with out buffering it first
# ENV PYTHONUNBUFFERED 1
# # create root directory for our project in the container
# RUN mkdir /webapp
# WORKDIR /webapp
# COPY requirements.txt .
# ADD . /webapp/
# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# #Expose the port on which the Django development server will run (change if needed)
# EXPOSE 8000
# # Run the Django development server
# # CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # for volumes
# # RUN mkdir -p /vol/todo_list/static && \
# #     mkdir -p /vol/todo_list/media && \
# #     chown -R app:app /vol && \
# #     chmod -R 755 /vol && \
# # RUN chmod -R +x /scripts

# ENV PATH="/scripts:/py/bin:$PATH"

# USER webapp

# CMD ["run.sh"]

# base image  
FROM python:3.10   
# setup environment variable  
# ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir /webapp

# where your code lives  
WORKDIR /webapp

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY requirements.txt .
ADD . /webapp/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# run this command to install all dependencies  
# RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]   