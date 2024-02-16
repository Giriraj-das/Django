import csv
import json

# Example for fixture
#
# [
#   {
#     "model": "myapp.person",
#     "pk": 1,
#     "fields": {
#       "first_name": "John",
#       "last_name": "Lennon"
#     }
#   },
#   {
#     "model": "myapp.person",
#     "pk": 2,
#     "fields": {
#       "first_name": "Paul",
#       "last_name": "McCartney"
#     }
#   }
# ]

DATA_ADS = 'data/ads.csv'
JSON_ADS = 'ad.json'

DATA_CAT = 'data/categories.csv'
JSON_CAT = 'category.json'

DATA_LOCATION = 'data/location.csv'
JSON_LOCATION = 'location.json'

DATA_USER = 'data/user.csv'
JSON_USER = 'user.json'


def csv_to_json(csv_file, model_name, json_file):
    result = []
    with open(csv_file, 'r', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            to_add = {'model': model_name}

            if 'Id' in row:
                to_add['pk'] = int(row['Id'])
                del row['Id']
            else:
                to_add['pk'] = int(row['id'])
                del row['id']

            if 'description' in row:
                row['description'] = row['description'].replace('\n', ' ')

            if row.get('name'):
                row['name'] = row['name'].strip()

            if row.get('age'):
                row['age'] = int(row['age'])

            if row.get('price'):
                row['price'] = int(row['price'])

            if row.get('category_id'):
                row['category_id'] = int(row['category_id'])

            if row.get('author_id'):
                row['author_id'] = int(row['author_id'])

            if 'is_published' in row:
                if row['is_published'] == 'FALSE':
                    row['is_published'] = False
                else:
                    row['is_published'] = True

            row.pop('location_id', None)

            to_add['fields'] = row
            result.append(to_add)
    with open(json_file, 'w', encoding='utf-8') as jsf:
        jsf.write(json.dumps(result, ensure_ascii=False))


# csv_to_json(DATA_ADS, "ads.ad", JSON_ADS)
# csv_to_json(DATA_CAT, "ads.category", JSON_CAT)
csv_to_json(DATA_LOCATION, "ads.location", JSON_LOCATION)
# csv_to_json(DATA_USER, "ads.user", JSON_USER)
