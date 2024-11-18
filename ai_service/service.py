import pandas as pd
from ai_service.watson_llm import llm
from pandasai import Agent
from pandasai import SmartDatalake
import os
from typing import List, Dict, Any
import json
import time

llm = llm

# datasets = ['data/Amazon Sale Report.csv','data/Financial Statements.csv',
#             'data/Sale Report.csv','data/May-2022.csv','data/women_clothing_ecommerce_sales.csv',
#             'data/Sales Product Ecommerce.csv']

# Ensure the user-defined path exists
user_defined_path = 'backend/static/ai_media'

if not os.path.exists(user_defined_path):
    os.makedirs(user_defined_path)

# Define the function
def process_datasets(datasets: List[str], query: str) -> Dict[str, any]:
    try:
        # Ensure the user-defined path exists
        if not os.path.exists(user_defined_path):
            os.makedirs(user_defined_path)
        
        # Get the initial state of the directory
        initial_files = {f: os.stat(os.path.join(user_defined_path, f)).st_mtime for f in os.listdir(user_defined_path)}

        # Run the SmartDatalake process
        lake = SmartDatalake(datasets, config={
            "llm": llm,
            "save_charts": True,
            "save_charts_path": user_defined_path,
            "enable_cache": False,
        })
        output = lake.chat(query)

        # Convert output to string if necessary
        output_str = str(output)

        # Wait until function completes execution
        time.sleep(1)

        # Check for newly added or modified files
        final_files = {f: os.stat(os.path.join(user_defined_path, f)).st_mtime for f in os.listdir(user_defined_path)}
        new_or_modified_files = [
            os.path.join('static/ai_media', file)  # Return relative paths
            for file, mtime in final_files.items()
            if file not in initial_files or mtime > initial_files[file]
        ]

        # Create the result dictionary
        result = {
            "output": output_str,
            "images": new_or_modified_files  # Use URLs relative to the static route
        }

    except Exception as e:
        result = {
            "error": str(e),
            "images": []
        }
    
    return json.dumps(result)
# # Example Usage
# if __name__ == "__main__":
    
#     # query = "which compnay would you advise me to invest in?"
#     # response = process_datasets(datasets, query)
#     # print(response)

# query = " what top 10 products generate most revenue"

# lake = SmartDatalake(datasets, config={
#     "llm": llm,
#     "save_charts": True,
#     "save_charts_path": user_defined_path,
#     "enable_cache": False}
#     )

# output = lake.chat(query)
# print(output)
# print(type(output))