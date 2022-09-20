#Importing the required modules
import requests
import json
import csv

#Base URL
url = "https://intake.steerhealth.io/api/doctor-search"

size = 648
#Payload
payload = json.dumps({
  "name": "",
  "specialty": "",
  "distance": "",
  "location": "",
  "errors": {},
  "organizationId": "aa1f8845b2eb62a957004eb491bb8ba70a",
  "size": size,
  "page": 0
  })
headers = {
  'Content-Type': 'application/json'
  }

#Getting the response
print("Getting Response..")
response = requests.request("POST", url, headers=headers, data=payload)

#Response to Json 
data = json.loads(response.text)

#List of dict of all providers 
providers_list =[]

#Looping through all the items
print("Getting all the providers...")
for i in data['items']:
    #Provider dict
    needed = {}

    needed["Full Name"] = i.get('firstName') +' '+ i.get('lastName')
      
    #Getting the specality
    if len(i.get('specialty')) == 0:
      needed["Speciality"] = ''
      needed["Add Speciality"] = ''
    elif len(i.get('specialty')) == 1:
      needed["Speciality"] = i.get('specialty')[0]
      needed["Add Speciality"] = ''
    else:
      needed["Speciality"] = i.get('specialty')[0]
      needed["Add Speciality"] = i.get('specialty')[1]

    #Getting the addresses
    if len(i['addresses']) == 0:
      needed["Full Address"] =  ''
      needed["Practice"] = ''
      needed["Address"] = ''
      needed["City"] = ''
      needed["State"] = ''
      needed["Zip"] = ''
      needed["Phone"] = ''
    else:
      needed["Full Address"] =  " " if i['addresses'][0]['name'] is None else i['addresses'][0]['name'] + "," + i['addresses'][0]['address']
      needed["Practice"] = i['addresses'][0]['name']
      needed["Address"] = i['addresses'][0]['address']
      needed["City"] = i['addresses'][0]['city']
      needed["State"] = i['addresses'][0]['state']
      needed["Zip"] = i['addresses'][0]['zip'] 
      needed["Phone"] = i['addresses'][0]['phoneNumber']
    
    #Appending the provider dict to the main list  
    providers_list.append(needed)

#Converting the provider list to csv
print("Saving to file all_providers.csv")
keys = providers_list[0].keys()
with open("all_providers.csv", "w") as file:
  csvwriter = csv.DictWriter(file, keys)
  csvwriter.writeheader()
  csvwriter.writerows(providers_list)  
print("Done")
