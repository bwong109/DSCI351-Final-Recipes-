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

- `README.md`: This file, providing instructions and information about the program.
- `main.py`: Main Python script containing the recipe management system logic.
- `recipes.zip`: Compressed file containing the `recipes.csv` file. Extract this file to access the sample recipe data.

### Run the Program
1. Extract the `recipes.zip` file to access the `recipes.csv` file.
2. Open a terminal or command prompt.
3. Navigate to the directory containing `main.py` and `recipes.csv`.
4. Run the program using the following command:
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
