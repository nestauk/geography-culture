#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script matches venue strings / locations to FourSquare IDs and retrieves venues details from the FourSquare API.

"""

import csv
import json
import sys

import click
import requests
import ratelim
import tqdm

from urllib.parse import urljoin

BASE_URL = "https://api.foursquare.com/v2/"

class FoursquareAPI(object):
    search_url = urljoin(BASE_URL, "venues/search")
    venue_url = urljoin(BASE_URL, "venues/{}")

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _build_arguments(self, arguments):
        base_arguments = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'v': '20160823',
        }
        base_arguments.update(arguments)
        return base_arguments

    @ratelim.patient(4500, 3600)
    def _get(self, endpoint, arguments):
        resp = requests.get(endpoint,
                            params=self._build_arguments(arguments))
        return resp

    def search(self, **arguments):
        return self._get(self.search_url, arguments)

    def venue(self, venue_id):
        url = self.venue_url.format(venue_id)
        return self._get(url, {})

@click.command()
@click.option('--client_id', envvar="FSQ_ID")
@click.option('--client_secret', envvar="FSQ_SECRET")
@click.option('--infile', default=sys.stdin, type=click.File('r'))
@click.option('--outfile', default=sys.stdout)
def main(client_id, client_secret, infile, outfile):
    """
    It accepts as input a no-header csvfile of three fields: name,latitude,longitude. For example:

        British Museum,44.5,0.15
        ...

    If the latitude/longitude is 0,0 it will perform a global search

    """
    assert client_id
    assert client_secret
    api = FoursquareAPI(client_id, client_secret)
    reader = csv.reader(infile)
    with tqdm.tqdm() as pbar:
        for name, lat, lon in reader:
            pbar.update(1)
            for _ in range(10):
                try:
                    if lat == "0" and lon == "0":
                        result = api.search(query=name, intent='global', ll="{},{}".format(lat, lon)).json()
                    else:
                        result = api.search(query=name, intent='match', ll="{},{}".format(lat, lon)).json()
                        if len(result['response']['venues']) == 0:
                            result = api.search(query=name, intent='checkin', ll="{},{}".format(lat, lon)).json()
                except (KeyError, requests.exceptions.RequestException):
                    pass
                break
            try:
                venue = result['response']['venues'][0]
                venue_details = api.venue(venue['id']).json()
            except (KeyError, IndexError):
                venue_details = {}
            print(json.dumps(venue_details))


if __name__ == "__main__":
    main()
