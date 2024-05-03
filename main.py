import csv
import boto3
from boto3.dynamodb.conditions import Key
from pymongo import MongoClient
import ipywidgets as widgets
from IPython.display import display, clear_output

# Function to read data from CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Function to connect to MongoDB
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipe_database']
    collection = db['recipes']
    return collection

# Function to insert data into MongoDB with ingredients as an array
def insert_data_mongodb(collection, data):
    for item in data:
        item["Ingredients"] = item["Ingredients"].split(",")
    collection.insert_many(data)
    print("Data inserted successfully!")
    output_info.clear_output()

# Function to delete a recipe by title from MongoDB
def delete_by_title_mongodb(collection, title):
    collection.delete_one({"Title": title})
    print("Recipe deleted successfully!")
    # Clear the output widget after deleting a recipe
    output_info.clear_output()

# Function to delete a recipe by title in DynamoDB
def delete_by_title_dynamodb(table, title):
    table.delete_item(Key={"Title": title})
    print("Recipe deleted successfully!")
    output_info.clear_output()

# Function to update a recipe by title in MongoDB
def update_by_title_mongodb(collection, title, new_data):
    new_ingredients = new_data['Ingredients'].split(",")
    collection.update_one({"Title": title}, {"$set": {"Ingredients": new_ingredients, "Instructions": new_data['Instructions']}})
    print("Recipe updated successfully!")

# Function to update a recipe by title in DynamoDB
def update_by_title_dynamodb(table, title, new_data):
    new_ingredients = new_data.get('Ingredients', '').split(",")
    update_expression = "SET Ingredients = :i, Instructions = :ins"
    expression_attribute_values = {':i': new_ingredients, ':ins': new_data.get('Instructions', '')}
    if 'Image_Name' in new_data:
        update_expression += ", Image_Name = :img"
        expression_attribute_values[':img'] = new_data['Image_Name']
    table.update_item(
        Key={"Title": title},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    print("Recipe updated successfully!")


# Function to search for recipes by title in MongoDB (10 results for demonstration purposes)
def search_by_title_mongodb(collection, title):
    return list(collection.find({"Title": {"$regex": title, "$options": "i"}}).limit(10))

def search_by_title_dynamodb(table, query):
    response = table.query(
        KeyConditionExpression=Key('Title').eq(query)
    )
    items = response['Items']
    return items

# Function to connect to DynamoDB
def connect_to_dynamodb():
    session = boto3.Session(
        aws_access_key_id='AKIAZQ3DUZQWT24YPIA5',
        aws_secret_access_key='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',
        region_name='us-east-2'
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('recipes')
    return table

# Function to insert data into DynamoDB with ingredients as an array
def insert_data_dynamodb(table, data):
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)
    print("Data inserted successfully!")
    output_info.clear_output()

# Function to read data from CSV file for DynamoDB
def read_csv_dynamodb(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row["Ingredients"] = row["Ingredients"].split(",")
            data.append(row)
    return data


# GUI for interacting with the application
def main():
    file_path = 'recipes.csv'
    data_mongodb = read_csv(file_path)
    
    # Connect to MongoDB
    collection_mongodb = connect_to_mongodb()
    
    # Connect to DynamoDB
    table_dynamodb = connect_to_dynamodb()
    
    
    # GUI elements
    db_selector = widgets.Dropdown(options=['MongoDB', 'DynamoDB'], description='Database:')
    
    title_input_insert = widgets.Text(description='Title:')
    ingredients_input_insert = widgets.Textarea(description='Ingredients:')
    instructions_input_insert = widgets.Textarea(description='Instructions:')
    insert_button = widgets.Button(description='Insert')
    
    title_input_delete = widgets.Text(description='Delete by Title:')
    delete_button = widgets.Button(description='Delete')
    
    title_input_update = widgets.Text(description='Title to Update:')
    new_ingredients_input_update = widgets.Textarea(description='New Ingredients:')
    new_instructions_input_update = widgets.Textarea(description='New Instructions:')
    update_button = widgets.Button(description='Update')
    
    title_input_search = widgets.Text(description='Search by Title:')
    search_button = widgets.Button(description='Search')
    output_search = widgets.Output()
    global output_info
    output_info = widgets.Output()

    # Event handlers
    def insert_button_clicked(b):
        if db_selector.value == 'MongoDB':
            insert_data_mongodb(collection_mongodb, [{
                "Title": title_input_insert.value,
                "Ingredients": ingredients_input_insert.value,
                "Instructions": instructions_input_insert.value,
            }])
        elif db_selector.value == 'DynamoDB':
            insert_data_dynamodb(table_dynamodb, [{
                "Title": title_input_insert.value,
                "Ingredients": ingredients_input_insert.value,
                "Instructions": instructions_input_insert.value,
            }])

    def delete_button_clicked(b):
        if db_selector.value == 'MongoDB':
            delete_by_title_mongodb(collection_mongodb, title_input_delete.value)
        elif db_selector.value == 'DynamoDB':
            delete_by_title_dynamodb(table_dynamodb, title_input_delete.value)

    def update_button_clicked(b):
        new_data = {
            "Ingredients": new_ingredients_input_update.value,
            "Instructions": new_instructions_input_update.value,
        }
        if db_selector.value == 'MongoDB':
            update_by_title_mongodb(collection_mongodb, title_input_update.value, new_data)
        elif db_selector.value == 'DynamoDB':
            update_by_title_dynamodb(table_dynamodb, title_input_update.value, new_data)

    def search_button_clicked(b):
        with output_search:
            output_search.clear_output()
            if db_selector.value == 'MongoDB':
                search_results = search_by_title_mongodb(collection_mongodb, title_input_search.value)
            elif db_selector.value == 'DynamoDB':
                search_results = search_by_title_dynamodb(table_dynamodb, title_input_search.value)

            if search_results:
                if len(search_results) == 1:
                    display_recipe_info(search_results[0], output_info)
                else:
                    print("Select a recipe:")
                    recipe_dropdown = widgets.Dropdown(options=[(recipe['Title'], recipe) for recipe in search_results])
                    display(recipe_dropdown)
                    recipe_dropdown.observe(dropdown_callback, names='value')
            else:
                print("No recipes found.")
    
    def display_recipe_info(recipe, output_widget):
        output_widget.clear_output()
        with output_widget:
            print("Title:", recipe['Title'])
            # Check if Ingredients is a list or a string
            if isinstance(recipe['Ingredients'], list):
                print("Ingredients:")
                ingredients_str = ', '.join(recipe['Ingredients'])
                print(ingredients_str)
            else:
                print("Ingredients:", recipe['Ingredients'])
            print("Instructions:", recipe['Instructions'])
            if 'Image_Name' in recipe:
                print("Image Name:", recipe['Image_Name'])


    def dropdown_callback(change):
        if change.new:
            display_recipe_info(change.new, output_info)

    # Event bindings
    insert_button.on_click(insert_button_clicked)
    delete_button.on_click(delete_button_clicked)
    update_button.on_click(update_button_clicked)
    search_button.on_click(search_button_clicked)

    # GUI
    insert_widgets = [title_input_insert, ingredients_input_insert, instructions_input_insert, insert_button]
    delete_widgets = [title_input_delete, delete_button]
    update_widgets = [title_input_update, new_ingredients_input_update, new_instructions_input_update, update_button]
    search_widgets = [title_input_search, search_button, output_search, output_info]

    display(db_selector)
    display(widgets.VBox(insert_widgets))
    display(widgets.VBox(delete_widgets))
    display(widgets.VBox(update_widgets))
    display(widgets.VBox(search_widgets))

if __name__ == "__main__":
    main()
