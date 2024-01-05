import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import folium
import re
from opencage.geocoder import OpenCageGeocode
import os
# from dotenv import load_dotenv

# Get the API key from:
# load_dotenv()  # take environment variables from .env.
# OPENCAGE_API = os.environ.get("OPENCAGE_API")
OPENCAGE_API = "34dc4de4441146eb8b6b2dbe9f1c03ed"


class PhoneNumberTracker:
    def __init__(self, number):
        self.number = str(number)

    def validate_phone_number(self, pulse=True):
        """
        Validates the phone number based on a regular expression pattern.

        Args:
        - pulse (bool): Default True, optional

        Returns:
        - bool: True if the phone number is valid, False otherwise.
        """

        # Regular expression pattern for phone numbers
        pattern = r"^\+\d{1,3}\d{3,}$"

        # Check if the phone number is valid
        if re.match(pattern, self.number):
            return True
        else:
            return False

    def get_country(self):
        """
        Retrieves the country name associated with the phone number.

        Returns:
        - str: Country name if found, else "No country found".
        """

        try:
            # Parse the phone number
            phone_number = phonenumbers.parse(self.number)

            # Get the country name
            country = geocoder.description_for_number(phone_number, "en")

            # Return the country name if found, else return "No country found"
            return country if country else "No country found"
        except phonenumbers.phonenumberutil.NumberParseException as e:
            return f"Error: {str(e)}"

    def get_carrier(self):
        """
        Retrieves the carrier name associated with the phone number.

        Returns:
        - str: Carrier name if found, else "No carrier found".
        """

        try:
            # Parse the phone number
            phone_number = phonenumbers.parse(self.number)

            # Get the carrier name
            carrier_name = carrier.name_for_number(phone_number, "en")

            # Return the carrier name if found, else return "No carrier found"
            return carrier_name if carrier_name else "No carrier found"
        except phonenumbers.phonenumberutil.NumberParseException as e:
            return f"Error: {str(e)}"

    def get_timezone(self):
        """
        Retrieves the timezone associated with the phone number.

        Returns:
        - str or list: Timezone(s) if found, else "No timezone found".
        """

        try:
            # Parse the phone number
            phone_number = phonenumbers.parse(self.number)

            # Get the timezone(s)
            time_zone = timezone.time_zones_for_number(phone_number)

            # Return the timezone(s) if found, else return "No timezone found"
            return time_zone if time_zone else "No timezone found"
        except phonenumbers.phonenumberutil.NumberParseException as e:
            return f"Error: {str(e)}"

    def get_geolocation(self):
        """
        Retrieves the geolocation associated with the phone number.

        Returns:
        - str: Geolocation if found, else "No geolocation found".
        """

        try:
            # Parse the phone number
            phone_number = phonenumbers.parse(self.number)

            # Get the geolocation
            location = geocoder.description_for_number(phone_number, "en")

            # Return the geolocation if found, else return "No geolocation found"
            return location if location else "No geolocation found"
        except phonenumbers.phonenumberutil.NumberParseException as e:
            return f"Error: {str(e)}"

    def reverse_geocode(self, lat, lng):
        """
        Performs reverse geocoding based on latitude and longitude.

        Args:
        - lat (float): Latitude
        - lng (float): Longitude

        Returns:
        - str: Address if found, else "No address found".
        """

        try:
            # Perform reverse geocoding
            geocoder = OpenCageGeocode(OPENCAGE_API)

            # Get the address
            result = geocoder.reverse_geocode(lat, lng)

            # Return the address if found, else return "No address found"
            if result and len(result):
                return (
                    result[0]["formatted"]
                    if result[0]["formatted"]
                    else "No address found"
                )
            return "No address found"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_map(self):
        """
        Generates a map based on the phone number's geolocation and saves it as index.html.

        Returns:
        - folium.Map: Folium map object
        - float: Latitude
        - float: Longitude
        """

        try:
            # Perform geocoding
            geocoder = OpenCageGeocode(OPENCAGE_API)

            # Get the latitude and longitude
            query = self.get_geolocation()
            result = geocoder.geocode(query)
            lat = result[0]["geometry"]["lat"]
            lng = result[0]["geometry"]["lng"]

            # Generate the map
            map = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=query).add_to(map)

            # Save the map as index.html
            map.save("index.html")

            # Return the map, latitude and longitude
            return map, lat, lng
        except Exception as e:
            return f"Error: {str(e)}"
