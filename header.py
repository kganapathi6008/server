import pandas as pd

def header(url, my_list, user_choice,):
    data = {
        'Mapping Description': [''],
        'Mapping Name': [''],
        'Mapping Task Name': [''],
        'Task flow Name': [''],
        'Scheduler details (if any)': [''],
        'Source Table': [''],
        'Target Tables': ['']
    }

    # Update the dictionary with non-empty values


    data['Mapping Name'][0] = ''.join(user_choice)
    if my_list:
        data['Source Table'][0] = ', '.join(my_list)




    return data
