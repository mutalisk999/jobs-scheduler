#!/usr/bin/env python
# encoding: utf-8

import schedule
import time
import os
import logging
import importlib
import glob

job_register = dict()


def start_schedule():
    global job_register

    while True:
        # register job
        job_active_round = set()
        for abs_name in glob.glob("jobs/*"):
            basename = os.path.basename(abs_name)
            if basename not in (['__init__.py', '__pycache__']):
                if not basename.endswith(".py"):
                    continue
                modname = 'jobs.' + basename.rstrip(".py")
                if modname in job_register.keys():
                    job_active_round.add(modname)
                    continue
                mod = importlib.import_module(modname)
                if getattr(mod, 'schedule_job', None) is not None \
                        and getattr(mod, 'cancel_job', None) is not None:
                    mod.schedule_job(schedule)
                    job_active_round.add(modname)
                    job_register[modname] = mod
                else:
                    logging.warning("modname: %s has no function named schedule_job or cancel_job" % modname)

        # cancel job
        need_cancel = set()
        for j in job_register:
            if j not in job_active_round:
                job_register[j].cancel_job(schedule)
                need_cancel.add(j)
        for j in need_cancel:
            del job_register[j]

        # run job
        schedule.run_pending()

        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    start_schedule()
