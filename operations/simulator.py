import requests
import json
import csv
from flask import Flask, url_for

# CONSTANTS
UNITS = "imperial"
GOOGLE_KEY = "AIzaSyBHrVBxy2f98hXD0iudseZCV1GXUXdiz0k"


# This function returns the distance in miles separating the two cities, or None if an error occurs
def get_distance(city1, city2):

    # set the distance variable
    distance = None

    # check if distance has already been calculated
    with open("/Users/ep24/Desktop/code/aa-projects/aa-html/first-website/static/storage/distance_storage.csv", "r") as distance_file:
        reader = csv.DictReader(distance_file)
        for row in reader:
            if (row["origin"] == city1 and row["destination"] == city2) or (row["origin"] == city2 and row["destination"] == city1):
                distance = row["distance (mi)"]
        if distance:
            return distance

        # if distance has not been previously calculated, we'll do that now
        else:
            google_origin = str(city1) + "airport"
            google_dest = f"{city2} airport"
            google_api_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={google_origin}&destinations={google_dest}&units={UNITS}&key={GOOGLE_KEY}"
            payload = {}
            headers = {}
            response = requests.request("GET", google_api_url, headers=headers, data=payload)
            data = json.loads(response.text)

            # we'll make sure that no error is thrown by google API
            if "distance" in data["rows"][0]["elements"][0]:
                text = data["rows"][0]["elements"][0]["distance"]["text"]
                distance = int(text.split()[0].replace(",", ""))

                # then add this calculation to our storage
                with open("/Users/ep24/Desktop/code/aa-projects/aa-html/first-website/static/storage/distance_storage.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([city1, city2, distance])
                return distance

            # if google API threw an error, we'll return None
            else:
                return None


def whats_close(origin, max_distance):
    # this will be the list of airports that are within driving range
    within_range = []

    # this opens the list of AA airport codes in the USA
    with open("/Users/ep24/Desktop/code/aa-projects/aa-html/first-website/static/storage/aa_airport_list_usa.csv", "r") as file:
        airport_list = csv.reader(file)
        for row in airport_list:
            city_pair = (origin, row[0])
            result = get_distance(*city_pair)
            if result is None:
                pass
            elif (int(result) < int(max_distance)) and origin != row[0]:
                within_range.append(row[0])
            else:
                pass
    return within_range