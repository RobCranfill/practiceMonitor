# test of adafruit iot lib
# robcranfill
# sys.arg[1] must be Adafruit AIO API key

import json
import random
import sys
import time

from Adafruit_IO import Client


if len(sys.argv) != 2:
    print("Must provide API key!")
    sys.exit(1)
api_key = sys.argv[1]

# This works for a feed in the "Default" group
FEED_NAME = "perfdata"
# How is this name supposed to be formatted? neither "/" nor "." work.
# FEED_NAME = "PracticeMonitor.perfdata"
# Perhaps all lower case would have worked. Not sure I want to use a group anyway.
#
# >>> from Adafruit_IO import Client
# >>> aio = Client("robcranfill", "XXX")
# >>> f = aio.feeds()
# >>> f
# [Feed(name='perfdata', key='perfdata', id=2660025, description='Feed for PerformanceMonitor project.', 
# unit_type=None, unit_symbol=None, history=True, visibility='private', license=None, status_notify=False, 
# status_timeout=4320), Feed(name='perfdata', key='practicemonitor.perfdata', id=2660022, description='', 
# unit_type=None, unit_symbol=None, history=True, visibility='private', license=None, status_notify=False, 
# status_timeout=4320)]
#


# not really what we want anymore
def generate_old_test_data():
    result = []
    t_start = time.time()
    print(f"sess#\tstart\tdur (sec)")
    for i in range(10):
        t_duration = random.randint(60, 600)
        record = f"{i}\t{time.ctime(t_start)}\t{t_duration}"
        print(record)
        t_start += t_duration + random.randint(600, 1200)
        result.append(record)
    return result

# As per main code. Refactor?
JSON_KEY_TS     = "SeshNumber"
JSON_KEY_START  = "SeshStart"
JSON_KEY_END    = "SeshEnd"
JSON_KEY_NOTES  = "SeshNotes"

def format_as_json(total_sessions, session_start_sec, session_end_sec, session_notes):

    one_record = [{ JSON_KEY_TS:    total_sessions,
                    JSON_KEY_START: time.ctime(session_start_sec),
                    JSON_KEY_END:   time.ctime(session_end_sec),
                    JSON_KEY_NOTES: session_notes
                    }]
    return json.dumps(one_record)


# create some semi-random session data
# return a list of JSON strings: the data
def generate_json_test_data():

    result = []
    t_start = time.time()
    print(f"sess#\tstart\tdur (sec)")
    for i in range(random.randint(5, 15)): # 5-15 sessions

        t_duration = random.randint(60, 600)
        t_start += t_duration + random.randint(600, 1200)

        json = format_as_json(i, t_start, t_start + t_duration, random.randint(1000, 10000))
        # print(json)
        result.append(json)
        
    return result


def send_data(api_key, data):
    try:
        aio = Client("robcranfill", api_key)
        print("client OK")

        for d in data:
            aio.send(FEED_NAME, d)
        print("send OK")

    except Exception as e:
        print(e)
        print("Bummer!")


# d = generate_old_test_data()
d = generate_json_test_data()
print(f"{len(d)} data points:\n{d}")

send_data(api_key, d)
