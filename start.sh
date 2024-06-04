#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app with uvicorn
uvicorn main:app --reload