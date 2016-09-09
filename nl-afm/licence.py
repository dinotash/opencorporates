# -*- coding: utf-8 -*-

import sys
import json
import datetime

#convert date into iso format
def parse_date(input_string):
	if ("/" in input_string):
		#dd/mm/yyyy format
		date_parts = input_string.split("/")
		output = date_parts[2] + "-" + date_parts[1].zfill(2) + "-" + date_parts[0].zfill(2)
		return output

	else:
		#dd mmm yyyy format
		month_translation = {
			'jan': "01",
			'feb': "02",
			'mrt': "03",
			'apr': "04",
			'mei': "05",
			'jun': "06",
			'jul': "07",
			'aug': "08",
			'sep': "09",
			'oct': "10",
			'okt': "10",
			'nov': "11",
			"dec": "12"
		}
		date_parts = input_string.split(" ")
		output = date_parts[2] + "-" + month_translation[date_parts[1]] + "-" + date_parts[0].zfill(2)
		return output

#load in data
while True:
	line = sys.stdin.readline()
	if not line:
		break
	raw_record = json.loads(line)

	#different transformers depending on category

#******

	#ONE: AUDIT FIRM
	if (raw_record['category'] == "Audit firm"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Audit firm',
				'permission_type': 'operating'
			}]
		}

		#optional extras
		if ('Adres' in raw_record):
			if (len(raw_record['Adres']) > 5):
				licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['Adres']
		if ('Status vergunning' in raw_record):
			licence_record['status'] = raw_record['Status vergunning']
		if ('Datum van de vergunningverlening' in raw_record):
			licence_record['start_date'] = parse_date(raw_record['Datum van de vergunningverlening'])
		if ('Internetadres' in raw_record):
			licence_record['licence_holder']['entity_properties']['website'] = raw_record['Internetadres']

		#officers
		shareholders = []
		auditors = []
		policymakers = []
		if ('Aandeelhouders / Vennoten / Maten' in raw_record):
			for shareholder in raw_record['Aandeelhouders / Vennoten / Maten']:
				officer = {
					'name': shareholder['Naam'],
					'position': 'Shareholder'
				}
				shareholders.append(officer)
			
		if ('Externe accountants (Werkzaam bij accountantsorganisatie)' in raw_record):
			for auditor in raw_record['Externe accountants (Werkzaam bij accountantsorganisatie)']:
				officer = {
					'name': auditor['Naam'],
					'position': 'External auditor (employed by the audit firm)'
				}
				auditors.append(officer)
		if ('Externe accountants (Verbonden aan accountantsorganisatie)' in raw_record):
			for auditor in raw_record['Externe accountants (Verbonden aan accountantsorganisatie)']:
				officer = {
					'name': auditor['Naam'],
					'position': 'External auditor (affiliated to the audit firm)'
				}
				auditors.append(officer)
		if ('Beleidsbepalers en medebeleidsbepalers' in raw_record):
			for policymaker in raw_record['Beleidsbepalers en medebeleidsbepalers']:
				officer = {
					'name': policymaker['Naam'],
					'position': 'Policymaker or co-policymaker'
				}
				policymakers.append(officer)

		#add officers to record
		if (len(shareholders) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['shareholders'] = shareholders
			else:
				licence_record['other_attributes'] = {'shareholders': shareholders}
		if (len(auditors) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['auditors'] = auditors
			else:
				licence_record['other_attributes'] = {'auditors': auditors}
		if (len(policymakers) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['policymakers'] = policymakers
			else:
				licence_record['other_attributes'] = {'policymakers': policymakers}

		#additional permissions
		if ("Wettelijke controles bij OOB’s" in raw_record):
			if (raw_record["Wettelijke controles bij OOB’s"] == "Ja"):
				new_permission = {
					'activity_name': "Statutory audit for public interest entities",
					'permission_type': "operating"
				}
				licence_record['permissions'].append(new_permission)

		print(json.dumps(licence_record))

#******

	#TWO: THIRD COUNTRY AUDIT ENTITIES
	elif (raw_record['category'] == "Third-country audit entity"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Third-country audit entity',
				'permission_type': 'operating'
			}]
		}

		#optional extras
		if ('Vestigingsadres' in raw_record):
			if (len(raw_record['Vestigingsadres']) > 5):
				licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['Vestigingsadres']
		if ('Status registratie' in raw_record):
			licence_record['status'] = raw_record['Status registratie']
		if ('Registratie datum' in raw_record):
			licence_record['start_date'] = parse_date(raw_record['Registratie datum'])

		#officers
		auditors = []
		policymakers = []
		if ('Auditors van een derde land' in raw_record):
			for auditor in raw_record['Auditors van een derde land']:
				officer = {
					'name': auditor['Naam auditor'],
					'position': 'Third-country auditor'
				}
				auditors.append(officer)
		if ('(Mede)beleidsbepalers:' in raw_record):
			for policymaker in raw_record['(Mede)beleidsbepalers:']:
				officer = {
					'name': policymaker['Naam'],
					'position': '(Co-)policymaker'
				}
				policymakers.append(officer)
		if ('(Mede)beleidsbepalers' in raw_record):
			for policymaker in raw_record['(Mede)beleidsbepalers']:
				officer = {
					'name': policymaker['Naam'],
					'position': '(Co-)policymaker'
				}
				policymakers.append(officer)
		
		#add officers
		if (len(auditors) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['auditors'] = auditors
			else:
				licence_record['other_attributes'] = {'auditors': auditors}
		if (len(policymakers) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['policymakers'] = policymakers
			else:
				licence_record['other_attributes'] = {'policymakers': policymakers}
		
		#permissions - first put the Dutch record out, then repeat with each country of licensing
		print(json.dumps(licence_record))

		if ('Inschrijving in de registers van toezichthoudende instanties in staten die geen lidstaat zijn' in raw_record):
			for registration in raw_record['Inschrijving in de registers van toezichthoudende instanties in staten die geen lidstaat zijn']:
				licence_record['licence_issuer']['jurisdiction'] = registration['Land']
				licence_record['licence_issuer']['name'] = registration['Naam toezichthoudende instantie']
				licence_record['jurisdiction_of_licence'] = registration['Land']
				print(json.dumps(licence_record))

		if ('Inschrijving als auditkantoor of auditorganisatie van een derde land in de registers van toezichthoudende instanties in lidstaten' in raw_record):
			for registration in raw_record['Inschrijving als auditkantoor of auditorganisatie van een derde land in de registers van toezichthoudende instanties in lidstaten']:
				licence_record['licence_issuer']['jurisdiction'] = registration['Land']
				licence_record['licence_issuer']['name'] = registration['Naam toezichthoudende instantie']
				licence_record['jurisdiction_of_licence'] = registration['Land']		
				print(json.dumps(licence_record))	

#*****

	#THREE: COLLECTIVE INVESTMENT SCHEME - have only captured this at category level as I'm not sure how to interpret details of permissions
	elif (raw_record['category'] == "Collective investment scheme"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Collective investment scheme',
				'permission_type': 'operating'
			}]
		}

		#optional extras
		if ('Plaats' in raw_record):
			if (len(raw_record['Plaats']) > 5):
				licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['Plaats']
		if ('Handelsnaam' in raw_record):
			if (raw_record['name'] == raw_record['Statutaire naam']):
				if (raw_record['name'] != raw_record['Handelsnaam']):
					trade_name = {
						'company_name': raw_record['Handelsnaam'],
						'type': 'trading'
					}
					licence_record['licence_holder']['entity_properties']['alternative_names'] = [trade_name]

		#tied agents
		tied_agents = []
		if ('Verbonden agenten' in raw_record):
			for agent in raw_record['Verbonden agenten']:
				officer = {
					'name': agent['Naam'],
					'position': 'Tied agent'
				}
				tied_agents.append(officer)
		
		if (len(tied_agents) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['tied_agents'] = tied_agents
			else:
				licence_record['other_attributes'] = {'tied_agents': tied_agents}

		#additional permissions
		if ('Vergunning' in raw_record):
			for application in raw_record['Vergunning']:
				application_string = application['Product'] + " - " + application['Financiele dienst']
				if (len(application_string) > 3):
					new_permission = {
						'activity_name': application_string,
						'permission_type': 'operating'
					}
					licence_record['permissions'].append(new_permission)
		if ('Europees paspoort (inkomend)' in raw_record):
			for service in raw_record['Europees paspoort (inkomend)']:
				service_string = service['Product'] + " - " + service['Financiele dienst']
				if (len(service_string) > 3):
					new_permission = {
						'activity_name': service_string,
						'permission_type': 'operating'
					}
					licence_record['permissions'].append(new_permission)

		print(json.dumps(licence_record))

#******
	
	#FOUR: INVESTMENT FIRM
	elif (raw_record['category'] == "Investment firm"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Investment firm',
				'permission_type': 'operating'
			}]
		}

		if ('Handelsnaam' in raw_record):
			if (raw_record['name'] == raw_record['Statutaire naam']):
				if (raw_record['name'] != raw_record['Handelsnaam']):
					trade_name = {
						'company_name': raw_record['Handelsnaam'],
						'type': 'trading'
					}
					licence_record['licence_holder']['entity_properties']['alternative_names'] = [trade_name]

		#additional permissions
		if ('Europees paspoort (inkomend)' in raw_record):
			for service in raw_record['Europees paspoort (inkomend)']:
				new_permission = {
					'activity_name': 'Europees paspoort (inkomend) - ' + service['Financiele dienst'],
					'permission_type': 'operating'
				}

				#add in date if there is one
				if ('Begindatum huidige matrix' in service):
					start_date = parse_date(service['Begindatum huidige matrix'])
					new_permission['other_attributes'] = {'start_date': start_date}
				if ('Begindatum' in service):
					start_date = parse_date(service['Begindatum'])
					new_permission['other_attributes'] = {'start_date': start_date}

				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)

		if ('EU-passport (incoming) via licenseholder continuation' in raw_record):
			for service in raw_record['EU-passport (incoming) via licenseholder continuation']:
				new_permission = {
					'activity_name': 'EU-passport (incoming) via licenceholder continuation - ' + service['Financiele dienst'],
					'permission_type': 'operating'
				}
				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)

		if ('DNB vergunning / EER Kredietinstelling' in raw_record):
			for service in raw_record['DNB vergunning / EER Kredietinstelling']:
				service_string = 'DNB licence / EER credit institutions and financial institutions - ' + service['Financiele dienst'] + " - " + 'Service / activity'
				if (len(service_string) > 3):
					new_permission = {
						'activity_name': service_string,
						'permission_type': 'operating'
					}
					if (new_permission not in licence_record['permissions']):
						licence_record['permissions'].append(new_permission)

		if ('Vergunning' in raw_record):
			for service in raw_record['Vergunning']:
				service_string = 'Vergunning - ' + service['Financiele dienst'] + " - " + 'Service / activity'
				if (len(service_string) > 3):
					new_permission = {
						'activity_name': service_string,
						'permission_type': 'operating'
					}
					if (new_permission not in licence_record['permissions']):
						licence_record['permissions'].append(new_permission)

		if ('Vrijgestelde beleggingsondernemingen' in raw_record):
			for service in raw_record['Vrijgestelde beleggingsondernemingen']:
				service_string = 'Exempt investment firms - ' + service['Financiele dienst'] + " - " + 'Service / activity'
				if (len(service_string) > 3):
					new_permission = {
						'activity_name': service_string,
						'permission_type': 'operating'
					}

					#add in date if there is one
					if ('Begindatum huidige matrix' in service):
						start_date = parse_date(service['Begindatum huidige matrix'])
						new_permission['other_attributes'] = {'start_date': start_date}
					if ('Begindatum' in service):
						start_date = parse_date(service['Begindatum'])
						new_permission['other_attributes'] = {'start_date': start_date}

					if (new_permission not in licence_record['permissions']):
						licence_record['permissions'].append(new_permission)

		if ('Permissions' in raw_record):
			for permission in raw_record['Permissions']:
				service_string = permission['scope'] + " - " + permission['instrument'] + " - " + permission['service']
				if (len(service_string) > 6):
					new_permission = {
						'activity_name': service_string,
						'permission_type': 'operating'
					}
					if (new_permission not in licence_record['permissions']):
						licence_record['permissions'].append(new_permission)					

		if ('Vergunning (beperkingen)' in raw_record):
			for restriction in raw_record['Vergunning (beperkingen)']:
				new_permission = {
					'activity_name': 'Application (restrictions) - ' + restriction['Beperking'],
					'permission_type': 'operating'
				}
				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)

		#tied agents
		tied_agents = []
		if ('Verbonden agenten' in raw_record):
			for agent in raw_record['Verbonden agenten']:
				officer = {
					'name': agent['Naam'],
					'position': 'Tied agent'
				}
				tied_agents.append(officer)
		if ('Verbonden agenten via' in raw_record):
			for agent in raw_record['Verbonden agenten via']:
				officer = {
					'name': agent['Statutaire naam'],
					'position': 'Hidden agent via'
				}
				tied_agents.append(officer)

		if (len(tied_agents) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['tied_agents'] = tied_agents
			else:
				licence_record['other_attributes'] = {'tied_agents': tied_agents}

		print(json.dumps(licence_record))

#*****

	#FIVE: FINANCIAL SERVICE PROVIDER
	elif(raw_record['category'] == "Financial service provider"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Financial service provider',
				'permission_type': 'operating'
			}]
		}

		#optional properties
		if ('Plaats' in raw_record):
			if (len(raw_record['Plaats']) > 5):
				licence_record['licence_holder']['entity_properties']['mailing_address'] = raw_record['Plaats']
		if ('Handelsnaam' in raw_record):
			if (raw_record['name'] == raw_record['Statutaire naam']):
				if (raw_record['name'] != raw_record['Handelsnaam']):
					trade_name = {
						'company_name': raw_record['Handelsnaam'],
						'type': 'trading'
					}
					licence_record['licence_holder']['entity_properties']['alternative_names'] = [trade_name]

		#officers
		affiliated_institutions = []
		associated_mediators = []
		warrantors = []
		policymakers = []

		if ('Aangesloten instellingen via' in raw_record):
			for institution in raw_record['Aangesloten instellingen via']:
				officer = {
					'name': institution['Statutaire naam'],
					'position': 'Affiliated institution via'
				}
				affiliated_institutions.append(officer)
		if ('Aangesloten instellingen' in raw_record):
			for institution in raw_record['Aangesloten instellingen']:
				officer = {
					'name': institution['Statutaire naam'],
					'position': 'Affiliated institution'
				}
				affiliated_institutions.append(officer)
		if ('Verbonden bemiddelaars via' in raw_record):
			for mediator in raw_record['Verbonden bemiddelaars via']:
				officer = {
					'name': mediator['Statutaire naam'],
					'position': 'Associated mediator via'
				}
				associated_mediators.append(officer)
		if ('Verbonden bemiddelaars' in raw_record):
			for mediator in raw_record['Verbonden bemiddelaars']:
				officer = {
					'name': mediator['Statutaire naam'],
					'position': 'Associated mediator'
				}
				associated_mediators.append(officer)
		if ('Warrantors' in raw_record):
			for warrantor in raw_record['Warrantors']:
				officer = {
					'name': warrantor['Statutaire naam'],
					'position': 'Warrantor'
				}
				warrantors.append(officer)
		if ('Warrantors via' in raw_record):
			for warrantor in raw_record['Warrantors via']:
				officer = {
					'name': warrantor['Statutaire naam'],
					'position': 'Warrantor via'
				}
				warrantors.append(officer)
		if ('Beleidsbepalers' in raw_record):
			for policymaker in raw_record['Beleidsbepalers']:
				officer = {
					'name': policymaker['Naam'],
					'position': 'Policymaker'
				}
				policymakers.append(officer)

		if (len(affiliated_institutions) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['affiliated_institutions'] = affiliated_institutions
			else:
				licence_record['other_attributes'] = {'affiliated_institutions': affiliated_institutions}
		if (len(associated_mediators) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['associated_mediators'] = associated_mediators
			else:
				licence_record['other_attributes'] = {'associated_mediators': associated_mediators}
		if (len(warrantors) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['warrantors'] = warrantors
			else:
				licence_record['other_attributes'] = {'warrantors': warrantors}
		if (len(policymakers) > 0):
			if ('other_attributes' in licence_record):
				licence_record['other_attributes']['policymakers'] = policymakers
			else:
				licence_record['other_attributes'] = {'policymakers': policymakers}

		#permissions
		if ('Europees paspoort (inkomend)' in raw_record):
			for permission in raw_record['Europees paspoort (inkomend)']:
				permission_string = 'EU-passport (incoming) - '
				if (('Product' in permission) and ('Financiele dienst' in permission)):
					permission_string = 'EU-passport (incoming) - ' + permission['Product'] + ' - ' + permission['Financiele dienst']
				elif ('Product' in permission):
					permission_string = 'EU-passport (incoming) - ' + permission['Product']
				elif ('Financiele dienst' in permission):
					permission_string = 'EU-passport (incoming) - ' + permission['Financiele dienst']
				else:
					continue

				new_permission = {
					'activity_name': permission_string,
					'permission_type': 'operating'
				}
				#add in date if there is one
				if ('Begindatum huidige matrix' in permission):
					start_date = parse_date(permission['Begindatum huidige matrix'])
					new_permission['other_attributes'] = {'start_date': start_date}
				if ('Begindatum' in permission):
					start_date = parse_date(permission['Begindatum'])
					new_permission['other_attributes'] = {'start_date': start_date}

				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)
		if ('Applications' in raw_record):
			for permission in raw_record['Applications']:
				permission_string = 'Application - '
				if (('Product' in permission) and ('Financiele dienst' in permission)):
					permission_string = 'Application - ' + permission['Product'] + ' - ' + permission['Financiele dienst']
				elif ('Product' in permission):
					permission_string = 'Application - ' + permission['Product']
				elif ('Financiele dienst' in permission):
					permission_string = 'Application - ' + permission['Financiele dienst']
				else:
					continue

				new_permission = {
					'activity_name': permission_string,
					'permission_type': 'operating'
				}
				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)
		if ('Vergunningen adviseren' in raw_record):
			for permission in raw_record['Vergunningen adviseren']:
				permission_string = 'Advice permits - '
				if (('Product' in permission) and ('Financiele dienst' in permission)):
					permission_string = 'Advice permit - ' + permission['Product'] + ' - ' + permission['Financiele dienst']
				elif ('Product' in permission):
					permission_string = 'Advice permit - ' + permission['Product']
				elif ('Financiele dienst' in permission):
					permission_string = 'Advice permit - ' + permission['Financial service']
				else:
					continue

				new_permission = {
					'activity_name': permission_string,
					'permission_type': 'operating'
				}
				#add in date if there is one
				if ('Begindatum huidige matrix' in permission):
					start_date = parse_date(permission['Begindatum huidige matrix'])
					new_permission['other_attributes'] = {'start_date': start_date}
				if ('Begindatum' in permission):
					start_date = parse_date(permission['Begindatum'])
					new_permission['other_attributes'] = {'start_date': start_date}

				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)
		if ('Europees paspoort (uitgaand)' in raw_record):
			for permission in raw_record['Europees paspoort (uitgaand)']:
				permission_string = 'EU-passport (outgoing) - '
				if (('Product' in permission) and ('Financiele dienst' in permission)):
					permission_string = 'EU-passport (outgoing) - ' + permission['Product'] + ' - ' + permission['Financiele dienst']
				elif ('Product' in permission):
					permission_string = 'EU-passport (outgoing) - ' + permission['Product']
				elif ('Financiele dienst' in permission):
					permission_string = 'EU-passport (outgoing) - ' + permission['Financiele dienst']
				else:
					continue
				new_permission = {
					'activity_name': permission_string,
					'permission_type': 'operating'
				}
				if (new_permission not in licence_record['permissions']):
					licence_record['permissions'].append(new_permission)
			
		print(json.dumps(licence_record))

