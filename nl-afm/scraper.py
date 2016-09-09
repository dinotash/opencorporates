# -*- coding: utf-8 -*-

import json
import datetime
from datetime import date
import turbotlib
from bs4 import BeautifulSoup
import bs4
import requests

#SOURCES
base_url = "http://www.afm.nl"

source_name = "Netherlands Authority for the Financial Markets (AFM)"

sources = [
	{'category': 'Audit firm', 'url': 'http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7BB5D6C574-90DE-4E1C-A997-5D84E5086C6B%7D&amp;perpage=1000000'},
	{'category': 'Third-country audit entity', 'url': 'http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7B5F004334-7EE7-4381-8D7D-E3EC499BB639%7D&amp;perpage=1000000'},
	{'category': 'Collective investment scheme', 'url': 'http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7B883BCFF1-0F26-442F-9FAF-A39FF911B109%7D&amp;perpage=1000000'},
	{'category': 'Investment firm', 'url': 'http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7B8F59ACF7-047B-4009-9FA7-90A264E6F3EF%7D&amp;perpage=1000000'},
	{'category': 'Financial service provider', 'url': 'http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7B04EFAD81-E254-40FA-8728-94D90447AD4B%7D&amp;perpage=1000000'},
	{'category': 'Clearing and settlement', 'url': "http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type={EAEB6389-443A-4808-A8B0-F0AE1C3DF3F8}"},
	{'category': 'Trading platform', 'url': "http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type={15F11EE8-8B22-4B9E-9480-C01BFB194E2C}"},
	{'category': 'Ontheffingen opvorderbaar geld', 'url': "http://www.afm.nl/nl/professionals/registers/alle-huidige-registers.aspx?type=%7BBC9EB444-7146-4FF9-81B3-59B726DC938D%7D&amp;perpage=1000000"}
]

#used to decode investment firm permissions
permissions = {
	'A1': 'Het ontvangen en doorgeven van orders met betrekking tot één of meer financiële instrumenten.',
	'A2': 'Het uitvoeren van orders voor rekening van cliënten.',
	'A3': 'Het handelen voor eigen rekening.',
	'A4': 'Vermogensbeheer.',
	'A5': 'Beleggingsadvies.',
	'A6': 'Het overnemen van financiële instrumenten en/of plaatsen van financiële instrumenten met plaatsingsgarantie.',
	'A7': 'Het plaatsen van financiële instrumenten zonder plaatsingsgarantie.',
	'A8': 'Het exploiteren van multilaterale handelsfaciliteiten.',
	'B1': "Bewaring en beheer van financiële instrumenten voor rekening van cliënten, met in'Valutawisseldiensten voorzover deze samenhangen met het verrichten van beleggingsdiensten.',begrip van bewaarneming en daarmee samenhangende diensten zoals contanten- en/of zekerhedenbeheer.",
	'B2': 'Het verstrekken van kredieten of leningen aan een belegger om deze in staat te stellen een transactie in één of meer financiële instrumenten te verrichten, bij welke transactie de onderneming die het krediet of de lening verstrekt, als partij optreedt.',
	'B3': 'Advisering aan ondernemingen inzake kapitaalstructuur, bedrijfsstrategie en daarmee samenhangende aangelegenheden, alsmede advisering en dienstverrichting op het gebied van fusies en overnames van ondernemingen.',
	'B4': 'Valutawisseldiensten voorzover deze samenhangen met het verrichten van beleggingsdiensten.',
	'B5': 'Onderzoek op beleggingsgebied en financiële analyse of andere vormen van algemene aanbevelingen in verband met transacties in financiële instrumenten.',
	'B6': 'Diensten in verband met het overnemen van financiële instrumenten.',
	'B7': 'Beleggingsdiensten en -activiteiten alsmede nevendiensten van het type vermeld in deel A of B van bijlage I die verband houden met de onderliggende waarde van de derivaten, als bedoeld in de punten 5, 6, 7 en 9 van deel C, voorzover deze in verband staan met de verlening van beleggings- of nevendiensten.',
	'C1': 'Effecten.',
	'C2': 'Geldmarktinstrumenten',
	'C3': 'Rechten van deelneming in instellingen voor collectieve belegging.',
	'C4': "Opties, futures, swaps, rentetermijncontracten en andere derivatencontracten die betrekking hebben op effecten, valuta, rentevoeten of rendementen, of andere afgeleide instrumenten, indexen of maatstaven en die kunnen worden afgewikkeld door middel van materiële aflevering of in contanten.",
	'C5': 'Opties, futures, swaps, rentetermijncontracten en andere derivatencontracten die betrekking hebben op grondstoffen en in contanten moeten of mogen worden afgewikkeld naar keuze van een van de partijen (tenzij de reden het in gebreke blijven is of een andere gebeurtenis die beëindiging van het contract tot gevolg heeft).',
	'C6': 'Opties, futures, swaps en andere derivatencontracten die betrekking hebben op grondstoffen en alleen kunnen worden afgewikkeld door middel van materiële levering, mits zij worden verhandeld op een gereglementeerde markt en/of een MTF.',
	'C7': 'Andere, niet in deel C, punt 6 vermelde opties, futures, swaps, termijncontracten en andere derivatencontracten die betrekking hebben op grondstoffen, kunnen worden afgewikkeld door middel van materiële levering en niet voor commerciële doeleinden bestemd zijn, en die de kenmerken van andere afgeleide financiële instrumenten hebben, waarbij o.a. in aanmerking wordt genomen of de clearing en afwikkeling via erkende clearinghouses geschiedt en of er regelmatig sprake is van "margin calls" (verzoek om storting van extra zekerheden).',
	'C8': 'Afgeleide instrumenten voor de overdracht van het kredietrisico.',
	'C9': 'Financiële contracten ter verrekening van verschillen ("contracts for differences").',
	'C10': 'Opties, futures, swaps, termijncontracten en andere derivatencontracten met betrekking tot klimaatvariabelen, vrachttarieven, emissievergunningen, inflatiepercentages of andere officiële economische statistieken, en die contant moeten, of, op verzoek van één der partijen, kunnen worden afgewikkeld (anderszins dan op grond van een verzuim of een ander ontbindend element), alsmede andere derivatencontracten met betrekking tot activa, rechten, verbintenissen, indices en maatregelen dan die vermeld in Deel C en die de kenmerken van andere afgeleide financiële instrumenten bezitten, waarbij o.a. in aanmerking wordt genomen of zij op een gereguleerde markt of MTF worden verhandeld of via erkende clearinghouses, en tevens of er regelmatig sprake is van "margin calls" (verzoek om storting van extra zekerheden).'
}

