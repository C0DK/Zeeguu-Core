#!/usr/bin/env python3


import logging

logger = logging.getLogger(__name__)

def info(msg):
    logger.info(msg)

def debug(msg):
    logger.debug(msg)


def log(msg):
    info(msg)


def warning(msg):
    logger.warning(msg)


def critical(msg):
    logger.critical(msg)


def logp(msg):
    log(msg)
    print(msg)