#*****

	#SIX: CLEARING AND SETTLEMENT
	elif (raw_record['category'] == "Clearing and settlement"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country'],
					'alternative_names': [{
						'company_name': raw_record['Handelsnaam'],
						'type': 'trading'
					}]
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': "Netherlands",
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Clearing and settlement',
				'permission_type': 'operating'
			},
			{
				'activity_name': raw_record['Activiteit'],
				'permission_type': 'operating'
			}]
		}

		print(json.dumps(licence_record))

#******

	#SEVEN: TRADING PLATFORMS
	elif(raw_record['category'] == "Trading platform"):
		#basic details
		try:
			licence_record = {
				'confidence': 'HIGH',
				'licence_holder': {
					'entity_properties': {
						'name': raw_record['name'],
						'jurisdiction': raw_record['country'],
						'alternative_names': [{
							'company_name': raw_record['Handelsnaam'],
							'type': 'trading'
						}]
					},
					'entity_type': "unknown"
				},
				'category': ['Financial'],
				'source_url': raw_record['source_url'],
				'sample_date': raw_record['sample_date'],
				'jurisdiction_of_licence': 'Netherlands',
				'licence_number': raw_record['licence_number'],
				'licence_issuer': {
					'jurisdiction': "Netherlands",
					'name': raw_record['source']
				},
				'permissions': [{
					'activity_name': 'Trading platform',
					'permission_type': 'operating'
				},
				{
					'activity_name': raw_record['permission'],
					'permission_type': 'operating'
				}]
			}

			print(json.dumps(licence_record))
		except:
			pass

