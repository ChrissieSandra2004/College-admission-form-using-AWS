import json
from datetime import datetime

# Define your function to validate slots
def validate_slots(slots):
    # List of required slots
    required_slots = ['UserName', 'PhoneNumber', 'Location', 'CheckInDate', 'CheckOutDate', 'NumberOfRooms', 'NumberOfPeople', 'RoomType']
    
    # Check for required slots and return the first one that is missing
    for slot in required_slots:
        if not slots[slot]:
            return {
                'isValid': False,
                'invalidSlot': slot,
                'message': f'Please provide your {slot}.'
            }
    
    # Additional validation logic (e.g., date validation) can go here

    return {'isValid': True}

def lambda_handler(event, context):
    # Extract the slots and intent name
    slots = event['currentIntent']['slots']
    intent_name = event['currentIntent']['name']
    
    # Validate slots
    order_validation_result = validate_slots(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            # Elicit the invalid slot
            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": order_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent_name,
                        "slots": slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": order_validation_result['message']
                    }
                ]
            }
        else:
            # If all slots are valid, delegate the intent
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent_name,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        # Fulfillment response logic
        user_name = slots['UserName']
        location = slots['Location']
        check_in_date = slots['CheckInDate']
        check_out_date = slots['CheckOutDate']
        number_of_rooms = slots['NumberOfRooms']
        room_type = slots['RoomType'].lower()
        total_price = 300  # Example total price for the booking
        phone_number = slots['PhoneNumber']

        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": f"Thank you, {UserName}. Your hotel booking in {Location} from {CheckInDate} to {CheckOutDate} "
                                   f"for {NumberOfRooms} {RoomType} room(s) has been confirmed. The total price for your stay is ${total_price}. "
                                   f"We will contact you at {PhoneNumber} if we need further information."
                    }
                },
                "intent": {
                    "name": "HotelBooking",
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Thank you, {UserName}. Your hotel booking is confirmed!"
                }
            ]
        }

    return response
