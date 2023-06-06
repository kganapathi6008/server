import pandas as pd
import os
import xlsxwriter
from testrun import testrun
import openpyxl

def combine(df, df1, folder_path, user_choice, data, list_list, df_user_final, dfdata, my_list, join_list_final, res_map_des, header_list, data_list, data_const, data_para, data_index,ylist,push_def,dataframes1,headingsxx):
    dftest = testrun(user_choice, my_list, list_list, join_list_final, res_map_des, header_list, data_list,ylist)
    data['Target Tables'][0] = ', '.join(list_list)

    output_file = f"{user_choice}.xlsx"
    output_path = os.path.join(folder_path, output_file)
    stxx=2

    # Write the dataframes to the Excel file
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Write the first dataframe to the Excel file starting from the 9th row
        dftest.to_excel(writer, sheet_name='Sheet1', startrow=1, index=False, header=True)
        start_row = 15

        # Check and write data_para to Excel
        #if data_para is not None and data_para.shape[0] > 0:
        end_row = start_row + data_para.shape[0]
        data_para.to_excel(writer, sheet_name='Sheet1', startrow=start_row, index=False, header=True)
        #else:
            #end_row = start_row

        start_rowq = end_row + 2

        # Check and write data_index to Excel
        if data_index is not None and data_index.shape[0] > 0:
            end_rowq = start_rowq + data_index.shape[0]
            data_index.to_excel(writer, sheet_name='Sheet1', startrow=start_rowq, index=False, header=True)
        else:
            end_rowq = start_rowq

        start_rowz = end_rowq + 2

        # Check and write df_user_final to Excel
        if df_user_final is not None and df_user_final.shape[0] > 0:
            end_rowz = start_rowz + df_user_final.shape[0]
            df_user_final.to_excel(writer, sheet_name='Sheet1', startrow=start_rowz, index=False, header=True)
        else:
            end_rowz = start_rowz

        # Write dfdata, data_const, df, and df1 to Excel, handling overlaps
        start_rowV = end_rowz + 2
        if dfdata is not None and dfdata.shape[0] > 0:
            end_rowV = start_rowV + dfdata.shape[0]
            dfdata.to_excel(writer, sheet_name='Sheet1', startrow=start_rowV, index=False, header=True)

            if data_const is not None and data_const.shape[0] > 0:
                start_rowC = end_rowV + 2
                end_rowC = start_rowC + data_const.shape[0]
                data_const.to_excel(writer, sheet_name='Sheet1', startrow=start_rowC, index=False, header=True)
                df.to_excel(writer, sheet_name='Sheet1', startrow=end_rowC + 2, index=False, header=True)

                if push_def is not None and push_def.shape[0] > 0:
                    push_def.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowC + 4, index=False,
                                      header=True)

                df1.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowC + 9, index=False, header=True)
            else:
                df.to_excel(writer, sheet_name='Sheet1', startrow=end_rowV + 2, index=False, header=True)

                if push_def is not None and push_def.shape[0] > 0:
                    push_def.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowV + 4, index=False,
                                      header=True)

                df1.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowV + 9, index=False, header=True)
        elif data_const is not None and data_const.shape[0] > 0:
            start_rowV = end_rowz + 2
            start_rowC = start_rowV
            end_rowC = start_rowC + data_const.shape[0]
            data_const.to_excel(writer, sheet_name='Sheet1', startrow=start_rowC, index=False, header=True)
            df.to_excel(writer, sheet_name='Sheet1', startrow=end_rowC + 2, index=False, header=True)

            if push_def is not None and push_def.shape[0] > 0:
                push_def.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowC + 4, index=False,
                                  header=True)

            df1.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + end_rowC + 9, index=False, header=True)
        else:
            start_rowV = end_rowz + 2
            df.to_excel(writer, sheet_name='Sheet1', startrow=start_rowV, index=False, header=True)

            if push_def is not None and push_def.shape[0] > 0:
                push_def.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + start_rowV + 4, index=False,
                                  header=True)

            df1.to_excel(writer, sheet_name='Sheet1', startrow=df.shape[0] + start_rowV + 9, index=False, header=True)
        #for df_sourcexx in dataframes1:

            #df_sourcexx.to_excel(writer, sheet_name='Sheet2', startrow=stxx, index=False, header=True)
            #stxx=stxx+ df_sourcexx.shape[0]+2
        for df_sourcexx, heading in zip(dataframes1, headingsxx):
            # Add the heading to the Excel sheet before the DataFrame
            heading_row = pd.DataFrame([[heading]], columns=['Heading'])
            heading_row.to_excel(writer, sheet_name='Source Tables', startrow=stxx+3, index=False, header=False)

            # Save the DataFrame to the Excel sheet
            df_sourcexx.to_excel(writer, sheet_name='Source Tables', startrow=stxx + 5, index=False, header=True)

            # Update the startrow for the next iteration
            stxx = stxx + df_sourcexx.shape[0] + 7
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        if df_user_final is not None and df_user_final.shape[0] > 0:
            # Fill the first column cells with the value "User Defined Function"
            for row in range(start_rowz, end_rowz):
                worksheet.write(row, 0, "User Defined Function")

            # merge cells and apply formatting
            worksheet.merge_range(start_rowz, 0, end_rowz, 0, "User Defined Functions",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        if dfdata is not None and dfdata.shape[0] > 0:
            # Fill the first column cells with the value "Use Defined Function"
            for row in range(start_rowV, end_rowV + 1):
                worksheet.write(row, 0, "Use Defined Function")

            worksheet.merge_range(start_rowV, 0, end_rowV + 1, 0, "Virtual Elements",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        if data_const is not None and data_const.shape[0] > 0:
            for row in range(start_rowC, end_rowC + 1):
                worksheet.write(row, 0, "Constants")

            worksheet.merge_range(start_rowC, 0, end_rowC + 1, 0, "Constants",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        #if data_para is not None and data_para.shape[0] > 0:
                # Fill the first column cells with the value "Use Defined Function"
        for row in range(start_row, end_row+1):
            worksheet.write(row, 0, "Parameters")

        worksheet.merge_range(start_row, 0, end_row+1, 0, "Parameters",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        if data_index is not None and data_index.shape[0] > 0:
                # Fill the first column cells with the value "Use Defined Function"
            for row in range(start_rowq, end_rowq):
                worksheet.write(row, 0, "Index")

            worksheet.merge_range(start_rowq, 0, end_rowq, 0, "Index",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        for row in range(9, 10):
                    worksheet.write(row, 0, "CDC Table")

        worksheet.merge_range(9, 0, 10 , 0, "CDC Table",
                                      workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))
        if push_def is not None and push_def.shape[0] > 0:
            # Calculate the start and end rows based on the available data
            if dfdata is None and data_const is None:
                start_row_push_def = end_rowz + 2

            elif dfdata is None and data_const is not None and data_const.shape[0]>0:
                start_row_push_def = end_rowC + 2

            elif data_const.shape[0]<1 and dfdata is not None and dfdata.shape[0]>0:
                start_row_push_def = df.shape[0] + end_rowV + 4

            elif dfdata is not None and dfdata.shape[0]>0 and data_const is not None and data_const.shape[0]>0:


                 start_row_push_def=df.shape[0] + end_rowC + 4
            else:


                start_row_push_def = df.shape[0] + start_rowV + 6


            # Fill the first column cells with the value "Use Defined Function"
            for row in range(start_row_push_def, start_row_push_def + 3):
                worksheet.write(row, 0, "Index")

            worksheet.merge_range(start_row_push_def, 0, start_row_push_def + 3, 0, "Push Definitions",
                                  workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'}))

            # Set the column widths to auto-fit
        for i, col in enumerate(df.columns):
            col_str = str(col)
            max_width = max(df[col_str].astype(str).map(len).max(), len(col_str))
            #max_width = max(df[col].astype(str).map(len).max(), len(col))
            worksheet.set_column(i, i, max_width)


    return output_path

