import PhoneNumberTracker
from PhoneNumberTracker import phonenumbers

try:
    # Get phone number input with country code
    number = input("Enter the phone number with country code: ")
    
    # Check if '+' is included in the input, if not, add it
    if "+" not in number:
        number = "+" + number
    
    # Parse the phone number to check its validity
    parsed_number = phonenumbers.parse(number)
    if not phonenumbers.is_valid_number(parsed_number):
        print("Invalid phone number")
        exit(1)

except Exception as e:
    print(e)
    exit(1)

try:
    # Create an object of PhoneNumberTracker class
    track = PhoneNumberTracker.PhoneNumberTracker(number)

    # Validate the phone number
    if track.validate_phone_number():
        print("Valid phone number")

        # Get country information
        country = track.get_country()
        print("Country:", country)

        # Get carrier information
        carrier = track.get_carrier()
        print("Carrier:", carrier)

        # Get timezone information
        timezone = track.get_timezone()
        print("Timezone:", timezone)

        # Get geolocation information
        geolocation = track.get_geolocation()
        print("Geolocation:", geolocation)

        # Get map and save it
        map, lat, lng = track.get_map()
        map.save("index.html")
        print("Map saved to index.html")

        # Reverse geocode to get address from latitude and longitude
        address = track.reverse_geocode(lat, lng)
        print("Address:", address)
    else:
        print("Invalid phone number")

except Exception as e:
    print(e)
    exit(1)