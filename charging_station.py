'''
Python AAT project
Hi, This is Faizan, This program is to find the nearest charging station to your current location.
it uses simple libraries to get your current location and then uses the OSM maps API (overpassAPI) to find the nearest charging station.
to use this program you will have to first install the libraries as follows
write the following in your command prompt:
pip install folium
pip install overpass
pip install matplotlib
pip install cartopy
pip install qrcode[pil]


These are the following references that I used to write this program:
https://readthedocs.org/projects/python-overpy/downloads/pdf/latest/
https://wiki.openstreetmap.org/wiki/Overpass_API#Quick_Start_(60_seconds):_Interactive_UI
https://www.youtube.com/watch?v=5wXjcykEKnc&t=189s

This one shows how to write queries for the overpass API:
https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0

This is for the geocoding:
https://github.com/geopy/geopy

this one is to calculate the distance between two points on a map, i dont really understand the math but this works well:
# https://en.wikipedia.org/wiki/Haversine_formula
'''


# Import requests and math libraries to make HTTP requests and calculations
import requests
import math
# These libraries are for the map plotting
import folium
# This library is for determining your current location
import geocoder
# for the qr code
import qrcode
import matplotlib.pyplot as plt


range = int(input("Enter the range in km: "))
range = range * 1000


def get_current_location():
    g = geocoder.ip('me')  # over here me means my laptop
    if g.ok:
        return g.latlng
    else:
        print("Failed to retrieve current location.")


current_location = get_current_location()
if current_location:
    lat, lon = current_location
    print(f"Your current latitude is {lat} and longitude is {lon}")
else:
    print("Unable to determine current location.")

# example coordinates, dont use this I just used this for testing
# lat = 12.907523326627508  # Latitude of Bengaluru
# lon = 77.5655353435218  # Longitude of Bengaluru
lats = []
lons = []

# Define the overpass api url
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the overpass query to find charging stations within desired km radius
overpass_query = f"""
[out:json];
node(around:{range},{lat},{lon})[amenity=charging_station];
out;
"""


# Send the request and get the response as json
response = requests.get(overpass_url, params={"data": overpass_query})
data = response.json()

# Check if any charging stations are found
if data["elements"]:
    # Initialize a list to store the distances and ids of the charging stations
    distances = []

    # Loop through the charging stations
    for element in data["elements"]:
        # Get the coordinates of the charging station from the data
        station_lat = element["lat"]
        station_lon = element["lon"]

        # Calculate the distance from the current location using the haversine formula
        # Assuming the earth's radius is 6371 km
        dlat = (station_lat - lat) * math.pi / 180  # Convert to radians
        dlon = (station_lon - lon) * math.pi / 180  # Convert to radians
        a = (math.sin(dlat / 2))**2 + math.cos(lat * math.pi / 180) * \
            math.cos(station_lat * math.pi / 180) * (math.sin(dlon / 2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = 6371 * c  # Distance in km

        # Append the distance and id to the list
        distances.append((d, element["id"]))

    # Sort the list by distance
    distances.sort()

    # Print the number of charging stations found
    print(f"{len(distances)} charging stations are found within 10 km radius of your current location")

    # Loop through the sorted list
    for i, (distance, station_id) in enumerate(distances):
        # Find the element with the station id
        for element in data["elements"]:
            if element["id"] == station_id:
                # Print the details of the charging station
                print(
                    f"{i+1}. {element['tags'].get('name', 'unknown')} at {element['lat']}, {element['lon']}")
                print(
                    f"   It is {distance:.2f} km away from your current location")
                print(
                    f"   It has {element['tags'].get('capacity', 'unknown')} charging points")
                print(
                    f"   It supports {element['tags'].get('socket', 'unknown')} socket type")
                lats.append(element['lat'])
                lons.append(element['lon'])
                break
else:
    print("Sorry, no charging stations are found within the radius of your current location")


def plot_points(latitudes, longitudes, current_lat, current_lon):
    map_osm = folium.Map(location=[current_lat, current_lon], zoom_start=12)

    folium.Marker(location=[current_lat, current_lon],
                  popup='Your Location', icon=folium.Icon(color='red')).add_to(map_osm)

    for lat, lon in zip(latitudes, longitudes):
        folium.Marker(location=[lat, lon],
                      popup='Charging Station').add_to(map_osm)

    map_osm.save('map.html')

    import webbrowser
    webbrowser.open('map.html')


plot_points(lats, lons, lat, lon)

elementid = int(input("please enter which station you want to select: "))
elementid = elementid - 1

if len(distances) >= elementid:
    # Get the tuple at index elementid (since indexing starts from 0)
    selected_element = distances[elementid]

    # Extract the latitude and longitude from the tuple
    element_distance, element_station_id = selected_element
    for element in data["elements"]:
        if element["id"] == element_station_id:
            element_lat = element["lat"]
            element_lon = element["lon"]
            print(f"The latitude of the 6th element is {element_lat}")
            print(f"The longitude of the 6th element is {element_lon}")
            break
else:
    print("There are fewer than 6 elements in the distances list.")


def generate_and_display_google_maps_qr(latitude, longitude):
    # Construct the Google Maps URL
    google_maps_url = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'

    # Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(google_maps_url)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Display the QR code
    plt.imshow(qr_image, cmap='gray')
    plt.axis('off')
    plt.show()

    # Save the QR code image
    qr_image.save("google_maps_location_qr.png")

    print("QR code generated and displayed successfully!")


generate_and_display_google_maps_qr(element_lat, element_lon)
