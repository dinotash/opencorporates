# -*- coding: utf-8 -*-

import sys
import json
import datetime

#overseas categories
overseas_categories = ['Foreign institution providing cross-border services', 'Hungarian representative office of foreign financial institution', 'Hungarian representative office of foreign insurance broker']

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
				'name': raw_record['Name'],
			},
			'entity_type': "unknown"
		},
		'category': ['Financial'],
		'source_url': raw_record['source_url'],
		'sample_date': raw_record['sample_date'],
		'jurisdiction_of_licence': 'Hungary',
		'licence_number': raw_record['Identifier'],
		'licence_issuer': {
			'jurisdiction': "Hungary",
			'name': raw_record['source']
		},
	}

	#status
	if ('Status' in raw_record):
		licence_record['status'] = raw_record['Status']

	#country is hungary, unless we're dealing with overseas categories, in which case it's not easy for the computer to pick out
	jurisdiction = "Hungary"
	for category in raw_record['categories']:
		if (category in overseas_categories):
			jurisdiction = "Unknown"
			break
	licence_record['licence_holder']['entity_properties']['jurisdiction'] = jurisdiction

	#address
	if ('Address' in raw_record):
		licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['Address']

	#website
	if ('Website address' in raw_record):
		if (raw_record['Website address'] != "n.a."):
			licence_record['licence_holder']['entity_properties']['website'] = raw_record['Website address']

	#permissions
	permission_list = []
	category_string = " - ".join(raw_record['categories'])
	category_permission = {
		'activity_name': category_string,
		'permission_type': 'operating'
	}
	permission_list.append(category_permission)
	if ('Activities' in raw_record):
		for activity in raw_record['Activities']:
			if ('Activity name' in activity):
				permission_string = activity['Activity name']
			else:
				permission_string = activity['Activity content']

			if ('Law reference' in activity):
				permission_string += " [" + activity['Law reference'] + "]"

			new_permission = {
				'activity_name': permission_string,
				'permission_type': 'operating'
			}
	if (len(permission_list) > 0):
		licence_record['permissions'] = permission_list

	#officers
	if ('Executive manager' in raw_record):
		officers_list = []
		for officer in raw_record['Executive manager']:
			new_officer = {
				'name': officer['Name'],
				'position': officer['Position name']
			}
			officers_list.append(new_officer)
		if (len(officers_list) > 0):
			licence_record['licence_holder']['entity_properties']['officers'] = officers_list

	#give us some output
	print(json.dumps(licence_record))
