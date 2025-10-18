from datetime import datetime

a = {'count 4': '5', '4': 'ADD', 'count 5': '3', '5': 'ADD', 'count 7': '3'}

dict1 = [1,2,3,4,5]
dict2 = [11,22,33,44,55]

a = dict(zip(dict1, dict2))

str = [{'D_ID': 1}, {'D_ID': 2}, {'D_ID': 3}, {'D_ID': 4}, {'D_ID': 5}, {'D_ID': 6}, {'D_ID': 7}]

tit = []

for i in str:
    tit.append(i['D_ID'])

print(datetime.now().date())
