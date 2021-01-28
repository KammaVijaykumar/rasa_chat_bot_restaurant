## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "pune"}
    - slot{"location": "pune"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_price_range
* restaurant_search{"price": "Less_than_300"}
    - slot{"price": "Less_than_300"}
    - action_search_restaurants
    - slot{"location": "pune"}
    - utter_get_email
* inform{"people": "shukla.avinash@gmail.com"}
    - slot{"people": "shukla.avinash@gmail.com"}
    - action_send_email
    - slot{"location": "pune"}
    - utter_goodbye