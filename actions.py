from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import json
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage

def getPriceRange(str):
    
    retVal = 300;

    str = str.lower()
    #print('\nNew Case  :', str)
    pattern = r'([0-9]*|[0-9]*.[0-9]*])'
    txt = str
    #x = re.findall(pattern , txt)
    x = re.findall(r'{_|-|between|greater|range|less|more|than|then||to|_|> than|< than|>|<|>=|<=|}*.[0-9]*|[0-9]*.[0-9]*]', str)

    p1 = -1
    p2 = -1
    sign = 'NOT_YET_SET'
    if ((x != None)):
        #print( x)
        #print(x.group())
        for ele in x:
            # do something with each found email string
            #print ('ELE : ', ele)

            if (((ele == 'greater') or (ele == '>') or (ele == 'more')) and (sign == 'NOT_YET_SET')) :
                sign = '>' 
            elif (((ele == 'less') or (ele == '<') ) and (sign == 'NOT_YET_SET')) :
                sign = '<' 
            elif (((ele == 'between') or (ele == 'range') or (ele == 'to') or (ele == '-')) and (sign == 'NOT_YET_SET')) :
                sign = 'range' 
            elif ((ele != '') and (p1 == -1)) :
                try:
                    p1 = float(ele)
                except:
                    p1 = -1
            elif ((ele != '') and (p2 == -1)) :
                try:
                    p2 = float(ele)
                except:
                    p2 = -1
            
    else:
        p1 = 700
        sign = '>'

    return(p1, p2,sign)
	
