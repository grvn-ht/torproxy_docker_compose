# -*- coding: utf-8 -*-

import requests
from stem import Signal
from stem.control import Controller
import time
import logging
from logging.handlers import WatchedFileHandler
import os


class over_control(Controller):
  @staticmethod
  def from_port(address = '127.0.0.1', port = 'default'):
    import stem.connection
    control_port = stem.socket.ControlPort(address, port)

    return Controller(control_port)

if os.name == 'nt':
    log_path = os.path.dirname(os.path.realpath(__file__))+'\\py_log.log'
    host = "localhost"
else:
    log_path = "/var/log/py/py_log.log"
    host = 'tor'

def renew_tor_ip():
    with over_control.from_port(address = host, port = 9051) as controller:
        controller.authenticate(password="admin")
        controller.signal(Signal.NEWNYM)
        controller.close()

def do_req(logg):
    with requests.Session() as session:
        session.proxies = {}
        session.proxies['http'] = 'socks5://'+host+':9050' #9150 for browser; 9050 for TOR service
        session.proxies['https'] = 'socks5://'+host+':9050'
    
    r = session.get('http://icanhazip.com/')
    ip = r.content
    print(ip)
    logg.info(ip)
    renew_tor_ip()

try:
    handler = WatchedFileHandler(log_path, mode="a", encoding="utf-8")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    for  i in range(3):    
        do_req(logger)
        time.sleep(5)
except Exception as error:
    logger.exception(error)
finally:
    logger.info('-----------------------------------')
    for i in range(len(logger.handlers)):
        logger.handlers[0].close()
        logger.removeHandler(logger.handlers[0])
