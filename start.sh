#!/bin/bash

# Step 1: Create a virtual environment if it doesn't already exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies from requirements.txt if the file exists
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  echo "No requirements.txt file found. Please create it or install packages manually."
fi

# Step 4: Create Django project if it doesn't exist
if [ ! -d "etl_project" ]; then
  echo "Creating Django project..."
  django-admin startproject etl_project
fi

# Step 5: Create Django app 'api' if it doesn't exist
if [ ! -d "etl_project/api" ]; then
  echo "Creating Django app 'api'..."
  cd etl_project
  python manage.py startapp api
  cd ..
fi

# Optional: Step 6 - Run Django server (comment this out if not needed)
echo "Starting Django development server..."
python etl_project/manage.py migrate
python etl_project/manage.py runserver