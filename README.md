# F1 Data Hub

A full-stack web application built with Python, Streamlit, and PostgreSQL to analyze, visualize and edit historical Formula 1 data.

This project is fully **Dockerized**, you can run it on any machine without needing to configure a local Python environment or install a local database server.

## Prerequisites

The only two things you'll need to run the app are:

1. Git (To clone the repository)
2. [Docker Desktop](https://www.docker.com/products/docker-desktop) (for the container, it will have to be running in the background for the app to work)

## Setup and start guide

Follow the steps you see to start the app:

### Step 1: Clone the repository
git clone https://github.com/alessandroMacchii/databasesqlexam.git
cd databasesqlexam

### Step 2: Start docker
download the docker desktop app and create an account 

### Step 3: Use docker from the terminal to start the container
type: docker compose up -d
keep in mind it might take a couple of minutes to get it started the first time

### Step 4: Load data
simply execute the two python files in this order
1. create_tables.py
2. load.py

### Step 5: Run the app
The application is now live and connected to the database.
Open any browser and go to:
http://localhost:8501

### Step 6: Enjoy!