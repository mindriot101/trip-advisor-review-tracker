#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import argparse


def format_label(label):
    return label.lower().replace(' ', '_')


def format_value(value):
    return int(value.replace(',', ''))


def parse_hotel(soup):
    chart = soup.find('div', id='ratingFilter')

    results = {}

    for li in chart.ul.find_all('li'):
        label = format_label(li.find('div').text)
        rating = format_value(li.find_all('span')[-2].text)

        results[label] = rating

    return results


def parse_attraction(soup):
    chart = soup.find('div', class_='visitorRating')

    results = {}
    for li in chart.ul.find_all('li'):
        label = format_label(li.find('div', class_='label').text)
        rating = format_value(li.find('div', class_='valueCount').text)
        results[label] = rating

    return results

PARSE_FUNCTIONS = {
    'hotel': parse_hotel,
    'attraction': parse_attraction,
}


def fetch_reviews(url, kind):
    r = requests.get(url)
    r.raise_for_status()

    html_text = r.text
    soup = BeautifulSoup(html_text, 'html.parser')

    return PARSE_FUNCTIONS[kind](soup)


def format_results(results):
    order = ['excellent', 'very_good', 'average', 'poor', 'terrible']
    keys = ['{name}:{value}'.format(name=name, value=results[name])
            for name in order]

    return ','.join(keys)


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-k', '--kind', required=True,
                        choices=['hotel', 'attraction'])
    args = parser.parse_args()

    results = fetch_reviews(args.url, kind=args.kind)
    print(format_results(results))