#FUNCTIONS
#retrieve a document at a given URL as parsed html tree
def get_doc(source_url):
	response = requests.get(source_url)
	html = response.content
	doc = BeautifulSoup(html)
	return doc

def parse_text(string):
	string = string.replace("\n", "")
	string = string.replace("\t", "")
	string = string.replace(u"\u00a0", " ")
	string = string.replace(u"\u2013", "-")
	while "  " in string:
		string = string.replace("  ", " ")
	string = string.strip()
	return string

#get going
sample_date = str(date.today())
turbotlib.log("Starting run on " + sample_date) # Optional debug logging
entity_count = 1

for source in sources:
	#Load the index page
	log_string = unicode("Loading category " + source['category'])
	turbotlib.log(log_string.encode('utf-8'))
	category_page = get_doc(source['url'])

	#Main categories have similar index pages
	if (source['category'] in ['Audit firm', 'Third-country audit entity', 'Collective investment scheme', 'Investment firm', 'Financial service provider', 'Ontheffingen opvorderbaar geld']):
		category_table = category_page.find("table", attrs={"cellspacing": "0", "cellpadding": "0"})
		category_rows = category_table.find_all("tr")

		#go through the rows to find the link for each entity
		for category_row in category_rows[1:]:
			category_cells = category_row.find_all("td")
			entity_name = parse_text(category_cells[0].text)
			entity_url = base_url + category_cells[0].a['href'].replace("&perpage=1000000", "")
			log_string = unicode("Loading entity " + unicode(entity_count) + " - " + entity_name)
			turbotlib.log(log_string.encode('utf-8'))
			try:
				entity_page = get_doc(entity_url)

				#placeholder output
				output = {
					'sample_date': sample_date,
					'source_url': entity_url,
					'source': source_name,
					'category': source['category']
				}
				if (source['category'] == "Third-country audit entity"):
					output['country'] = parse_text(category_cells[2].text)
				added_info = False

				#first table - basic details
				overall_table = entity_page.find("table", attrs={"class": "register_details"})
				overall_rows = overall_table.find_all("tr")
				#can have more than one label/value pair per row
				for overall_row in overall_rows:
					overall_ths = overall_row.find_all("th")
					overall_tds = overall_row.find_all("td")

					for overall_th in overall_ths:
						overall_th_index = overall_ths.index(overall_th)
						label = parse_text(overall_th.text.replace(":", ""))
						if (label == "Land"):
							label = "country"
						
						#addresses are complex - need to deal with line breaks
						if (label == "Contactgegevens"):
							address_lines = overall_tds[overall_th_index].contents
							value = ""
							for line in address_lines:
								try:
									if (str(line) == "<br/>"):
										value += ", "
									else:
										value += (" " + line.replace("\n", ","))
								except:
										value += (" " + line.replace("\n", ","))
							value = parse_text(value)

						#not an address, normal pair
						else:
							value = parse_text(overall_tds[overall_th_index].text)

						if ((len(label) > 0) and (len(value) > 0)):
							output[label] = value
							added_info = True

				#get other tables - ignore the first, as it will be the overall table
				entity_table_list = entity_page.find_all("table")
				for entity_table in entity_table_list[1:]:
					#special format register of investment firm permissions
					if (entity_table.attrs['class'] == ['register_details', 'matrix']):
						subtable = []
						entity_table_rows = entity_table.find_all("tr")
						permission_scope = ""

						#only look at the meat of the table - look for where there is an "x"
						permission_rows = entity_table_rows[2:]
						row_index = 0
						for permission_row in permission_rows:
							#check to see if this is resetting 
							row_ths = permission_row.find_all("th")
							if (len(row_ths) > 0):
								permission_scope = parse_text(row_ths[0].text)
								row_index = 0

							entity_table_cols = permission_row.find_all("td")
							column_index = 0
							for permission_col in entity_table_cols:
								#look for an x
								if (parse_text(permission_col.text) == "x"):
									permission_item = {
										'scope': permission_scope
									}

									#translate column into a service permission
									if (column_index <= 8):
										service_permission = "A" + str(column_index)
									else:
										service_permission = "B" + str(column_index - 8)
									permission_item['service'] = permissions[service_permission]
									permission_item['service_code'] = service_permission

									#translate row into an instrument permission
									instrument_permission = "C" + str(row_index)
									permission_item['instrument'] = permissions[instrument_permission]
									permission_item['instrument_code'] = instrument_permission

									subtable.append(permission_item)

								column_index += 1
							row_index += 1

						#add to output only if we found something
						if (len(subtable) > 0):
							output['Permissions'] = subtable
							added_info = True


					#normal tables are much easier
					else:
						#format A: have a <thead> where first row is title and second row is headers
						if (entity_table.find("thead") is not None):
							thead_rows = len(entity_table.find("thead").find_all("tr"))
							entity_table_rows = entity_table.find_all("tr")
							#only one header row
							if (thead_rows == 1):
								entity_table_title = "Advice permits"

							#more than one table header row - title in the first
							else:
								entity_table_title = parse_text(entity_table_rows[0].text)
								if (entity_table_title[-1] == ":"):
									entity_table_title = entity_table_title[:-1]
								
							#tell it where the content is
							header_row = entity_table_rows[thead_rows - 1]
							content_rows = entity_table_rows[thead_rows:]

						#format B: have no <thead>, and one row with headers. Table title in an h3 before it
						else:
							#get the title first
							entity_table_title_h3 = entity_table.find_previous("h3")
							entity_table_title = parse_text(entity_table_title_h3.text)
							if (entity_table_title[-1] == ":"):
								entity_table_title = entity_table_title[:-1]
							
							#find the content
							entity_table_rows = entity_table.find_all("tr")
							header_row = entity_table_rows[0]
							content_rows = entity_table_rows[1:]

						#go ahead and parse iff we have set things up correctly
						subtable = []

						#get the headers
						subtable_fields = []
						entity_table_headers = header_row.find_all("th")
						for entity_table_header in entity_table_headers:
							field = parse_text(entity_table_header.text)
							subtable_fields.append(field)

						#get the details
						for entity_row in content_rows:
							subtable_item = {}
							entity_row_cells = entity_row.find_all("td")
							for entity_row_cell in entity_row_cells:
								entity_cell_index = entity_row_cells.index(entity_row_cell)
								label = subtable_fields[entity_cell_index]
								value = parse_text(entity_row_cell.text)

								#add to item if we found info
								if ((len(value) > 0) and (len(label) > 0)):
									subtable_item[label] = value
							
							#slightly odd case: subfunds of a collective investment scheme - only one cell filled in on the row
							if ((source['category'] == "Collective investment scheme") and (len(subtable_item) == 1) and ('Type' in subtable_item)):
								if (subtable_item['Type'] != "Subfondsen"): #ignore the header
									#add the item to the last fund we had (including creating the list if needed)
									last_fund = subtable[-1]
									if (last_fund is not None):
										if ('Subfunds' in last_fund):
											last_fund['Subfunds'].append(subtable_item['Type'])
										else:
											last_fund['Subfunds'] = [subtable_item['Type']]

							#otherwise, add item to table if we found any value pairs
							else:
								if (len(subtable_item) > 0):
									subtable.append(subtable_item)
						
						#add table to output if it contained any items
						if (len(subtable) > 0):
							output[entity_table_title] = subtable
							added_info = True

				#return our output
				if (added_info):
					#ensure we have a consistent identifying field across all records
					if ('name' not in output):
						if ('Naam organisatie' in output):
							output['name'] = output['Naam organisatie']
						elif ('Naam auditorganisatie' in output):
							output['name'] = output['Naam auditorganisatie']
						elif ('Statutaire naam' in output):
							output['name'] = output['Statutaire naam']
						elif ('Handelsnaam' in output):
							output['name'] = output['Handelsnaam']

					if ('licence_number' not in output):
						if ('Vergunningnummer' in output):
							output['licence_number'] = output['Vergunningnummer']
						elif ('Registrationnumber' in output):
							output['licence_number'] = output['Registrationnumber']
						else:
							output['licence_number'] = "Not stated"

					if ('country' not in output):
						#audit firm - dutch
						if (output['category'] == "Audit firm"):
							output['country'] = "Netherlands"
						else:
							output['country'] = "Not stated"

					print(json.dumps(output))

				entity_count += 1
			
			except Exception as detail:
				log_string = unicode("Unable to load entity " + unicode(entity_count) + " - " + entity_name + " - ")
				log_string += unicode(detail)
				turbotlib.log(log_string.encode('utf-8'))

	#one page wonder category
	if (source['category'] == "Clearing and settlement"):
		#one table on the page - parse it and print each row
		register_table = category_page.find("table")
		register_rows = register_table.find_all("tr")
		
		#get headers
		clearing_fields = []
		register_headers = register_rows[0].find_all("td")
		for register_header in register_headers:
			clearing_field = parse_text(register_header.text)
			clearing_fields.append(clearing_field)

		#get the rows
		for register_row in register_rows[1:]:
			#placeholder for output
			output = {
				'sample_date': sample_date,
				'source': source_name,
				'source_url': source['url'],
				'category': source['category'],
				'licence_number': "Not stated"
			}
			added_info = False

			#go through cells and add info
			register_cells = register_row.find_all("td")
			column_index = 0
			for register_cell in register_cells:
				label = clearing_fields[column_index]
				value = parse_text(register_cell.text)
				if ((len(label) > 0) and (len(value) > 0)):
					output[label] = value
					added_info = True
				column_index += 1

			#return output
			if (added_info):
				#ensure consistency across all records
				if ('name' not in output):
					output['name'] = output['Instelling']
				if ('country' not in output):
					output['country'] = output['Land van vestiging']

				print(json.dumps(output))

	#three slightly different tables on the same page
	if (source['category'] == "Trading platform"):
		#treat each table in turn
		platform_table_list = category_page.find_all("table")
		platform_permissions = ["Regulated market (trading venues)", "Regulated market", "Multilateral trading facility"]
		for platform_table in platform_table_list:
			platform_rows = platform_table.find_all("tr")

			#first get the relevant permissions based on how which number table this is
			platform_index = platform_table_list.index(platform_table)
			platform_permission = platform_permissions[platform_index]

			#then get the headers from the first row
			platform_fields = []
			for platform_header in platform_rows[0].find_all("td"):
				platform_field = parse_text(platform_header.text)
				platform_fields.append(platform_field)

			#extract the data from each row
			for platform_row in platform_rows[1:]:
				#placeholder output
				output = {
					'sample_date': sample_date,
					'source_url': source['url'],
					'category': source['category'],
					'permission': platform_permission,
					'source': source_name,
					'licence_number': "Not stated"
				}
				added_info = False

				#go across the cells
				platform_cells = platform_row.find_all("td")
				column_index = 0
				for platform_cell in platform_cells:
					label = platform_fields[column_index]
					value = parse_text(platform_cell.text)

					if ((len(label) > 0) and (len(value) > 0)):
						output[label] = value
						added_info = True

					column_index += 1

				if (added_info):
					#ensure consistent approach to naming
					if ('name' not in output):
						if ('Houder van vergunning' in output):
							output['name'] = output['Houder van vergunning']
						elif ('Houder van ontheffing' in output):
							output['name'] = output['Houder van ontheffing']
						elif ('Vergunninghouder' in output):
							output['name'] = output['Vergunninghouder']
					if ('country' not in output):
						output['country'] = output['Land van vestiging']

					print(json.dumps(output))