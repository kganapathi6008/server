import os
import time
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import zipfile
from automation101 import get_urls
from dynamic import dynamic
import shutil
from datetime import datetime
from status import get_status
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

def delete_old_zip_files():
    current_working_directory = os.getcwd()
    files = os.listdir(current_working_directory)

    for file_name in files:
        if file_name.endswith('.zip') and 'extract' in file_name:
            file_path = os.path.join(current_working_directory, file_name)
            creation_time = os.path.getctime(file_path)
            if (time.time() - creation_time) > (24 * 60 * 60):
                os.remove(file_path)
def delete_extracted_folder(extracted_folder_path):
    if os.path.exists(extracted_folder_path):
        created_time = os.path.getctime(extracted_folder_path)
        current_time = time.time()
        time_difference = current_time - created_time
        twenty_four_hours = 24 * 60 * 60  # 24 hours in seconds

        if time_difference >= twenty_four_hours:
            shutil.rmtree(extracted_folder_path)





@app.route('/process_zip', methods=['POST'])
def process_zip():
    # Check if the request contains a file
    delete_old_zip_files()
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']

    # Check if the file has a filename
    if file.filename == '':
        return 'Empty filename', 400

    # Check if the file is a zip file
    if not file.filename.endswith('.zip'):
        return 'Invalid file format', 400

    # Save the zip file to the current working directory
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_with_timestamp = f"{timestamp}_{filename}"
    file_path = os.path.join(os.getcwd(), filename_with_timestamp)
    file.save(file_path)

    done_stuff = 0

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path101 = os.path.join(os.getcwd(), f"status_{current_time}.txt")
    with open(file_path101, "w") as file:
        file.write("Unzip in Process")


    # Extract the contents of the zip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    # Extract the contents of the zip file



    # Set the extracted folder path to the present working directory
    extracted_folder_path = os.path.join(os.getcwd(), os.path.splitext(filename)[0])


    extracted_file_name = os.path.basename(extracted_folder_path)


    # Delete the zip file
    os.remove(file_path)

    # Check if any files or directories were extracted
    extracted_files = [f for f in os.listdir(extracted_folder_path) if not f.endswith('.zip')]
    if len(extracted_files) == 0:
        # No files were extracted
        print('No files extracted')


    # Generate the dynamic folder and zip it
    current_working_directory = os.getcwd()
    zip_path = dynamic(extracted_folder_path, current_working_directory, extracted_file_name,file_path101)



    if os.path.exists(file_path101):
        os.remove(file_path101)

    # Return the zipped folder as a response
    response = send_file(zip_path, as_attachment=True)
    delete_extracted_folder(extracted_folder_path)


    return response






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
