import os

def get_status():
    files = [file for file in os.listdir() if file.endswith(".txt") and "status" in file.lower()]

    if files:
        file_path = files[0]

        try:
            with open(file_path, "r") as file:
                file_content = file.read()
            return file_content
        except FileNotFoundError:
            return f"No '{file_path}' file found."
    else:
        return "We are working on it"

