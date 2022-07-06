from collections import defaultdict
from fileinput import filename
from re import sub
import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np
import subprocess
import time

#parse the path of the manifest fil
root = ET.parse("C:\\Users\\basam\\Documents\\Unscaffold\\Tiktok\\TikTok\\AndroidManifest.xml").getroot()

permissions = root.findall("uses-permission")
permissions2 = root.findall("uses-feature")
permissions3 = root.findall("permission")

exported_key = "{http://schemas.android.com/apk/res/ndroid}exported"

application = root.find("application")
content_provider = application.findall("provider")
for provider in  application.findall("provider"): 
    if [provider.attrib] == "true":
        print (provider)

filename = "tiktok.csv"
content_filename = "tiktok_content.csv"

def extract_data(p):
    result = defaultdict(list)
    for perm in p:
        for att in perm.attrib:
            result[att].append(perm.attrib[att])
    return result



data = extract_data(permissions)


data1 = extract_data(permissions2)


data2 = extract_data(permissions3)


data3 = extract_data(content_provider)


#check if key expoertd true is in data3
key = "{http://schemas.android.com/apk/res/android}exported"
key_authority = "{http://schemas.android.com/apk/res/android}authorities"
def check_key(data3, key):
    if key in data3:
        #check if it has the value of true
        if "true" in data3[key]:
            #return total number of true values
            return data3[key].count("true")
        else:
            #return 0 if there are no true values
            return 0    
    else:
        return False



#return dictionary index of each repeating true value in data3
def get_index(data3, key):
    if key in data3:
        #return  dictionary
        indice= [i for i, x in enumerate(data3[key]) if x == "true"]
        return indice
    else:
        return False


#index = get_index(data3, key)
indices = get_index(data3, key)
#locate values at this indices [1,2,9,20]
#indices = [1,2,10,21]
def get_authority(data3, key_authority, indices):
    if key_authority in data3:
        #return  values at these indices
        return [data3[key_authority][i] for i in indices]
    else:
        return False

data_check = check_key(data3, key)

index = get_index(data3, key)
authorities = get_authority(data3, key_authority, indices)


#run each value in authorities in adb shell Content query content:// then pass quthority using subprocess
for authority in authorities:
    subprocess.call(["adb", "shell", "Content", "query", "uri", "content://", authority], shell=True)
    time.sleep(1)
# subprocess.call(["adb", "shell", "Content", "query", "content://", authority], shell=True)



# subprocess.call("adb shell Content query uri content://{{authority/udetails}}", shell=True)






   





    
  





#find all indices of true values in data3
# def find_true_indices(data3, key):
#     if key in data3:
#         #check if it has the value of true
#         if "true" in data3[key]:
#             #return total number of true values
#             return data3[key].index("true")
#         else:
#             #return 0 if there are no true values
#             return 0    
#     else:
#         return False




# data_check = check_key(data3, key)

# print(data_check)

# data_list = list_keys(data3, key)
# print(data_list)




#print out the 







#             use = format("{}\t:\t{}\n".format(att,perm.attrib[att]))
#             #split the data use  into two rows
#             use = use.split("\t:\t")

#             #convert the list to an array
#             use = np.array(use)

#             #append the data to the data array
#             data.append(use)

 
# data = []
# content_data = []


# for perm in permissions2:
#     for att in perm.attrib:
#         use = format(format(att,perm.attrib[att]))
#         print(use)
#         #split the data use  into two rows
#         use = use.split("\t:\t")

#         #convert the list to an array
#         use = np.array(use)

#         #append the data to the data array
#         data.append(use)


# for perm in permissions3:
#     for att in perm.attrib:
#         # print("{}\t:\t{}\n".format(att, perm.attrib[att]))
#         use = format("{}\t:\t{}\n".format(att,perm.attrib[att]))

#         #split the data use  into two rows
#         use = use.split("\t:\t")

#         #convert the list to an array
#         use = np.array(use)
#         # print(use)

#         #append the data to the data array
#         data.append(use)



# df = pd.DataFrame(data)
# df.columns = ['Attribute', 'Permission']
# #color the column headers
# df.style.applymap(lambda x: 'background-color: lightblue' if x == 'Permission' else 'background-color: lightgreen')

# #remove double quotes from the Permission column
# df['Permission'] = df['Permission'].str.replace('"', '')
# #remove brackets from the Attribute column
# df['Attribute'] = df['Attribute'].str.strip('{}')

# #save the dataframe to a csv file
# df.to_csv(filename, index=False)




# for content in content_provider:
#     con = format(content.attrib)
#     #split the data where there is a comma, into a new row
#     con = con.split(",")
#     #convert the list to an array
#     con = np.array(con)
#     #append the data to the data array
#     content_data.append(con)
    

# df = pd.DataFrame(content_data)

# #column names
# df.columns = ['Authority', 'Content-Provider', 'Value', 'Name', 'Extra-Name', 'Type']
# #remove starting curly brackets from the Authority column
# df['Authority'] = df['Authority'].str.strip('{')
# #remove single quotes from the Authority column
# df['Authority'] = df['Authority'].str.replace("'", "")
# df['Authority'] = df['Authority'].str.replace("{http://schemas.android.com/apk/res/android}authorities:", "")

# #remove curly brackets Permission column
# df['Content-Provider'] = df['Content-Provider'].str.strip('{}')
# #remove single quotes from the Permission column
# df['Content-Provider'] = df['Content-Provider'].str.replace("'", "")
# #remove specific string from the Permission column
# df['Content-Provider'] = df['Content-Provider'].str.replace("{http://schemas.android.com/apk/res/android}", "")

# #remove single quotes from the Value column
# df['Value'] = df['Value'].str.replace("'", "")
# #remove specific string from the Value column
# df['Value'] = df['Value'].str.replace("{http://schemas.android.com/apk/res/android}", "")


# # if single quotes are in the Name column, remove them
# df['Name'] = df['Name'].str.replace("'", "")
# #remove specific string from the Name column
# df['Name'] = df['Name'].str.replace("{http://schemas.android.com/apk/res/android}", "")

# # if single quotes are in the Extra-Name column, remove them
# df['Extra-Name'] = df['Extra-Name'].str.replace("'", "")
# #remove specific string from the Extra-Name column
# df['Extra-Name'] = df['Extra-Name'].str.replace("{http://schemas.android.com/apk/res/android}", "")

# #save the dataframe to a csv file
# df.to_csv(content_filename, index=False)


# #check on the csv file to see if there are any duplicates
# df.duplicated()
# #remove duplicates from the csv file
# df.drop_duplicates(inplace=True)
# #save the dataframe to a csv file
# df.to_csv(content_filename, index=False)



# time.sleep(5)
# #read the content_filename csv file into a dataframe
# df = pd.read_csv(content_filename)
# #create a  test case to check if column Content-Provider  has enabled: true





