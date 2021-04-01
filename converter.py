import json 
 
#open the file
with open('all_the_d1_players.json') as f:
  data = json.load(f)
 
#reading file
for emp in data['Player']:
    print(emp)