#*******

	#EIGHT: Ontheffingen opvorderbaar geld
	elif (raw_record['category'] == "Ontheffingen opvorderbaar geld"):
		#basic details
		licence_record = {
			'confidence': 'HIGH',
			'licence_holder': {
				'entity_properties': {
					'name': raw_record['name'],
					'jurisdiction': raw_record['country']
				},
				'entity_type': "unknown"
			},
			'category': ['Financial'],
			'source_url': raw_record['source_url'],
			'sample_date': raw_record['sample_date'],
			'jurisdiction_of_licence': 'Netherlands',
			'licence_number': raw_record['licence_number'],
			'licence_issuer': {
				'jurisdiction': 'Netherlands',
				'name': raw_record['source']
			},
			'permissions': [{
				'activity_name': 'Ontheffingen opvorderbaar geld',
				'permission_type': 'operating'
			}]
		}

		#optional properties
		if ('Handelsnaam' in raw_record):
			if (raw_record['name'] == raw_record['Statutaire naam']):
				if (raw_record['name'] != raw_record['Handelsnaam']):
					trade_name = {
						'company_name': raw_record['Handelsnaam'],
						'type': 'trading'
					}
					licence_record['licence_holder']['entity_properties']['alternative_names'] = [trade_name]

		if ('Ontheffing bemiddelen' in raw_record):
			for exemption in raw_record['Ontheffing bemiddelen']:
				new_permission = {
					'activity_name': exemption['Product'] + " - " + exemption['Financiele Dienst'],
					'permission_type': 'operating'
				}
				licence_record['permissions'].append(new_permission)

		if ('Ontheffing bemiddelen beperkingen' in raw_record):
			for exemption in raw_record['Ontheffing bemiddelen beperkingen']:
				new_permission = {
					'activity_name': exemption['Beperking'],
					'permission_type': 'operating'
				}
				licence_record['permissions'].append(new_permission)

		print(json.dumps(licence_record))