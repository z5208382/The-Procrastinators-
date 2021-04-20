import re
import signal
from subprocess import PIPE, Popen
from time import sleep
import threading

import pytest


@pytest.fixture
def url():
    '''
    # Use this fixture to get the URL of the server. It starts the server for you,
    # so you don't need to.
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


@pytest.fixture(autouse=True)
def thread_one():
    '''
    Block until all but one thread exited, before each test
    '''
    # Use this if you want to see which test function
    # does not wait for threads to finish
    # t_count = len(threading.enumerate())
    # assert t_count == 1
    while len(threading.enumerate()) > 1:
        pass
