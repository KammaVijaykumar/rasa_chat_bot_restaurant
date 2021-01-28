## intent:affirm
- yes
- yep
- yeah
- indeed
- that's right
- ok
- great
- right, thank you
- correct
- great choice
- sounds really good
- thanks

## intent:goodbye
- bye
- goodbye
- good bye
- stop
- end
- farewell
- Bye bye
- have a good one
- no
- no thanks
- nope
- nah

## intent:greet
- hey
- howdy
- hey there
- hello
- hi
- good morning
- good evening
- dear sir

## intent:restaurant_search
- i'm looking for a place to eat
- I want to grab lunch
- I am searching for a dinner spot
- I am looking for some restaurants in [Delhi](location).
- I am looking for some restaurants in [Bangalore](location)
- show me [chinese](cuisine) restaurants
- show me [chines]{"entity": "cuisine", "value": "chinese"} restaurants in the [New Delhi]{"entity": "location", "value": "Delhi"}
- show me a [mexican](cuisine) place in the [centre](location)
- i am looking for an [indian](cuisine) spot called olaolaolaolaolaola
- search for restaurants
- anywhere in the [west](location)
- I am looking for [asian fusion](cuisine) food
- I am looking a restaurant in [294328](location)
- in [Gurgaon](location)
- [South Indian](cuisine)
- [North Indian](cuisine)
- [Italian](cuisine)
- [Chinese]{"entity": "cuisine", "value": "chinese"}
- [chinese](cuisine)
- [Lithuania](location)
- Oh, sorry, in [Italy](location)
- in [delhi](location)
- I am looking for some restaurants in [Mumbai](location)
- I am looking for [mexican indian fusion](cuisine)
- can you book a table in [rome](location) in a [moderate]{"entity": "price", "value": "mid"} price range with [british](cuisine) food for [four]{"entity": "people", "value": "4"} people
- [central](location) [indian](cuisine) restaurant
- please help me to find restaurants in [pune](location)
- Please find me a restaurantin [bangalore](location)
- [mumbai](location)
- show me restaurants
- please find me [chinese](cuisine) restaurant in [delhi](location)
- can you find me a [chinese](cuisine) restaurant
- [delhi](location)
- please find me a restaurant in [ahmedabad](location)
- please show me a few [italian](cuisine) restaurants in [bangalore](location)
- test
- in price less than [300](price)
- in price below [300](price)
- in price between [300 to 700](price)
- in price between [300 - 700](price)
- in range of [300 to 700](price)
- in range of [300 - 700](price)
- in price more than [700](price)
- [Less_than_300](price)
- [Lesser than Rs. 300](price)
- [Between_300_to_700](price)
- [Rs. 300 to 700](price)
- [More_than_700](price)
- [More than 700](price)
- [< 300](price)
- [> 300](price)
- [< 700](price)
- [> 700](price)
- [Rs. 300 to 700](price)
- [More_than_700](price)
- [More than 700](price)

- find a restaurant
- [bangaluru](location)
- [Chinese]{"entity": "cuisine", "value": "chinese"}
- find restaurants with price less than [300](price)
- find restaurants with price between [300 to 700](price)
- find restaurants with price above [700](price)
- find restuarant
- find a [american](cuisine) restuarant in [pune](location)
- food recommendation
- restaurant recommendation in [bombay](location)
- [chinese](cuisine) in [mumbai](location) 


## synonym:4
- four

## synonym:Delhi
- New Delhi

## synonym:Bangalore
- bngalore
- bengalluru
- Bangalor
- bangalore
- bengaluru
- Bengaluru

## synonym:Hyderabad
- hyderabad
- Secunderabad
- secunderabad
- cyberabad
- Cyberabad

## synonym:Mumbai
- Bombay
- mumbai
- bombay

## synonym:Kolkata
- Calcutta
- kolkata
- kolkatta
- calcutta
- calcuta

## synonym:Chennai
- chennai
- madras
- Madras

## synonym:chinese
- chines
- Chinese
- Chines
- china

## synonym:mid
- moderate

## synonym:vegetarian
- veggie
- vegg

## regex:greet
- hey[^\s]*

## regex:pincode
- [0-9]{6}

## regex:TIER_1_ID
- [Agra]

## regex: email
- /^\S+@\S+\.\S+$/
	
## intent: inform
- my email is [shukla.avinash@gmail.com](people)
- This is my email [avi.shukla1009@gmail.com](people)
- [mkchrystal@gmail.com](people)
- [vijaykumar.gavs@gmail.com](people)
- [vishal.pardeshi@gmail.com](people)