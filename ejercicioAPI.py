import requests

response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
dictionary= response.json()

keys_0 = list(dictionary.keys())
values_0 = list(dictionary.values())
keys_1 = list(values_0[0][0].keys())

print(keys_1)

clean=[]
clean = list(filter(lambda x: "Ingredient" in x and (dictionary[keys_0[0]][0][x] and dictionary[keys_0[0]][0][x]!=" "),keys_1))
clean +=  list(filter(lambda x: "Measure" in x and (dictionary[keys_0[0]][0][x] and dictionary[keys_0[0]][0][x]!=" "),keys_1))
clean +=  list(filter(lambda x: "Measure" not in x and "Ingredient" not in x and (dictionary[keys_0[0]][0][x] and dictionary[keys_0[0]][0][x]!=" "),keys_1))
print(clean)

for key in keys_1:
    print(f'{key}: {dictionary[keys_0[0]][0][key]}\n') if key in clean else ...
    