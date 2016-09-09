# -*- coding: utf-8 -*-

import sys
import json
import datetime

#load in data
while True:
	line = sys.stdin.readline()
	if not line:
		break
	raw_record = json.loads(line)

	#basic details
	licence_record = {
		'confidence': 'HIGH',
		'licence_holder': {
			'entity_properties': {
				'name': raw_record['name']
			},
			'entity_type': "unknown"
		},
		'category': ['Financial'],
		'source_url': raw_record['source_url'],
		'sample_date': raw_record['sample_date'],
		'jurisdiction_of_licence': 'Cyprus',
		'licence_issuer': {
			'jurisdiction': "Cyprus",
			'name': "Cyprus Securities and Exchange Commission"
		},
		'permissions': [{
			'activity_name': raw_record['category'],
			'permission_type': 'operating'
		}]
	}

	#optionals
	if (u'Company Registration Number' in raw_record):
		licence_record['licence_holder']['entity_properties']['company_number'] = raw_record[u'Company Registration Number']
	if (u'Licence Date' in raw_record):
		licence_record['start_date'] = raw_record[u'Licence Date']
	if (u'Web Site' in raw_record):
		licence_record['licence_holder']['entity_properties']['website'] = raw_record['Web Site']
	if (u'Telephone' in raw_record):
		licence_record['licence_holder']['entity_properties']['telephone'] = raw_record['Telephone']
	if (u'Country' in raw_record):
		licence_record['licence_holder']['entity_properties']['jurisdiction'] = raw_record['Country']
	if (u'Competent Authority' in raw_record):
		licence_record['licence_issuer']['name'] = raw_record['Competent Authority']
	if (u'Date of Termination' in raw_record):
		licence_record['end_date'] = raw_record[u'Date of Termination']
	if (u'Licence Number' in raw_record):
		licence_record['licence_number'] = raw_record['Licence Number']
	if (u'Scope Of Authorization' in raw_record):
		new_permission = {
			'activity_name': raw_record[u'Scope Of Authorization'],
			'permission_type': 'operating'
		}
		licence_record['permissions'].append(new_permission)
	if (u'Administrative Services' in raw_record):
		new_permission = {
			'activity_name': raw_record[u'Administrative Services'],
			'permission_type': 'operating'
		}
		licence_record['permissions'].append(new_permission)

	print(json.dumps(licence_record))