# pylint: disable=unused-argument
"""
RECEIVING END
Testing part
When received, use regExp to get CODE
https://pymotw.com/2/smtpd/

Unused argument disabled, process_message needs mail and rcpt options to work
"""
import smtpd
import asyncore
import threading
import time
import re

def timer(server, delta):
    '''
    Timeout function. Closes server after delta seconds
    '''
    time.sleep(delta)
    server.close()


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        self.body = data.decode('utf-8')
        self.close()


def runner(delta):
    '''
    Runs the mail server on 127.0.0.1:1025
    Ready to receive email
    Mail server is immediately closed after receiving an email
    If timer expire with no code, generic exception is raised
    Otherwise, it will parse the email received and only return the code
    '''
    server = CustomSMTPServer(('127.0.0.1', 1025), None)
    server.body = None
    thread = threading.Thread(target=timer, args=(server, delta), daemon=True)
    thread.start()
    asyncore.loop(0)
    if server.body is not None:
        parsed = server.body.split('\n')
        code = re.match(r'CODE: (.*)', parsed[-1]).group(1)
        return code
    else:
        raise Exception("No code received")


if __name__ == '__main__':
    runner(3)
