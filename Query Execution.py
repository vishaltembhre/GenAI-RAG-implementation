import pandas as pd
import os, sys
from datetime impaort datetime,timedelta
import psycopg2
import matplotlib as plt
import win32com.client as win32
import shutil
import time

def schedule(hrs=0,mins=0):
    waiting_time = hrs*60*60 + mins*60
    Curr_Time = datetime.now()
    Execution_time = Curr_Time + timedelta(hours=hrs,minutes=mins)
    print('The Script Will Execute at - ' + str(Execution_time),'\n')
    time.sleep(waiting_time)
 
def zip_folder(folder_path, zip_filename, destination_path):
    try:
        # Create the zip file
        shutil.make_archive(zip_filename, 'zip', folder_path)
       
        # Move the zip file to the destination path
        shutil.move(f"{zip_filename}.zip", destination_path)
 
        print(f"Folder '{folder_path}' zipped and moved successfully to '{destination_path}'.")
    except Exception as e:
        print(f"Error zipping and moving folder: {e}")
 
def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd="\r"):
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
 
def PlotPieChart(dfl,txt):
    #plotting pie chart -- start
    PlotResultD = dfl[dfl.columns[1]].tolist()
    PlotResultL = dfl[dfl.columns[0]].tolist()
    plt.figure(figsize=(8, 8))
    plt.pie(PlotResultD, labels=PlotResultL, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(txt)
    plt.savefig(f'{txt}.png')
    plt.show()
    ##plotting pie chart -- end
 
def handle_failed_query(ferror,conn,cursor, sql):
    error = sys.exc_info()[1]
    ferror.write(f'{sql} - {error}\n')
    #print('Failed to execute query:', sql, error)  #Uncomment if wanted to have real-time look at Errors while script is executing
    conn.rollback()
 
def clean_data(value):
    # Use regex and string manipulation to extract the string within quotes
    cleaned_value = value.str.extract(r"\'([^\']+)\'")[:]
    return cleaned_value
 
def Clean(df):  
    for column in df.columns:
        data_type = df[column].dtype
        if data_type == 'object':
            df[column] =  clean_data(df[column].astype(str))
 
#Update connection setting as per environment
def Connect_PROD():
    conn= psycopg2.connect(
    host='database-PROD.redshift.amazonaws.com',
    dbname='database',
    user='Read_Access',
    password='password',
    port='5439'  #default port for redshift Database, update as per required database
    )
    return conn
 
def Connect_SIT():
    conn= psycopg2.connect(
    host='database-SIT.redshift.amazonaws.com',
    dbname='database',
    user='Read_Access',
    password='password',
    port='5439'  #default port for redshift Database, update as per required database
    )
    return conn


def main():
 
    #Update for scheduling
    #schedule(),schedule(hrs = 1,mins =20),schedule(hrs = 1),schedule(mins = 20)
    #schedule(1,20),schedule(1)
    schedule(hrs = 1,mins =4)
 
    #User Input - START
    conn = Connect_PROD()
    cursor = conn.cursor()
 
    #Update as per Execution
    OutputFileName = 'ProgressDemo' #'09APR_LIB_BSNSS_PREPROD' #05MAR_DUPIXENT_DWH_SIT
    SqlScriptNM = 'count.sql'
 
    #Initialise Directory
    SQLLocation = 'C:/Users/Documents/Migration/PreProd/'
    OutputLocation = 'C:/Users/Documents/Migration/PreProd/'+OutputFileName+'/'
   
    #to zip output folder
    FolderToZip = SQLLocation+ 'Output2/' + OutputFileName
    ZipFilename = OutputFileName + '.zip'
    ZipFileLocation = r'C:\Users\Documents\Migration\PreProd\Output2\ZipLog\\' + ZipFilename
 
    columns = ['Table_Name', 'Dbcut_Count', 'Reinvent_Count', 'Mismatch_Count', 'Mismatch_Percentage', 'Result']
   
    if os.path.exists(OutputLocation):
        shutil.rmtree(OutputLocation)
   
    os.makedirs(OutputLocation)
 
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.Subject = OutputFileName + ' Automation Execution Completed'
    mail.To = 'abc@gmail.com'
    mail.cc = 'abc@gmail.com'


    #User Input - END
 
    logNm = OutputLocation  + 'ExecutionLog.csv'
    ErrorLgNm = OutputLocation  + 'ErrorLog.txt'
    SQLLgNm = OutputLocation  + 'SQLQuery.txt'
    FormattedLgNm = OutputLocation  + OutputFileName +'.xlsx'
 
    fin = open( SQLLocation + SqlScriptNM, 'r')
    fout = open(  logNm , 'a')
    ferror = open(  ErrorLgNm, 'a')
    fSQL = open(  SQLLgNm, 'a')
 
    fout.truncate(0)
    ferror.truncate(0)
    fSQL.truncate(0)
    start_time = datetime.now()
    print("Test Execution Start time", start_time)  #Script Execution Start Time
   
    sqls = fin.readlines()


    ScriptLen = len(sqls) + 1
    #initialse Progress Bar
    print_progress(0, ScriptLen, prefix='Progress:', suffix='Complete', length=50)
    i=0
    for sql in sqls:
        i=i+1
        fSQL.write(sql + '\n')
        try:
             cursor.execute(sql)
        except Exception as Error:
            if isinstance(Error, psycopg2.errors.InFailedSqlTransaction):
                handle_failed_query(ferror,conn,cursor,sql)
                conn.rollback()
            else:
                handle_failed_query(ferror,conn,cursor,sql)
        else:
            row = cursor.fetchall()
            fout.write(f'{row}\n')
            print_progress(i + 1 , ScriptLen, prefix='Progress:', suffix='Complete', length=50)
           
    fout.close()
    fin.close()
    ferror.close()
    fSQL.close()
    end_time = datetime.now()
    print("Test Execution End time", end_time ) #Script Execution End Time
 
    time_difference = end_time - start_time
 
    try:
        df = pd.read_csv( logNm, header=None)
        df.columns = columns
 
        Clean(df)
        #print(df)
        df.to_excel( FormattedLgNm , index=False)
 
        ResultDF = df['Result'].value_counts(dropna=False).to_frame().reset_index()
        ResultDF.columns = ['Result', 'Count']
        ResultDF.loc[len(df)] = ResultDF['Count'].sum()
        #print(ResultDF)
 
        df['Mismatch_Percentage'] = df['Mismatch_Percentage'].astype(float)
 
        bins = [0,1,5,25,100]
        labels = ['0-1', '1-5','5-25', '25-100']
 
        df['Category'] = pd.cut(df['Mismatch_Percentage'], bins=bins, labels=labels)
 
        MismatchDistibutionDf = df['Category'].value_counts(dropna=False).to_frame().reset_index()
        MismatchDistibutionDf.columns = ['Category', 'Count']
        MismatchDistibutionDf.loc[len(df)] = MismatchDistibutionDf['Count'].sum()
 
        # Write the result to a new sheet
        with pd.ExcelWriter( FormattedLgNm , engine='openpyxl', mode='a') as writer:
            MismatchDistibutionDf.to_excel(writer, sheet_name='Mismatch Distibution', index=False)
            ResultDF.to_excel(writer, sheet_name='Result Summary', index=False)
    except:
        print('Error in Formatting CSV')
 
   
    '''
    try:
        PlotPieChart(ResultDF,'Result_Summary')
        PlotPieChart(MismatchDistibutionDf,'Mismatch_Distribution_Summary')
    except:
        print('Error in plotting chart') '''
 
    mail.Body = '''
    #######################################################
 
    Hello,
 
    This is Auto-Generated E-Mail.
    PFA the execution log & error log along with formatted output.
    Total execution Time - ''' + str(time_difference) + '''
 
    Regards,
    Python
 
    #######################################################'''
   
    try:
        zip_folder(FolderToZip,ZipFilename,ZipFileLocation)
    except:
        print('Zip Not Working')
 
    try:
        attachment_paths = [ZipFileLocation]
        for attachment_path in attachment_paths:
            mail.Attachments.Add(attachment_path)
    except:
        print('Attachment Not Working')
 
    mail.Send()
 
    print("Email sent successfully!")


if __name__ == '__main__':
    main()



