# -*- coding: utf-8 -*-

import json
import datetime
from datetime import date
import turbotlib
from bs4 import BeautifulSoup
import bs4
import requests

#FUNCTIONS
#retrieve a document at a given URL as parsed html tree
def get_doc(source_url):
	response = requests.get(source_url)
	html = response.content
	doc = BeautifulSoup(html)
	return doc

#convert date from dd/mm/yyyy to yyyy-mm-dd
def parse_date(input_date):
	date_parts = input_date.strip().split("/")
	year_part = date_parts[2].strip().zfill(4)
	month_part = date_parts[1].strip().zfill(2)
	day_part = date_parts[0].strip().zfill(2)

	return year_part + "-" + month_part + "-" + day_part


#SOURCES
base_url = "http://www.cysec.gov.cy"
sources = [
	{'type': 'Investment firm (local)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/investment-firms/cypriot/'},
	{'type': 'Investment firm (expired)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/investment-firms/ΠΡΩΗΝ-ΚΕΠΕΥ/'},
	{'type': 'Investment firm (cross-border)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/investment-firms/member-states/Cross-Border/'},
	{'type': 'Investment firm (branch)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/investment-firms/member-states/Branch/'},
	{'type': 'Investment firm (multilateral trading facility)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/investment-firms/member-states/Multilateral-Trading-Facilities/'},
	{'type': 'UCITS firm (local)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/ucits/local-ucits/'},
	{'type': 'UCITS firm', 'url': 'http://www.cysec.gov.cy/en-GB/entities/ucits/list/'},
	{'type': 'Management company (local)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/ucits/cypriot-management-companies/'},
	{'type': 'Management company (cross-border)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/ucits/ΕΤΑΙΡΕΙΕΣ-ΔΙΑΧΕΙΡΗΣΗΣ-ΚΡΑΤΩΝ-ΜΕΛΩΝ/ΔΙΑΣΥΝΟΡΙΑΚΩΣ/'},
	{'type': 'Management company (branch)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/ucits/ΕΤΑΙΡΕΙΕΣ-ΔΙΑΧΕΙΡΗΣΗΣ-ΚΡΑΤΩΝ-ΜΕΛΩΝ/ΜΕ-ΥΠΟΚΑΤΑΣΤΗΜΑ/'},
	{'type': 'AIFM (authorised)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aifm/authorised/'},
	{'type': 'AIFM (registered)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aifm/registered/'},
	{'type': 'AIFM (registered)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aifm/registered/'},
	{'type': 'AIF', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aif/AIF/'},
	{'type': 'AIFLNP', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aif/aiflnp/'},
	{'type': 'EUVECA and EUSEF', 'url': 'http://www.cysec.gov.cy/en-GB/entities/aif/EuVECA-EuSEF/'},
	{'type': 'Regulated market (local)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/regulated-markets/by-cysec/'},
	{'type': 'Regulated market (cross-border)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/regulated-markets/by-other/'},
	{'type': 'Issuer (local)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/issuers/approved-prospectuses/'},
	{'type': 'Issuer (cross-border)', 'url': 'http://www.cysec.gov.cy/en-GB/entities/issuers/prospectuses-notifications/'},
	{'type': 'Administrative services provider', 'url': 'http://www.cysec.gov.cy/en-GB/entities/asp/list/'}
]

#GET GOING
sample_date = str(date.today())
turbotlib.log("Starting run on " + sample_date) # Optional debug logging

#go through each category in turn
source_count = str(len(sources))
for source in sources:
	#monitor progress
	source_index = str(sources.index(source) + 1).zfill(len(source_count))
	turbotlib.log("Loading category " + source_index + "/" + source_count + ": " + source['type'])

	#load the index page
	try:
		index_page = get_doc(source['url'])

		#find the table of entries, and then each entry within it
		index_table = index_page.find("table", id="RegulatedListViewer")
		if (index_table is not None):
			entity_tables = index_table.find_all("table", attrs={"class": "DefaultText", 'cellspacing': 1})
			
			for entity in entity_tables:
				#find the link to the relevant page
				entity_link = entity.find("a", attrs={"class": "RegulatedEntityName"})
				entity_url = base_url + entity_link['href']
				
				# process name to remove leading numeral
				entity_name = entity_link.text.strip()
				entity_name_start = entity_name.find(". ")
				entity_name = entity_name[entity_name_start + 2:].strip()
			
				output = {
					'sample_date': sample_date,
					'source_url': entity_url,
					'category': source['type'],
					'name': entity_name
				}

				#go through remaining rows of the table
				tr_list = entity.find_all("tr", attrs={"class": "DefaultText"})
				for tr in tr_list:
					#deal with where we have two label and value cells on a row
					td_list = tr.find_all("td", attrs={"class": "DefaultText"})
					for td in td_list:
						#total pain in the arse - they've incldued all the possible (but not used values), just marked them as "HideValue" spans/tds. So, need to find just the other bits of the text
						td_text = ""
						for child in td.children:
							add_child = True
							if (isinstance(child, bs4.Tag)):
								if ('class' in child.attrs):
									if ('HideValue' in child.attrs['class']):
										add_child = False
							if (add_child):
								if (isinstance(child, bs4.Tag)):
									child_text = " " + child.text.strip()
								else:
									child_text = " " + child.strip()
								td_text += child_text
								td_text.strip()
						
						#where we have found something, extract the data into a useful format
						if (len(td_text) > 0):
							td_parts = td_text.split(":")
							label = td_parts[0].strip()

							#deal with urls having a colon in them - re-stitch them together
							if (len(td_parts) > 2):
								td_parts[1] = "".join(td_parts[1:])

							value = td_parts[1].strip()
							
							#convert date to useful form
							date_fields = [u'Licence Date', u'Date of Termination']
							if (label in date_fields):
								value = parse_date(value)

							#need to split out any mad excess spaces
							if (label == "Administrative Services"):
								while ("  " in value):
									value = value.replace("  ", " ")

							#need to split two values in the same cell
							if ((label == "Telephone") and ("Fax" in value)):
								value_parts = value.split(", Fax")
								telephone = value_parts[0].strip()
								if (len(telephone) > 0):
									output['Telephone'] = telephone
								fax = value_parts[1].strip()
								if (len(fax) > 0):
									output['Fax'] = fax

							elif ((label == "Licence Number") and ("Licence Date" in value)):
								value_parts = value.split("Licence Date")
								licence_number = value_parts[0].strip()
								if (len(licence_number) > 0):
									output['Licence Number'] = licence_number
								licence_date = value_parts[1].strip()
								if (len(licence_date) > 0):
									output['Licence Date'] = parse_date(licence_date)

							else:
								if ((len(label) > 0) and (len(value) > 0)):
									output[label] = value

				#go back and try to find the licence numbers if not already picked up. It looks like they didn't close all of the necessary <tr> tags on the index pages...
				if ("Licence Number" not in output):
					strong_tag = entity_link.find_next("strong")
					if (strong_tag is not None):
						if (strong_tag.text.strip() == "Licence Number"):
							#find the relevant bit of the licence number, and exclude all the hidden spans
							strong_text = strong_tag.parent.text.strip()
							strong_start = strong_text.find(":") + 1
							strong_end = strong_text.find("\n")
							strong_licence = strong_text[strong_start:strong_end].strip()
							if (len(strong_licence) > 0):
								output['Licence Number'] = strong_licence
				
				#output the overall device
				print(json.dumps(output))
	except:
		pass