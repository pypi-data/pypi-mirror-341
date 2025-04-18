#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2025 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""""""

import time
from logging.handlers import RotatingFileHandler

from condor_log_utils.JobLog import ClusterLogFile

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import sys
import traceback

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-o', '--out-base', type=Path,
                        help='output file base, anything after a dsot is ignored. eg: ./out/analyzer.xxx '
                             'will produce: ./out/analyzer.log and analyzer.csv. If not set all '
                             'output goes to STDOUT and STDERR')
    parser.add_argument('files', nargs='*', type=Path, help='files to analyze')


def main():
    global logger

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)

    log_formatter = logging.Formatter(fmt=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser)
    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    out_csvfile = None
    if args.out_base:
        out_base = args.out_base.parent
        out_name = args.out_base.name
        out_name = re.sub(Path(out_name).suffix, '', out_name)
        log_file = out_base / (out_name + '.logger')
        out_csvfile = out_base / (out_name + '.csv')

        logfile = log_file
        logfile.parent.mkdir(parents=True, exist_ok=True)
        log_file_handler = RotatingFileHandler(logfile, maxBytes=10 ** 7, backupCount=5)
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    file: Path
    for file in args.files:
        logger.debug(f'Processing: {file}')
        if not file.exists():
            logger.error(f'File does not exist: {file}')
            continue

        cluster_log = ClusterLogFile(file.absolute(), logger=logger)
        cluster_log.process_log()
        cluster_log.print(out_csvfile)

    if out_csvfile:
        logger.info(f' CSV written to {out_csvfile}')
        logger.info(f' LOG written to: {log_file}')


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
