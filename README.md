# Holiday Vacation Recommendation 🌎🌴

An interactive web application that recommends holiday destinations based on user-selected locations and personal descriptions. It uses a machine learning model to generate destination suggestions and displays results with descriptions and images.  

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
  
## Overview
The "Holiday Vacation Recommendation" web app helps users discover travel destinations by selecting a location and entering personal preferences. The app communicates with a FastAPI backend to generate recommendations based on the input, delivering suggestions with images and relevant details.

## Features
  * **Location Selection**: Choose a continent or country from a comprehensive list.  
  * **Custom Description Input**: Describe your ideal vacation experience to receive more tailored suggestions.  
  * **Recommendation Display**: Receive multiple destination suggestions, each with a description and accompanying image.  
  * **Dynamic Fetching**: Uses REST API to fetch recommendations based on user inputs.
  
## Demo

## Technologies Used
  * Frontend: HTML, CSS, JavaScript  
  * Backend: FastAPI (Python)  
  * Machine learning: Hugging Face's `sentence-transformers` for text embeddings  
  * Database/Storage: JSON and XLSX for storing holiday destination data  

## Getting Started
Follow these steps to set up and run the project locally.

## Prerequisites  
  * Python 3.11.4  
  * Node.js (for frontend setup if applicable)  
  * Git for cloning the repository  
  * Virtual environment (recommended for backend dependencies)  

## Installation
### 1. Clone the repository:  
    git clone https://github.com/TBao-THUer/Hackathon---Holiday-Vacation-Recommendation.git
    cd Hackathon---Holiday-Vacation-Recommendation
### 2. Backend Setup:  
  * Create a virtual environment and install dependencies:  
    ```bash  
    python -m venv env  
    source env/bin/activate  # On Windows, use `env\Scripts\activate`  
    pip install -r requirements.txt

    ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory (if your device raises this error, the code below can help you)  
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force 
    
   
  * Run the FastAPI server:  
    ```bash  
    uvicorn inference:app --reload  
    
### 3. Frontend Setup:  
  * Open `web.html` in your browser to launch the interface.
  * Alternatively, if using nmp or a live server.   
      ```bash
      npm install  
      npm start # or use live server extension in VSCode   
   
## Project Structure
    ```graphql
    .
    ├── backend                     # FastAPI backend for recommendations
    │   ├── inference.py            # Main API endpoint
    │   └── load_model.py           # Build and save the architecture and fine-tune weights model
    ├── files
    |   ├── best_model.weights.h5   # Save the weights model after fine-tuning
    |   ├── encoded_file.npy        # File saves all encoded destination embeddings
    |   ├── hackathons.xlsx         # File saves all destinations and their details we collected 
    |   ├── my_model.keras          # Files saves the architecture of model
    ├── frontend                    # HTML, CSS, and JS files for the UI
    │   ├── web.html                # Main HTML file for frontend
    │   └── style.css               # CSS file for frontend layout
    └── README.md                   # Project documentation
    └── requirements.txt            # Backend dependencies


## Usage  
1. Start the backend server:
     ```bash
     uvicorn inference:app --reload

3. Open `web.html` in your browser.
4. Select a location and enter your vacation description. Click "Search" or press "Enter" to receive recommendations.

## API Reference
**Endpoint** `/predict`
  * Method: `POST` 
  * Description: Accepts user preferences and returns a list of 5 recommended destinations.  
  * Request Body:  
    ```json
    {  
    "location": "Asia",  
    "description": "I enjoy beaches and historical landmarks."  
    }    
  * Response
    ```json
    [[ "Sukhothai Historical Park (Thailand): A site that combines natural beauty with historical ruins in a serene setting.", img_path_0], [ "Nusa Penida (Indonesia): Known for its stunning cliffs, beautiful beaches, and unique rock formations, a must-visit for nature lovers.", img_path_1], [ "Quy Nhon (Vietnam): A coastal city, known for its stunning beaches, ancient temples, and vibrant markets.", img_path_2 ], [ "Penghu Islands (Taiwan): A stunning archipelago known for its beautiful beaches, unique rock formations, and rich cultural history.", img_path_3 ], [ "Sentosa Island (Singapore): A resort destination featuring a world-renowned tourist attraction, beaches, water parks, and aquarium.", img_path_4]]

## Contributing  
  1. Fork the project.  
  2. Create a feature branch (`git checkout -b branch feature-name`).  
  3. Commit changes (`git commit -m "Add some feature"`).  
  4. Push to the branch (`git push origin feature-name`)  
  5. Open a pull request.  
