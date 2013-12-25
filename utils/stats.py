#!/usr/bin/env python
# Copyright (C) 2010-2013 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os.path
import sys
import time

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.cuckoo.core.database import Database, TASK_PENDING, TASK_RUNNING
from lib.cuckoo.core.database import TASK_COMPLETED, TASK_RECOVERED
from lib.cuckoo.core.database import TASK_REPORTED, TASK_FAILED_ANALYSIS
from lib.cuckoo.core.database import TASK_FAILED_PROCESSING


def timestamp(dt):
    """Returns the timestamp of a datetime object."""
    return time.mktime(dt.timetuple())


if __name__ == '__main__':
    db = Database()

    print db.count_samples(), 'samples in db'
    print db.count_tasks(), 'tasks in db'

    states = (
        TASK_PENDING, TASK_RUNNING,
        TASK_COMPLETED, TASK_RECOVERED, TASK_REPORTED,
        TASK_FAILED_ANALYSIS, TASK_FAILED_PROCESSING,
    )

    for state in states:
        count = db.count_tasks(state)
        print state, count, 'tasks'

    # Later on we might be interested in only calculating stats for all
    # tasks starting at a certain offset, because the Cuckoo daemon may
    # have been restarted at some point in time.
    offset = None

    # For the following stats we're only interested in completed tasks.
    tasks = db.list_tasks(offset=offset, status=TASK_COMPLETED)
    tasks += db.list_tasks(offset=offset, status=TASK_REPORTED)

    # Get the time when the first task started.
    started = min(timestamp(_.started_on) for _ in tasks)

    # Get the time when the last task completed.
    completed = max(timestamp(_.completed_on) for _ in tasks)

    # Get the amount of tasks that actually completed.
    finished = len(tasks)

    hourly = 60 * 60 * finished / (completed - started)

    print 'roughly', int(hourly), 'tasks an hour'
    print 'roughly', int(24 * hourly), 'tasks a day'