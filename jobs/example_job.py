#!/usr/bin/env python
# encoding: utf-8

import logging
import time
from datetime import datetime

job = None


def schedule_job(schedule):
    global job
    job = schedule.every().minute.at(":00").do(do_example)
    logging.info("schedule_job: %s", __name__)


def cancel_job(schedule):
    global job
    if job is not None:
        schedule.cancel_job(job)
        logging.info("cancel_job: %s", __name__)


def do_example():
    logging.info("%s", time.ctime())
