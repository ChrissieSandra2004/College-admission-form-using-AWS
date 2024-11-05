import json
from datetime import datetime

def lambda_handler(event, context):
    # Extracting the intent name
    intent_name = event['currentIntent']['name']

    # Handling the "BookHotel" intent
    if intent_name == 'BookHotel':
        slots = event['currentIntent']['slots']
        greeting_complete = slots['GreetingComplete']
        user_name = slots['UserName']
        phone_number = slots['PhoneNumber']
        location = slots['Location']
        check_in_date = slots['CheckInDate']
        check_out_date = slots['CheckOutDate']
        number_of_rooms = slots['NumberOfRooms']
        number_of_people = slots['NumberOfPeople']
        room_type = slots['RoomType']

        # Step 1: Greet the user if the greeting hasn't been completed
        if greeting_complete is None:
            # Mark the greeting as complete
            slots['GreetingComplete'] = 'Yes'
            return elicit_slot(event, slots, 'GreetingComplete', 'Hello! Welcome to Marriott! How can I assist you today?')

        # Step 2: Collect the user's name if not provided
        if user_name is None:
            return elicit_slot(event, slots, 'UserName', 'Sure, can I have your name for the reservation?')

        # Step 3: Collect the phone number if not provided
        if phone_number is None:
            return elicit_slot(event, slots, 'PhoneNumber', f'Hi {user_name}, kindly provide your contact number.')

        # Step 4: Collect other booking details
        if location is None:
            return elicit_slot(event, slots, 'Location', 'Where would you like to book the hotel?')
        if check_in_date is None:
            return elicit_slot(event, slots, 'CheckInDate', 'What is your check-in date?')
        if check_out_date is None:
            return elicit_slot(event, slots, 'CheckOutDate', 'What is your check-out date?')
        if number_of_rooms is None:
            return elicit_slot(event, slots, 'NumberOfRooms', 'How many rooms would you like to book?')
        if number_of_people is None:
            return elicit_slot(event, slots, 'NumberOfPeople', 'How many people will be staying?')
        if room_type is None:
            return elicit_slot(event, slots, 'RoomType', 'What type of room would you like? (standard, deluxe, suite)')

        # Calculate the number of nights
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
            number_of_nights = (check_out - check_in).days

            if number_of_nights <= 0:
                return close(event, "Failed", "The check-out date must be after the check-in date.")

        except ValueError:
            return close(event, "Failed", "Invalid date format. Please provide dates in the format YYYY-MM-DD.")

        # Determine the base rate per night based on the room type
        room_type = room_type.lower()
        if room_type == 'standard':
            base_rate_per_night = 100
        elif room_type == 'deluxe':
            base_rate_per_night = 150
        elif room_type == 'suite':
            base_rate_per_night = 200
        else:
            return close(event, "Failed", "The specified room type is not available. Please choose from standard, deluxe, or suite.")

        # Calculate the total price
        total_price = number_of_nights * base_rate_per_night * int(number_of_rooms)

        # Fulfill the booking request with a price
        response_message = (f"Thank you, {user_name}. Hotel booking confirmed in {location} from {check_in_date} "
                            f"to {check_out_date} for {number_of_rooms} {room_type} room(s), "
                            f"accommodating {number_of_people} people. The total price for the stay is ${total_price}. "
                            f"We will contact you at {phone_number} if we need further information.")

        # Respond to Lex to fulfill the intent
        return close(event, "Fulfilled", response_message)

    # If the intent is not recognized
    return close(event, "Failed", "I'm not able to handle this request. Please try again later or contact customer service.")

def elicit_slot(event, slots, slot_to_elicit, message):
    """Elicit a slot from the user."""
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": event['currentIntent']['name'],
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }

def close(event, fulfillment_state, message):
    """Close the conversation with the user."""
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
