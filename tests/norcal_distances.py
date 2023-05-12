# This Python file uses the following encoding: utf-8
#
# Copyright 2016 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Tests for the places module."""

import uuid

from types import GeneratorType

import responses

import googlemaps

import pprint

# from __init__ import TestCase

import __init__

# import unittest
# import codecs

# from urllib.parse import urlparse, parse_qsl

# class TestCase(unittest.TestCase):
#     def assertURLEqual(self, first, second, msg=None):
#         """Check that two arguments are equivalent URLs. Ignores the order of
#         query arguments.
#         """
#         first_parsed = urlparse(first)
#         second_parsed = urlparse(second)
#         self.assertEqual(first_parsed[:3], second_parsed[:3], msg)

#         first_qsl = sorted(parse_qsl(first_parsed.query))
#         second_qsl = sorted(parse_qsl(second_parsed.query))
#         self.assertEqual(first_qsl, second_qsl, msg)

#     def u(self, string):
#         """Create a unicode string, compatible across all versions of Python."""
#         # NOTE(cbro): Python 3-3.2 does not have the u'' syntax.
#         return codecs.unicode_escape_decode(string)[0]


# tests = TestCase() 
class PlacesTest(__init__.TestCase):
    def setUp(self):
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        self.location = (37.804363, -122.271111)
        self.type = "cities"
        self.language = "en"
        self.region = "US"
        self.radius = 100000

    @responses.activate
    def test_places_find(self):
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "candidates": []}',
            status=200,
            content_type="application/json",
        )

        results_dic=self.client.find_place(
            "cities",
            "textquery",
            fields=["business_status", "geometry/location", "place_id"],
            location_bias="point:90,90",
            language=self.language,
        )

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results_dic)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?language=en-AU&inputtype=textquery&"
            "locationbias=point:90,90&input=restaurant"
            "&fields=business_status,geometry/location,place_id&key=%s"
            % (url, self.key),
            responses.calls[0].request.url,
        )

        with self.assertRaises(ValueError):
            self.client.find_place("restaurant", "invalid")
        with self.assertRaises(ValueError):
            self.client.find_place(
                "restaurant", "textquery", fields=["geometry", "invalid"]
            )
        with self.assertRaises(ValueError):
            self.client.find_place("restaurant", "textquery", location_bias="invalid")

    @responses.activate
    def test_places_text_search(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "results": [], "html_attributions": []}',
            status=200,
            content_type="application/json",
        )

        self.client.places(
            "cities",
            location=self.location,
            radius=self.radius,
            region=self.region,
            language=self.language,
            type=self.type,
        )

        # pprint(responses.calls[0].url)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?language=en-AU&location=-33.86746%%2C151.20709&"
            "query=cities&"
            "radius=100&region=AU&type=cities&key=%s" % (url, self.key),
            responses.calls[0].request.url,
        )

    @responses.activate
    def test_places_nearby_search(self):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "results": [], "html_attributions": []}',
            status=200,
            content_type="application/json",
        )

        results_dic=self.client.places_nearby(
            location=self.location,
            region=self.region,
            # keyword="foo",
            # language=self.language,
            name="cities",
            # open_now=True,
            # rank_by="distance",
            radius=self.radius,
            type=self.type,
        )

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results_dic)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            responses.calls[0].request.url,
        )

        with self.assertRaises(ValueError):
            self.client.places_nearby(radius=self.radius)
        with self.assertRaises(ValueError):
            self.client.places_nearby(self.location, rank_by="distance")

        with self.assertRaises(ValueError):
            self.client.places_nearby(
                location=self.location,
                rank_by="distance",
                keyword="foo",
                radius=self.radius,
            )

    @responses.activate
    def test_place_detail(self):
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "result": {}, "html_attributions": []}',
            status=200,
            content_type="application/json",
        )

        self.client.place(
            "ChIJN1t_tDeuEmsRUsoyG83frY4",
            fields=["business_status", "geometry/location",
                    "place_id", "reviews"],
            language=self.language,
            reviews_no_translations=True,
            reviews_sort="newest",
        )

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?language=en-AU&placeid=ChIJN1t_tDeuEmsRUsoyG83frY4"
            "&reviews_no_translations=true&reviews_sort=newest"
            "&key=%s&fields=business_status,geometry/location,place_id,reviews"
            % (url, self.key),
            responses.calls[0].request.url,
        )

        with self.assertRaises(ValueError):
            self.client.place(
                "ChIJN1t_tDeuEmsRUsoyG83frY4", fields=["geometry", "invalid"]
            )

    @responses.activate
    def test_photo(self):
        url = "https://maps.googleapis.com/maps/api/place/photo"
        responses.add(responses.GET, url, status=200)

        ref = "CnRvAAAAwMpdHeWlXl-lH0vp7lez4znKPIWSWvgvZFISdKx45AwJVP1Qp37YOrH7sqHMJ8C-vBDC546decipPHchJhHZL94RcTUfPa1jWzo-rSHaTlbNtjh-N68RkcToUCuY9v2HNpo5mziqkir37WU8FJEqVBIQ4k938TI3e7bf8xq-uwDZcxoUbO_ZJzPxremiQurAYzCTwRhE_V0"
        response = self.client.places_photo(ref, max_width=100)

        self.assertTrue(isinstance(response, GeneratorType))
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?maxwidth=100&photoreference=%s&key=%s" % (url, ref, self.key),
            responses.calls[0].request.url,
        )

    @responses.activate
    def test_autocomplete(self):
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "predictions": []}',
            status=200,
            content_type="application/json",
        )

        session_token = uuid.uuid4().hex

        results_dic=self.client.places_autocomplete(
            "Oakland, CA",
            session_token=session_token,
            # offset=3,
            # origin=self.location,
            location=self.location,
            radius=self.radius,
            # language=self.language,
            types="restaurant",
            # components={"country": "us"},
            # strict_bounds=True,
        )

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results_dic)

        # self.assertEqual(1, len(responses.calls))
        # self.assertURLEqual(
        #     "%s?components=country%%3Aau&input=Google&language=en-AU&"
        #     "origin=-33.86746%%2C151.20709&"
        #     "location=-33.86746%%2C151.20709&offset=3&radius=100&"
        #     "strictbounds=true&types=geocode&key=%s&sessiontoken=%s"
        #     % (url, self.key, session_token),
        #     responses.calls[0].request.url,
        # )

    @responses.activate
    def test_autocomplete_query(self):
        url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json"
        responses.add(
            responses.GET,
            url,
            body='{"status": "OK", "predictions": []}',
            status=200,
            content_type="application/json",
        )

        self.client.places_autocomplete_query("pizza near New York")

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?input=pizza+near+New+York&key=%s" % (url, self.key),
            responses.calls[0].request.url,
        )


foo=PlacesTest()
foo.setUp()
# foo.test_places_text_search()
# foo.test_places_nearby_search()
# foo.test_places_find()
foo.test_autocomplete()