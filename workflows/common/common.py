#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import os
from configparser import ConfigParser

logger = logging.getLogger('workflows')

def getConf():
    logger.info('%s.getConf starts', __name__)

    currentPath = os.path.dirname(os.path.abspath(__file__))
    app_dir = currentPath + '/../..'
    cfg = ConfigParser()
    confPath = app_dir + '/conf/synapse.conf'
    try:
        cfg.read(confPath)
        #username = os.environ.get('EWS_USERNAME', cfg.set('EWS', 'username'))
        #password = os.environ.get('EWS_PASSWORD', self.cfg.get('EWS', 'password'))
        #authType = os.environ.get('EWS_AUTH_TYPE', self.cfg.get('EWS', 'auth_type'))
        #ews_server = os.environ.get('EWS_SERVER', self.cfg.get('EWS', 'server'))
        #smtp_address = os.environ.get('EWS_SMTP_ADDRESS', self.cfg.get('EWS', 'smtp_address'))
        logger.info('Config: {}'.format(cfg))
        return cfg
    except Exception as e:
        logger.error('%s', __name__, exc_info=True)

