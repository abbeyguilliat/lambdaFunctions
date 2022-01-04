### PART 1
## read in Detroit Police Reports file using CSVREADER
import csv
from functools import reduce
import json

input_file = csv.DictReader(open('911_Calls_for_Service_(Last_30_Days).csv'))
call_info = []
for row in input_file:
    call_info.append(row)

## use filter w/ lambda to exclude rows that have missing information in the Zip or Neighborhood column
valid_data = list(filter(lambda row: row['neighborhood'] != '' and row['zip_code'] != 0 and row['dispatchtime'] != '' and row['totalresponsetime'] != '' and row['totaltime'] != '', call_info))
    
## use lambda w/ reduce to calculate avg total response, dispatch, and total times
dispatch_list = []
for row in valid_data:
    dispatch_list.append(float(row['dispatchtime']))
total_dispatch = reduce(lambda time1,time2: time1+time2,dispatch_list)
avg_dispatch = total_dispatch / len(dispatch_list)
print('average dispatch time: ' + str(avg_dispatch))

totalresponse_list = []
for row in valid_data:
    totalresponse_list.append(float(row['totalresponsetime']))
total_totalresponse = reduce(lambda time1,time2: time1+time2,totalresponse_list)
avg_totalresponse = total_totalresponse / len(totalresponse_list)
print('average total response time: ' + str(avg_totalresponse))

total_list = []
for row in valid_data:
    total_list.append(float(row['totaltime']))
total_total = reduce(lambda time1,time2: time1+time2,total_list)
avg_total = total_total / len(total_list)
print('average total time: ' + str(avg_total))

### PART 2
## divide the list of dictionaries into smaller lists of dictionaries separated by neighborhood
neighborhood_list = []
for row in valid_data:
    if (row['neighborhood'] not in neighborhood_list) == True:
        neighborhood_list.append(row['neighborhood'])

json_neighborhood_list = []

for neighborhood in neighborhood_list:
    dispatch_list = []
    totalresponse_list = []
    total_list = []
    neighborhood_dict = []
    neighborhood_dict = list(filter(lambda row: row['neighborhood'] == neighborhood, valid_data))
    json_neighborhood_list.append(neighborhood_dict)
    for row in neighborhood_dict:
        dispatch_list.append(float(row['dispatchtime']))
        totalresponse_list.append(float(row['totalresponsetime']))
        total_list.append(float(row['totaltime']))
    total_dispatch = reduce(lambda time1,time2: time1+time2,dispatch_list)
    avg_dispatch = total_dispatch / len(dispatch_list)
    total_totalresponse = reduce(lambda time1,time2: time1+time2,totalresponse_list)
    avg_totalresponse = total_totalresponse / len(totalresponse_list)
    total_total = reduce(lambda time1,time2: time1+time2,total_list)
    avg_total = total_total / len(total_list)
    print("\n" + neighborhood + "\n===============")
    print('average dispatch time: ' + str(avg_dispatch))
    print('average total response time: ' + str(avg_totalresponse))
    print('average total time: ' + str(avg_total))

### PART 3
with open('service_calls_by_neighborhood.txt','w') as outfile:
    json.dump(json_neighborhood_list, outfile, sort_keys = True, indent=4)