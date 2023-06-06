import pandas as pd
import numpy as np

def testrun(user_choice,my_list,list_list,join_list_final,res_map_des,header_list,data_list,ylist):
    # Create an empty DataFrame with 20 columns and 5 rows

    df = pd.DataFrame(columns=[''] * 20, index=range(12))

    # Assign values to the first column
    df.iloc[:, 0] = ['Mapping Description', 'Mapping Name :', 'Mapping Task Name :', 'Task flow Name :', 'Scheduler details (if any) :','Source Table :','Target Tables :','CDC Tables','','Additional Filters/Join Conditions (if any) :','Business Rules (If any)','']

    # Select the subset of the DataFrame without the first row and first four columns

    df.iloc[1, 1] = user_choice
    df.iloc[3, 2] = user_choice
    df.iloc[0, 1] = res_map_des
    df.iloc[3, 1] = res_map_des

    # Write the contents of my_list to the 3rd row, starting from the 4th column
    df.iloc[5, 1:1 + len(my_list)] = my_list
    df.iloc[6, 1:1 + len(list_list)] = list_list
    df.iloc[9, 1:1 + len(join_list_final)] = join_list_final
    df.iloc[10, 1:1 + len(header_list)] = header_list
    df.iloc[11, 1:1 + len(data_list)] = data_list
    # Create the new DataFrame with one row and two columns

    xlist=[]

    xlist.append('Source Table')
    xlist.append('CDC Output')

    df.iloc[7, 1:1 + len(xlist)] = xlist
    df.iloc[8, 1:1 + len(xlist)] = ylist


    return df
