# -*- coding: utf-8 -*-

import json
import datetime
from datetime import date
import turbotlib
from bs4 import BeautifulSoup
import bs4
import requests
import math

#SOURCES
sources = [
	{'categories': ['Money market', 'Financial institution', 'Credit institution', 'Cooperative credit institution', 'Savings cooperative'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=127&ktasearch_label=Savings+cooperative&ktasearch_prev_value=-27&pmod=primaryType&n=&st=0&i=&a=1&x=18&y=16&pt_up=1'},
	{'categories': ['Money market', 'Financial institution', 'Credit institution', 'Cooperative credit institution', 'Credit cooperative'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=128&ktasearch_label=Credit+cooperative&ktasearch_prev_value=127&pmod=primaryType&n=&st=0&i=&a=1&x=50&y=21&pt_up=1'},
	{'categories': ['Money market', 'Financial institution', 'Credit institution', 'Bank'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=17&ktasearch_label=Bank&ktasearch_prev_value=128&pmod=primaryType&n=&st=0&i=&a=1&x=44&y=8'},
	{'categories': ['Money market', 'Financial institution', 'Specialised credit institution', 'Mortgage institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=125&ktasearch_label=Mortgage+institution&ktasearch_prev_value=17&pmod=primaryType&n=&st=0&i=&a=1&x=22&y=16&pt_up=1'},
	{'categories': ['Money market', 'Financial institution', 'Specialised credit institution', 'Other specialised credit institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=126&ktasearch_label=Other+spec.+credit+inst.&ktasearch_prev_value=125&pmod=primaryType&n=&st=0&i=&a=1&x=70&y=12'},
	{'categories': ['Money market', 'Financial institution', 'Specialised credit institution', 'Home savings fund'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=124&ktasearch_label=Home+savings+fund&ktasearch_prev_value=126&pmod=primaryType&n=&st=0&i=&a=1&x=40&y=6'},
	{'categories': ['Money market', 'Financial institution', 'Prudent financial enterprise equivalent to credit institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=83&ktasearch_label=Prudent+financial+enterprise+equ.+to+credit+inst.&ktasearch_prev_value=124&pmod=primaryType&n=&st=0&i=&a=1&x=17&y=12'},
	{'categories': ['Money market', 'Financial enterprise', 'Financial enterprise'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=129&ktasearch_label=Financial+enterprise&ktasearch_prev_value=83&pmod=primaryType&n=&st=0&i=&a=1&x=52&y=18'},
	{'categories': ['Money market', 'Non-financial institution', 'Independent money market broker', 'Multiple agent (D)', 'Not fee paying multiple agent (comm.credit)'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=97&ktasearch_label=Not+fee+paying+multiple+agent+%28comm.credit%29&ktasearch_prev_value=129&pmod=primaryType&n=&st=0&i=&a=1&x=82&y=7&pt_up=1'},
	{'categories': ['Money market', 'Non-financial institution', 'Independent money market broker', 'Multiple agent (D)', 'Fee paying multiple agent'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=96&ktasearch_label=Fee+paying+multiple+agent&ktasearch_prev_value=97&pmod=primaryType&n=&st=0&i=&a=1&x=42&y=17&pt_up=1'},
	{'categories': ['Money market', 'Non-financial institution', 'Independent money market broker', 'Broker'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=98&ktasearch_label=Broker&ktasearch_prev_value=96&pmod=primaryType&n=&st=0&i=&a=1&x=14&y=15&pt_up=1'},
	{'categories': ['Money market', 'Non-financial institution', 'Independent money market broker', 'Multiple main agent (D)'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=95&ktasearch_label=Multiple+main+agent+%28D%29&ktasearch_prev_value=98&pmod=primaryType&n=&st=0&i=&a=1&x=23&y=3'},
	{'categories': ['Money market', 'Non-financial institution', 'Electronic money issuer institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=113&ktasearch_label=Electronic+money+issuer+institution&ktasearch_prev_value=95&pmod=primaryType&n=&st=0&i=&a=1&x=14&y=0'},
	{'categories': ['Money market', 'Non-financial institution', 'Cash processing firm'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=27&ktasearch_label=Cash+processing+firm&ktasearch_prev_value=113&pmod=primaryType&n=&st=0&i=&a=1&x=30&y=16'},
	{'categories': ['Money market', 'Non-financial institution', 'Main agents'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=99&ktasearch_label=Main+agents&ktasearch_prev_value=27&pmod=primaryType&n=&st=0&i=&a=1&x=26&y=2'},
	{'categories': ['Money market', 'Non-financial institution', 'Issuer of credit tokens'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=131&ktasearch_label=Issuer+of+credit+tokens&ktasearch_prev_value=99&pmod=primaryType&n=&st=0&i=&a=1&x=21&y=6&pt_up=1'},
	{'categories': ['Money market', 'Non-financial institution', 'Payment institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=93&ktasearch_label=Payment+institution&ktasearch_prev_value=131&pmod=primaryType&n=&st=0&i=&a=1&x=16&y=19'},
	{'categories': ['Capital market', 'Investment firm'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=112&ktasearch_label=Investment+firm&ktasearch_prev_value=93&pmod=primaryType&n=&st=0&i=&a=1&x=80&y=6'},
	{'categories': ['Capital market', 'Central repository'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=111&ktasearch_label=Central+repository&ktasearch_prev_value=112&pmod=primaryType&n=&st=0&i=&a=1&x=58&y=13&pt_up=1'},
	{'categories': ['Capital market', 'Intermediary According to Batv.'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=122&ktasearch_label=Intermediary+According+to+Batv.&ktasearch_prev_value=111&pmod=primaryType&n=&st=0&i=&a=1&x=65&y=11'},
	{'categories': ['Capital market', 'Stock exchange'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=6&ktasearch_label=Stock+exchange&ktasearch_prev_value=122&pmod=primaryType&n=&st=0&i=&a=1&x=42&y=12&pt_up=1'},
	{'categories': ['Capital market', 'Commodity dealer service provider'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=4&ktasearch_label=Commodity+dealer+service+provider&ktasearch_prev_value=6&pmod=primaryType&n=&st=0&i=&a=1&x=57&y=15'},
	{'categories': ['Captial market', 'Trust'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=132&ktasearch_label=Trust&ktasearch_prev_value=4&pmod=primaryType&n=&st=0&i=&a=1&x=44&y=15'},
	{'categories': ['Capital market', 'Clearing house'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=14&ktasearch_label=Clearing+house&ktasearch_prev_value=132&pmod=primaryType&n=&st=0&i=&a=1&x=24&y=7'},
	{'categories': ['Capital market', 'Central counterparty'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=92&ktasearch_label=Central+counterparty&ktasearch_prev_value=14&pmod=primaryType&n=&st=0&i=&a=1&x=43&y=10'},
	{'categories': ['Capital market', 'Tied agent'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=91&ktasearch_label=Tied+agent&ktasearch_prev_value=92&pmod=primaryType&n=&st=0&i=&a=1&x=52&y=16'},
	{'categories': ['Capital market', 'Fund manager', 'Investment fund manager'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=9&ktasearch_label=Investment+fund+manager&ktasearch_prev_value=91&pmod=primaryType&n=&st=0&i=&a=1&x=63&y=17&pt_up=1'},
	{'categories': ['Capital market', 'Fund manager', 'AIFM'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=135&ktasearch_label=AIFM&ktasearch_prev_value=9&pmod=primaryType&n=&st=0&i=&a=1&x=24&y=16'},
	{'categories': ['Capital market', 'Fund manager', 'UCITS'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=136&ktasearch_label=UCITS&ktasearch_prev_value=135&pmod=primaryType&n=&st=0&i=&a=1&x=46&y=23&pt_up=1'},
	{'categories': ['Capital market', 'Fund manager', 'Venture capital fund manager'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=10&ktasearch_label=Venture+capital+fund+manager&ktasearch_prev_value=136&pmod=primaryType&n=&st=0&i=&a=1&x=34&y=18'},
	{'categories': ['Insurance market', 'Interest representation organisation'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=79&ktasearch_label=Interest+representation+org.&ktasearch_prev_value=10&pmod=primaryType&n=&st=0&i=&a=1&x=38&y=0'},
	{'categories': ['Insurance market', 'Insurance institution', 'Branch insurer'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=114&ktasearch_label=Branch+insurer&ktasearch_prev_value=79&pmod=primaryType&n=&st=0&i=&a=1&x=45&y=17'},
	{'categories': ['Insurance market', 'Insurance institution', 'Insurance association'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=33&ktasearch_label=Insurance+association&ktasearch_prev_value=114&pmod=primaryType&n=&st=0&i=&a=1&x=54&y=11&pt_up=1'},
	{'categories': ['Insurance market', 'Insurance institution', 'Insurance company'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=31&ktasearch_label=Insurance+company&ktasearch_prev_value=33&pmod=primaryType&n=&st=0&i=&a=1&x=66&y=9&pt_up=1'},
	{'categories': ['Insurance market', 'Independent insurance intermediary', 'Insurance agent branch'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=115&ktasearch_label=Insurance+agent+branch&ktasearch_prev_value=31&pmod=primaryType&n=&st=0&i=&a=1&x=38&y=3&pt_up=1'},
	{'categories': ['Insurance market', 'Independent insurance intermediary', 'Broker'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=49&ktasearch_label=Broker&ktasearch_prev_value=115&pmod=primaryType&n=&st=0&i=&a=1&x=72&y=8'},
	{'categories': ['Insurance market', 'Independent insurance intermediary', 'Multiple agent'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=50&ktasearch_label=Multiple+agent&ktasearch_prev_value=49&pmod=primaryType&n=&st=0&i=&a=1&x=69&y=10&pt_up=1'},
	{'categories': ['Insurance market', 'Insurance expert advisor', 'Business organisation'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=53&ktasearch_label=Business+organisation&ktasearch_prev_value=50&pmod=primaryType&n=&st=0&i=&a=1&x=36&y=11&pt_up=1'},
	{'categories': ['Insurance market', 'Insurance expert advisor', 'Insurance expert advisor - natural person'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=54&ktasearch_label=Insurance+expert+advisor-natural+person&ktasearch_prev_value=53&pmod=primaryType&n=&st=0&i=&a=1&x=64&y=1&pt_up=1'},
	{'categories': ['Fund market', 'Private pension fund'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=39&ktasearch_label=Private+pension+fund&ktasearch_prev_value=54&pmod=primaryType&n=&st=0&i=&a=1&x=44&y=10'},
	{'categories': ['Fund market', 'Voluntary funds', 'Voluntary pension fund'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=43&ktasearch_label=Voluntary+pension+fund&ktasearch_prev_value=39&pmod=primaryType&n=&st=0&i=&a=1&x=58&y=16'},
	{'categories': ['Fund market', 'Voluntary funds', 'Voluntary mutual fund'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=42&ktasearch_label=Voluntary+mutual+fund&ktasearch_prev_value=43&pmod=primaryType&n=&st=0&i=&a=1&x=32&y=7&pt_up=1'},
	{'categories': ['Fund market', 'Voluntary funds', 'Voluntary healthcare fund'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=41&ktasearch_label=Voluntary+healthcare+fund&ktasearch_prev_value=42&pmod=primaryType&n=&st=0&i=&a=1&x=71&y=3'},
	{'categories': ['Other institution', 'Auditor'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=110&ktasearch_label=Auditor&ktasearch_prev_value=42&pmod=primaryType&n=&st=0&i=&a=1&x=77&y=8'},
	{'categories': ['Other institution', 'Occupational pension provider'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=100&ktasearch_label=Occupational+pension+provider&ktasearch_prev_value=110&pmod=primaryType&n=&st=0&i=&a=1&x=30&y=8&pt_up=1'},
	{'categories': ['Branch of Hungarian institution', 'Insurance sector', 'Insurance branch'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=64&ktasearch_label=Insurance+branch&ktasearch_prev_value=64&pmod=primaryType&n=&st=0&i=&a=1&x=66&y=22'},
	{'categories': ['Branch of Hungarian institution', 'Insurance sector', 'Independent insurance broker branch'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=65&ktasearch_label=Independent+insurance+broker+branch&ktasearch_prev_value=64&pmod=primaryType&n=&st=0&i=&a=1&x=21&y=14'},
	{'categories': ['Branch of Hungarian institution', 'Money market sector', 'Branch of credit institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=62&ktasearch_label=Branch+of+credit+institution&ktasearch_prev_value=65&pmod=primaryType&n=&st=0&i=&a=1&x=39&y=6'},
	{'categories': ['Branch of Hungarian institution', 'Capital market sector'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=-25&ktasearch_label=Capital+market+sector&ktasearch_prev_value=62&pmod=primaryType&n=&st=0&i=&a=1&x=47&y=10'},
	{'categories': ['Foreign institution providing cross-border services', 'Money market sector'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=68&ktasearch_label=Money+market+sector&ktasearch_prev_value=127&pmod=primaryType&n=&st=0&i=&a=1&x=32&y=18&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Capital market sector', 'Investment fund manager'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=78&ktasearch_label=Investment+fund+manager&ktasearch_prev_value=78&pmod=primaryType&n=&st=0&i=&a=1&x=33&y=7&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Capital market sector', 'Investment enterprise'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=77&ktasearch_label=Investment+enterprise&ktasearch_prev_value=78&pmod=primaryType&n=&st=0&i=&a=1&x=22&y=8&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Capital market sector', 'Alternative Investment Fund Manager with cross-border services defined by AIFMD'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=134&ktasearch_label=Alternative+Investment+Fund+Manager+with+cross-border+services+defined+by+AIFMD&ktasearch_prev_value=77&pmod=primaryType&n=&st=0&i=&a=1&x=57&y=12&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Funds sector', 'Occupational pension provider'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=103&ktasearch_label=Occupational+pension+provider&ktasearch_prev_value=134&pmod=primaryType&n=&st=0&i=&a=1&x=33&y=16&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Insurance sector', 'Insurer'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=73&ktasearch_label=Insurer&ktasearch_prev_value=103&pmod=primaryType&n=&st=0&i=&a=1&x=63&y=6'},
	{'categories': ['Foreign institution providing cross-border services', 'Insurance sector', 'Insurance broker'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=74&ktasearch_label=Insurance+broker&ktasearch_prev_value=73&pmod=primaryType&n=&st=0&i=&a=1&x=49&y=12&pt_up=1'},
	{'categories': ['Foreign institution providing cross-border services', 'Insurance sector', 'Insurance consultant'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=76&ktasearch_label=Insurance+consultant&ktasearch_prev_value=74&pmod=primaryType&n=&st=0&i=&a=1&x=65&y=9&pt_up=1'},
	{'categories': ['Representative office', 'Money market sector', 'Foreign representative office of Hungarian financial institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=28&ktasearch_label=Foreign+repr.off.+of+Hung.financial+inst.&ktasearch_prev_value=76&pmod=primaryType&n=&st=0&i=&a=1&x=28&y=22'},
	{'categories': ['Representative office', 'Money market sector', 'Hungarian representative office of foreign financial institution'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=29&ktasearch_label=Hungarian+repr.office+of+foreign+financial+inst.&ktasearch_prev_value=28&pmod=primaryType&n=&st=0&i=&a=1&x=63&y=16'},
	{'categories': ['Representative office', 'Capital market sector'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=-22&ktasearch_label=Capital+market+sector&ktasearch_prev_value=29&pmod=primaryType&n=&st=0&i=&a=1&x=21&y=18'},
	{'categories': ['Representative office', 'Insurance sector', 'Hungarian representative office of foreign insurance broker'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=117&ktasearch_label=Hungarian+repr.office+of+foreign+insurance+broker&ktasearch_prev_value=-22&pmod=primaryType&n=&st=0&i=&a=1&x=90&y=22'},
	{'categories': ['Representative office', 'Insurance sector', 'Foreign representative office of Hungarian insurer'], 'url': 'https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?ktasearch_value=37&ktasearch_label=Foreign+repr.off.+of+Hung.+Insurer&ktasearch_prev_value=117&pmod=primaryType&n=&st=0&i=&a=1&x=75&y=8'}
]

#tabs on detail pages not to process
excluded_tabs = ["Broker relationship (Mandator role)"]

search_url = "https://alk.mnb.hu/en/left_menu/market_participants/kereso/kereses?st=0&i="

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

#how to run through an index 
def parse_index(bs_page, categories, start_num, results_count):
	#find the table of results -- all pages seem to have the same structure
	index_table = bs_page.find("table", attrs={'class': 'ResultTable'})
	index_rows = index_table.tbody.find_all("tr")

	entity_count = start_num

	#go through the results one-by-one
	if (len(index_rows) > 0):
		for index_row in index_rows:
			#skip non-data rows
			index_row_class = index_row.get('class')
			if (index_row_class is None):
				continue
			if (('Odd' not in index_row_class) and ('Even' not in index_row_class)):
				continue

			#find the identifier in the second column
			td_list = index_row.find_all("td")
			row_identifier = parse_text(td_list[1].text.strip())

			#run a search by identifier, in order to get a link to the entity details page
			row_search_url = search_url + row_identifier
			turbotlib.log("    Loading intermediate search page for entity " + row_identifier + " (" + str(entity_count) + " / " + str(results_count) + ")")
			row_search_page = get_doc(row_search_url)

			#find the results table (same format as before) - link is in first row, first column
			row_search_table = row_search_page.find("table", attrs={'class': 'ResultTable'})
			if (row_search_table is not None):
				if (row_search_table.tbody.tr is not None):
					row_search_result = row_search_table.tbody.tr
					entity_detail_url = row_search_result.td.a['href']

					#load the detail page
					turbotlib.log("    Loading details for entity " + row_identifier + " (" + str(entity_count) + " / " + str(results_count) + ")")
					parse_detail(entity_detail_url, categories)

			entity_count += 1

#run through the details page for each individual entity -- they have different tabs
def parse_detail(page_url, categories):
	detail_page = get_doc(page_url)

	#create an object to add information to
	output = {
		'source_url': page_url,
		'sample_date': sample_date, 
		'categories': categories,
		'source': 'Magyar Nemezeti Bank'
	}
	added_info = False

	#get a list of all the available data tabs - go through them in turn
	table_list = detail_page.find_all("table", attrs={"class": "ResultBox"})
	for table in table_list:
		#get table title from div above - from the id, ignoring the initial "table_"
		table_title_tag = table.find_previous("div", attrs={"class": "Holder"})
		table_title = table_title_tag['id'][6:]

		#proceed if title is on the naughty list
		if (table_title not in excluded_tabs):

			#how to process each tab depends on whether it's just plain data, or if it's a table with headers
			if (table.thead is None):
				#No header, two columns means values and 
				row_list = table.find_all("tr")
				for row in row_list:
					col_list = row.find_all("td")
					
					#check for errors with extra tabs
					if (len(col_list) != 2):
						print("      Error with tab '" + table_title + "' on page " + page_url + " - not two columns")
						quit()

					#get the label from the first column
					label = parse_text(col_list[0].text.strip()[:-1]) #remove trailing colon
					
					#value in second column can bean image or words
					if (col_list[1].img is not None):
						img_src = col_list[1].img['src']
						img_src_words = img_src.split("/")
						if (img_src_words[-1] == "szuperkereso_1.png"):
							value = "Active"
						else:
							value = "Not active"
					else:
						value = parse_text(col_list[1].text.strip())

					if ((len(label) > 3) and (len(value) > 3)):
						#don't overwrite values if we've seen them before
						if (label not in output):
							output[label] = value
							added_info = True

			#dealing with tabs that contain a full table
			else:
				#get the headers
				headers = []
				header_row = table.thead.tr
				header_cols = header_row.find_all("th")
				for header_col in header_cols:
					header = parse_text(header_col.text.strip())
					headers.append(header)

				#extract the data from the main rows - each row becomes an object, and we keep a list of such objects
				data = []
				table_rows = table.tbody.find_all("tr")
				for table_row in table_rows:
					#skip rows with nothing but a page forward/backward button
					if (len(table_row.find_all("div")) > 0):
						continue

					#go through columns one by one, adding to our object
					data_row = {}
					table_cols = table_row.find_all("td")
					for table_col in table_cols:
						#get the header, based on 
						col_index = table_cols.index(table_col)
						header = headers[col_index]

						#get the value - as above, could be image or text
						if (table_col.img is not None):
							img_src = table_col.img['src']
							img_src_words = img_src.split("/")
							if (img_src_words[-1] == "szuperkereso_1.png"):
								value = "Active"
							else:
								value = "Not active"
						else:
							value = parse_text(table_col.text.strip())

						#add to our data if we found anything
						if (len(value) > 3):
							data_row[header] = value

					#store row if we found anything
					if (len(data_row) > 0):
						data.append(data_row)

				#store data if we find any
				if (len(data) > 0):
					output[table_title] = data
					added_info = True

	#print the result if we found any information
	if (added_info):
		print(json.dumps(output))

#get going
sample_date = str(date.today())
turbotlib.log("Starting run on " + sample_date) # Optional debug logging

#load each category in turn
source_count = str(len(sources))
for source in sources:
	#monitor progress
	source_name = " > ".join(source['categories'])
	source_index = str(sources.index(source) + 1)
	turbotlib.log("Loading category " + source_index + "/" + source_count + ": " + source_name)

	#load the index page for the category
	source_page = get_doc(source['url'])

	#find the number of results - tells us how many pages we need to bother with
	source_results_div = source_page.find("div", attrs={"class": "ResultSize"})
	source_results_count = parse_text(source_results_div.find_next("b").text.strip())
	turbotlib.log("  Found " + source_results_count + " entities")

	#work out how many pages of results for this category
	results_count = int(source_results_count)
	page_count = int(math.floor(results_count / 10))
	if ((results_count % 10) != 0):
		page_count += 1

	#load results from front page - the detail is dealt with in the function
	parse_index(source_page, source['categories'], 1, results_count)

	#deal with multiple pages too
	if (page_count > 1):
		for page in range(2, page_count + 1):
			turbotlib.log("  Loading index page " + str(page) + "/" + str(page_count))
			page_url = source['url'] + "&pt_p=" + str(page)
			page_doc = get_doc(page_url)
			start_num = (10 * (page - 1)) + 1
			parse_index(page_doc, source['categories'], start_num, results_count)