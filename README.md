---

# Nearest Charging Station Finder

Hi there! I'm Faizan, and this program helps you find the nearest charging station to your current location. It utilizes simple libraries to determine your current location and then queries the OpenStreetMap (OSM) API, specifically the Overpass API, to find the nearest charging station.

## Installation

Before using this program, you'll need to install the required Python libraries. You can do this by running the following commands in your command prompt:

```
pip install geocoder
pip install overpass
pip install matplotlib
pip install cartopy
```

## References

I relied on several resources to develop this program:

- [Overpass API Documentation](https://wiki.openstreetmap.org/wiki/Overpass_API#Quick_Start_(60_seconds):_Interactive_UI)
- [Overpass API Quick Start Guide](https://readthedocs.org/projects/python-overpy/downloads/pdf/latest/)
- [Tutorial on Writing Queries for Overpass API](https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0)
- [Geocoding with Geopy](https://github.com/geopy/geopy)
- [Haversine Formula for Calculating Distances](https://en.wikipedia.org/wiki/Haversine_formula)

## Usage

1. Run the program.
2. Enter the range in kilometers within which you want to search for charging stations.
3. The program will determine your current location automatically.
4. It will then search for charging stations within the specified range using the Overpass API.
5. Finally, it will display the nearest charging station(s) along with relevant details and plot them on a map.


---
