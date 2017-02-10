#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import logging
import glob
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import namedtuple
import numpy as np
import datetime

logging.basicConfig(
    level='INFO', format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)

plt.style.use(['seaborn-talk'])

class SourceFile(object):

    score_headings = ['excellent', 'very_good', 'average', 'poor', 'terrible']
    score_values = [5, 2, 0, -2, -5]

    def __init__(self, name, filename):
        self.filename = filename
        self.name = name
        self.timestamps = []

    def parse(self):
        scores = []
        with open(self.filename) as infile:
            for line in infile:
                line = line.strip()
                contents = line.split()
                timestamp = int(contents[0])

                upload_data = {
                    part.split(':')[0]: int(part.split(':')[1])
                    for part in contents[1:]
                }

                row = [timestamp] + [upload_data[heading]
                                     for heading in self.score_headings]
                scores.append(tuple(row))

        dtype = [('timestamp', int)] + \
            list(zip(self.score_headings, [int] * len(self.score_headings)))
        return np.array(scores, dtype=dtype)

    def render_to(self, name, filename):
        data = self.parse()

        totals = []
        for row in data:
            totals.append(np.sum([row[heading] for heading in self.score_headings]))
        totals = np.array(totals)

        dates = np.array([
            datetime.datetime.fromtimestamp(value)
            for value in data['timestamp']
        ])

        ratings = []
        for row in data:
            ratings.append(
                sum(row[heading] * score for (heading, score) in
                    zip(self.score_headings, self.score_values))
            )
        ratings = np.array(ratings)
        self.plot_ratings = (dates, ratings / totals)

        fig, axes = plt.subplots(2, 1, sharex=True)
        axes[0].plot(self.plot_ratings[0], self.plot_ratings[1], 'o', ls='-', drawstyle='steps-mid')

        for typ in self.score_headings:
            axes[1].plot(dates, data[typ] - data[typ].min(), 'o', ls='-',
                         label=typ, drawstyle='steps-mid')

        axes[1].legend(loc='best')

        axes[0].set(title=name, ylabel='Rating')
        axes[1].set(ylabel=r'$\Delta$ score', xlabel='Date')

        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(filename)


def main(args):
    if args.verbose:
        logger.setLevel('DEBUG')
    logger.debug(args)

    files = glob.iglob('score_*.txt')

    mapping = []
    for filename in files:
        output_filename = os.path.splitext(filename)[0] + '.png'
        logger.info('Rendering %s to %s', filename, output_filename)

        name = (os.path.splitext(filename)[0]
                .replace('score_', '')
                .replace('_', ' ')
                .capitalize())

        s = SourceFile(name, filename)

        s.render_to(name, output_filename)

        mapping.append((name, s.plot_ratings))

    fig, axis = plt.subplots()
    for name, (x, y) in mapping:
        axis.plot(x, y, drawstyle='steps-mid', marker='.', label=name)

    axis.legend(loc='best')
    axis.set(ylabel='Rating', xlabel='Date')
    fig.savefig('score_comparison.png')
    plt.close(fig)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    main(parser.parse_args())
