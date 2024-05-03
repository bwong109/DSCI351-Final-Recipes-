# Recipe Management System

## Overview
This Python program allows users to manage recipes using either MongoDB or DynamoDB as the backend database. Users can insert, delete, update, and search for recipes through a graphical user interface (GUI). The program utilizes CSV files to input recipe data and interacts with the chosen database based on user actions.

## Requirements
- Python
- Required Python packages (install using `pip install package_name`):
  - `boto3`
  - `pymongo`
  - `ipywidgets`
  - `IPython`

## File Structure
- `main.py`: Main Python script containing the recipe management system logic.
- `recipes.csv`: Sample CSV file containing recipe data for demonstration purposes.
- `README.md`: This file, providing instructions and information about the program.

## Commands to Run
1. **Run the Program**:
   ```bash
   python main.py

## Usage
1. Upon running the program, a graphical interface will appear.
2. Select the database type (MongoDB or DynamoDB) from the dropdown menu.
3. Use the provided input fields and buttons to perform operations:
  - Insert: Add a new recipe.
  - Delete: Remove a recipe by title.
  - Update: Modify a recipe by title.
  - Search: Find recipes by title.

## Note to User:
- Make sure to have MongoDB running locally if using MongoDB as the database
- AWS credentials should be connected to DynamoDB per given key
