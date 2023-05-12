from datetime import datetime
import time

import csv
import pprint

import responses

import googlemaps



# csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
# cal_cities = []
# state=", CA, USA"
# with open(csv_file_path, 'r') as file:
#     csvreader=csv.reader(file)
#     for row in csvreader:
# 	    cal_cities.append(row[1]+state)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(cal_cities)

class DistanceMatrixTest():


    def setUp(self):
        csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
        cal_cities = []
        state=", USA"
        with open(csv_file_path, 'r') as file:
            csvreader=csv.reader(file)
            for row in csvreader:
    	        cal_cities.append(row[1]+state)	
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        self.cal_cities = cal_cities
        # print(cal_cities)

        attractive_centers = [
			"San Francisco, USA",
			"Berkeley, USA",
			"Sacramento, USA"
			# "Napa",
			# "Sonoma",
			# "San Mateo",
			# "Palo Alto"
		]
        self.attractive_centers = attractive_centers
    @responses.activate
    def test_basic_params(self):
        responses.add(
            responses.GET,
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            body='{"status":"OK","rows":[]}',
            status=200,
            content_type="application/json",
        )

        # csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
        # cal_cities = []
        # state=" CA, USA"
        # with open(csv_file_path, 'r') as file:
    	#     csvreader=csv.reader(file)
    	#     for row in csvreader:
    	# 	    cal_cities.append(row[1])

        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(self.cal_cities)
        origins = self.cal_cities
        pp.pprint(self.attractive_centers)
        destinations = self.attractive_centers
        # pp.pprint(destinations)

        matrix = self.client.distance_matrix(self.cal_cities[1:10], self.attractive_centers)

        pp.pprint(matrix)
        pp.pprint(responses.calls[0].request.url)

        # self.assertEqual(1, len(responses.calls))
        # self.assertURLEqual(
        #     "https://maps.googleapis.com/maps/api/distancematrix/json?"
        #     "key=%s&origins=Perth%%2C+Australia%%7CSydney%%2C+"
        #     "Australia%%7CMelbourne%%2C+Australia%%7CAdelaide%%2C+"
        #     "Australia%%7CBrisbane%%2C+Australia%%7CDarwin%%2C+"
        #     "Australia%%7CHobart%%2C+Australia%%7CCanberra%%2C+Australia&"
        #     "destinations=Uluru%%2C+Australia%%7CKakadu%%2C+Australia%%7C"
        #     "Blue+Mountains%%2C+Australia%%7CBungle+Bungles%%2C+Australia"
        #     "%%7CThe+Pinnacles%%2C+Australia" % self.key,
        #     responses.calls[0].request.url,
        # )


foo = DistanceMatrixTest()
foo.setUp()
foo.test_basic_params()
