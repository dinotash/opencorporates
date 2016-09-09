import sys
import json

while True:
  line = sys.stdin.readline()
  if not line:
    break
  raw_record = json.loads(line)

  #skip individuals
  if (raw_record['category'] == "Insurance mediation employees"):
    continue

  if ('permissions' in raw_record):
    permissions_list = raw_record['permissions']
  else:
    permissions_list = [{'permission': raw_record['category'], 'country': 'Sweden'}]

  for permission in permissions_list:
    #create a rich licence record with the required
    licence_record = {
      'confidence': 'HIGH',
      'licence_holder': {
        "entity_properties": {
          'name': raw_record['name']
        },
        "entity_type": "unknown"
      },
      'category': ["Financial"],
      'permissions': [
        {
          'activity_name': permission['permission'],
          'permission_type': "operating"
        }
      ],
      'source_url': raw_record['source_url'],
      'sample_date': raw_record['sample_date'],
      'licence_issuer': {
        'jurisdiction': "Sweden",
        'name': raw_record['source_authority']
      }
    }

    #add address if we have it
    if 'address' in raw_record:
      licence_record['licenced_location'] = raw_record['address']
      licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['address']

    if 'telephone' in raw_record:
      licence_record['licence_holder']['entity_properties']['telephone_number'] = raw_record['telephone']

    #keep track of ids
    if 'fi_identification_number' in raw_record:
      licence_record['licence_number'] = raw_record['fi_identification_number']
    if 'corporate_identification_number' in raw_record:
      licence_record['licence_holder']['entity_properties']['company_number'] = raw_record['corporate_identification_number']

    #check what kind of permission we have
    if ('date' in permission):
      licence_record['start_date'] = permission['date']
    if ('country' in permission):
      licence_record['jurisdiction_of_licence'] = permission['country']
    else:
      licence_record['jurisdiction_of_licence'] = "Sweden"

    #output the result
    print json.dumps(licence_record)