def getRestaurants(tracker, required_records = 5):
	config={ "user_key":"f4924dc9ad672ee8c4f8c84743301af5"}
	#config = {'user_key':"455c41499144739a6f131347a8130495"}
	zomato = zomatopy.initialize_app(config)
	loc = tracker.get_slot('location')
	# Avi Begin
	 
	Tier_1_city = 'Ahmedabad|Delhi|Bengaluru|Chennai|Delhi|Hyderabad|Kolkata|Mumbai|Pune|'
	Tier_2_city = 'Agra|Ajmer|Aligarh|Amravati|Amritsar|Asansol|Aurangabad|Bareilly|Belgaum|Bhavnagar|Bhiwandi|Bhopal|\
	Bhubaneswar|Bikaner|Bilaspur|Bokaro Steel City|Chandigarh|Coimbatore|Cuttack|Dehradun|Dhanbad|Bhilai\
	|Durgapur|Dindigul|Erode|Faridabad|Firozabad|Ghaziabad|Gorakhpur|Gulbarga|Guntur|Gwalior|Gurgaon|Guwahati|\
	Hamirpur|Hubli–Dharwad|Indore|Jabalpur|Jaipur|Jalandhar|Jammu|Jamnagar|Jamshedpur|Jhansi|Jodhpur|Kakinada|\
	Kannur|Kanpur|Karnal|Kochi|Kolhapur|Kollam|Kozhikode|Kurnool|Ludhiana|Lucknow|Madurai|Malappuram|Mathura|\
	Mangalore|Meerut|Moradabad|Mysore|Nagpur|Nanded|Nashik|Nellore|Noida|Patna|Pondicherry|Purulia|Prayagraj|\
	Raipur|Rajkot|Rajahmundry|Ranchi|Rourkela|Salem|Sangli|Shimla|Siliguri|Solapur|Srinagar|Surat|Thanjavur|\
	Thiruvananthapuram|Thrissur|Tiruchirappalli|Tirunelveli|Tiruvannamalai|Ujjain|Bijapur|Vadodara|Varanasi|\
	Vasai-Virar City|Vijayawada|Visakhapatnam|Vellore|Warangal'

	pattern = Tier_1_city + Tier_2_city

	x = re.search(pattern , loc,re.IGNORECASE)

	if (x == None):
		#print('\n ****** LOCATION NOT FOUND ******* : ', loc)
		response=""
	
		response=response+ "inside ActionSearchRestaurants Its a Tier 3 location. We do not operate in that area yet " + "\n"
		#dispatcher.utter_message("---------"+response)
		#SlotSet('check_op',False)
		#return [SlotSet('location',loc)]
		return (response)
	# Avi Ends
	
	cuisine = tracker.get_slot('cuisine')
	location_detail=zomato.get_location(loc, 1)
	d1 = json.loads(location_detail)
	lat=d1["location_suggestions"][0]["latitude"]
	lon=d1["location_suggestions"][0]["longitude"]
	cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
	average_cost_for_two_ppl = 300	
	rest_dicts = dict()
	
	response=""
	start = 1
	
	avg_price = tracker.get_slot('price')
	p1, p2, sign = getPriceRange(avg_price)
	
	# todo : Set avg ptice logic : DONE
	# check if this functionalitu can be made reusable : DONE
	# write email functionality : NOT DONE
	# exception handling : NOT DONE
	# sort : DONE
	# nlu update
	
	for i in range(1, 100, 20):
		start = i
		#count = 20 + i-1
		count = 20

		#results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 100)
		#start = 1
		#count = 20
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), count, start)
		d = json.loads(results)
		#print(results)
		if d['results_found'] == 0:
			response= "no results"
		else:
						
			for restaurant in d['restaurants']:
				#response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"
				
				flag = 0;
				avgCostForTwo = restaurant['restaurant']['average_cost_for_two']
				if ((sign == '<') and (avgCostForTwo <= p1)):
					flag = 1
				if ((sign == '>') and (avgCostForTwo >= p1)):
					flag = 1	
				if ((sign == 'range') and (avgCostForTwo >= p1) and (avgCostForTwo <= p2)):
					flag = 1					
				#if ((sign == '>') or (sign == '<') or ((sign == 'range')):
				
				
				#if (restaurant['restaurant']['average_cost_for_two'] >= average_cost_for_two_ppl):
				
				#if (restaurant['restaurant']['average_cost_for_two'] >= average_cost_for_two_ppl):
				if (flag == 1):
					rest_name_addr = restaurant['restaurant']['name'] + " in " + restaurant['restaurant']['location']['address'] + ', with avg Cost for 2 as : ' + str(restaurant['restaurant']['average_cost_for_two']) + ', '
					rating = restaurant['restaurant']['user_rating']['aggregate_rating']
					#response=response+ "JSR 1 : ActionSearchRestaurants "+ rest_name_addr + ' has been rated ' + rating  +"\n"
					
					rest_dicts[rest_name_addr] = float(rating)
					if len(rest_dicts) >= required_records:
						break
		
		if len(rest_dicts) >= required_records:
			break			
	sorted_rest_list  =  sorted(rest_dicts.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
	for i, rest_rating in enumerate (sorted_rest_list):
		response = response+ rest_rating[0] + ' has been rated ' + str(rest_rating[1])  + "\n"

	if (response == "" ):
		response = 'There are no restaurants in this price range !!!'
	#response = response + '__AVG _ Price_' + avg_price
	
	return (response, loc)
	
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'
		
	def run(self, dispatcher, tracker, domain):
		response = ''
		loc = ''
		try:
			response, loc = getRestaurants(tracker, 5)
		except Exception as e:
			response = ' Eception has occured while Searching Restaurants : \n ' + e
	
		dispatcher.utter_message("---------\n" + response + "\n---------")
		return [SlotSet('location',loc)]

class CheckLocation(Action):
	def name(self):
		return 'check_location'
		
	def run(self, dispatcher, tracker, domain):

		loc = tracker.get_slot('location')
		if loc == '':
			return(SlotSet('check_op',False))
			#return str(False)
			
		#print('\n ****** Printing Location ******* : ', loc)
		Tier_1_city = 'Ahmedabad|Delhi|Bangalore|Chennai|Delhi|Hyderabad|Kolkata|Mumbai|Pune|'
		Tier_2_city = 'Agra|Ajmer|Aligarh|Amravati|Amritsar|Asansol|Aurangabad|Bareilly|Belgaum|Bhavnagar|Bhiwandi|Bhopal|\
		Bhubaneswar|Bikaner|Bilaspur|Bokaro Steel City|Chandigarh|Coimbatore|Cuttack|Dehradun|Dhanbad|Bhilai\
		|Durgapur|Dindigul|Erode|Faridabad|Firozabad|Ghaziabad|Gorakhpur|Gulbarga|Guntur|Gwalior|Gurgaon|Guwahati|\
		Hamirpur|Hubli–Dharwad|Indore|Jabalpur|Jaipur|Jalandhar|Jammu|Jamnagar|Jamshedpur|Jhansi|Jodhpur|Kakinada|\
		Kannur|Kanpur|Karnal|Kochi|Kolhapur|Kollam|Kozhikode|Kurnool|Ludhiana|Lucknow|Madurai|Malappuram|Mathura|\
		Mangalore|Meerut|Moradabad|Mysore|Nagpur|Nanded|Nashik|Nellore|Noida|Patna|Pondicherry|Purulia|Prayagraj|\
		Raipur|Rajkot|Rajahmundry|Ranchi|Rourkela|Salem|Sangli|Shimla|Siliguri|Solapur|Srinagar|Surat|Thanjavur|\
		Thiruvananthapuram|Thrissur|Tiruchirappalli|Tirunelveli|Tiruvannamalai|Ujjain|Bijapur|Vadodara|Varanasi|\
		Vasai-Virar City|Vijayawada|Visakhapatnam|Vellore|Warangal'
	
		pattern = Tier_1_city + Tier_2_city

		x = re.search(pattern , loc,re.IGNORECASE)

		if (x == None):
			#print('\n ****** LOCATION NOT FOUND ******* : ', loc)
			#response=""
		
			#response=response+ "inside CheckLocation Its a Tier 3 location. We do not operate in that area yet " + "\n"
			#dispatcher.utter_message("---------"+response)
			SlotSet('check_op',False)
			#return [SlotSet('location',loc)]
			return(SlotSet('check_op',False))
			
		else:
			return(SlotSet('check_op',True))
					
		#return str(True)
		
		#if validate_location(loc):
		#	SlotSet('check_op',True)
		#else:
		#	SlotSet('check_op',False)
		#return True

		
class ActionSendEmail(Action):
	def name(self):
		return 'action_send_email'
		
	def run(self, dispatcher, tracker, domain):

		response = ''
		loc = ''
		try:
			response, loc = getRestaurants(tracker, 10)
		except Exception as e:
			response = str(e) + 'Exception occured while getting Top 10 Restaurants...'
			
		try:
			addr = tracker.get_slot('people')
			mail_content = response
			#The mail addresses and password
			sender_address = 'aimlchatbot44@gmail.com'
			sender_pass = 'rasabot1234'
			receiver_address = addr
			#Setup the MIME
			message = MIMEMultipart()
			message['From'] = sender_address
			message['To'] = receiver_address
			message['Subject'] = 'Restaurent Recommendations.'   #The subject line
			#The body and the attachments for the mail
			message.attach(MIMEText(mail_content, 'plain'))
			#Create SMTP session for sending the mail
			session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
			session.starttls() #enable security
			session.login(sender_address, sender_pass) #login with mail_id and password
			text = message.as_string()
			session.sendmail(sender_address, receiver_address, text)
		except Exception as e:
			response=response+str(e)
			a = 10
		finally:
			session.quit()
			
		response = response + '\n\n' +  'Eception has occured while sending email...' 
			
			
	
		dispatcher.utter_message("---------\n" + response + "\n---------")

		return [SlotSet('location',loc)]
		
# def getEmail(email):
#     addr = email.get_slot('people')
#     mail_content = ''
#     #The mail addresses and password
#     sender_address = 'rasabot5@gmail.com'
#     sender_pass = 'rasabot1234%'
#     receiver_address = addr
#     #Setup the MIME
#     message = MIMEMultipart()
#     message['From'] = sender_address
#     message['To'] = receiver_address
#     message['Subject'] = 'Restaurent Recommendations.'   #The subject line
#     #The body and the attachments for the mail
#     message.attach(MIMEText(mail_content, 'plain'))
#     #Create SMTP session for sending the mail
#     session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
#     session.starttls() #enable security
#     session.login(sender_address, sender_pass) #login with mail_id and password
#     text = message.as_string()
#     session.sendmail(sender_address, receiver_address, text)
#     session.quit()
#     print('eMail Sent')