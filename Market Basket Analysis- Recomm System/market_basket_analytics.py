#____________________________________________________________________________________

#- Author name: Saurabh Patil                              
#- Title : Market basket analytics
#- Coding: utf-8 -*-
#- Type: Python source code
# ___________________________________________________________________________________

import requests
import csv

#sorting the data
def sorting_by_items(data,length):
    newList = []
    for x in data:
        if len(x) == length:
            newList.append(x)
    return(newList)

#Recommendation based on search list
def recommendation(data,search_list):
    for x in search_list:
        if set(data).issubset(x):
                recomm = [set(x) - set(data)]
                break
    else:
        recomm = 'None'
    return(recomm)

#Get the training set
url = "http://kevincrook.com/utd/market_basket_training.txt"
req = requests.get(url)
output =  open('market_basket_training.txt', 'wb')
output.write(req.content)
output.close()

#Get the testing set
url1 = "http://kevincrook.com/utd/market_basket_test.txt"
req1 = requests.get(url1)
output1 =  open('market_basket_test.txt', 'wb')
output1.write(req1.content)
output1.close()

row = []
with open('market_basket_training.txt','rt', encoding = 'utf-8') as file:
    reader = csv.reader(file, delimiter = ',')
    for line in reader:
        row.append(line[1:])
uniq_row = [row[0]]

for i in row:
    add = True
    for j in uniq_row:
        if set(i) == set(j):
            add = False
    if (add):
        uniq_row.append(i)
frequency = []
for uniq_record in uniq_row:
    count = 0
    for x in row:
        if set(uniq_record) == set (x):
            count += 1    
    frequency.append([uniq_record,count])    
frequency = sorted(frequency,key = lambda x:x[1],reverse = True)

sortedItems = []
for x in frequency:
    sortedItems.extend(x[:-1])
two_items = sorting_by_items(sortedItems,2)            # Two products per record
three_items = sorting_by_items(sortedItems,3)          # Three products per record
four_items = sorting_by_items(sortedItems,4)           # Four products per record

df_test = []
with open('market_basket_test.txt','rt', encoding = 'utf-8') as file:
    reader = csv.reader(file, delimiter = ',')
    for line in reader:
        df_test.append(line[1:])

#Generate recommandation results
final_recomm = []
for record in df_test:
    data = [i for i in record if ((i != 'P04') and (i != 'P08'))]
    if len(data) == 3:
         result = recommendation(data,four_items)
    elif len(data) == 2:
         result = recommendation(data,three_items)
    elif len(data) == 1:
         result = recommendation(data,two_items)
    final_recomm.append(result)

#Insert the results into Market Basket Recommendatinos text file
index = ["{0:03}".format(i) for i in range(1,101)]
with open('market_basket_recommendations.txt', mode='wt') as output_file: 
        for i in range(0,100):
            if i<99:
                line = str(index[i]) + ',' + str(final_recomm[i][0].pop()) +'\n'
            else:
                line = str(index[i]) + ',' + str(final_recomm[i][0].pop())
            output_file.write(line)
