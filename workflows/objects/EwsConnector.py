#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import os
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM

class EwsConnector:
    'Exchange web service connector'

    def __init__(self, cfg):
        self.logger = logging.getLogger('workflows.' + __name__)
        self.cfg = cfg
        self.account = self.getAccount()

    def getAccount(self):
        self.logger.info('%s. getAccount starts', __name__)
        try:
            username = os.environ.get('EWS_USERNAME', self.cfg.get('EWS', 'username'))
            password = os.environ.get('EWS_PASSWORD', self.cfg.get('EWS', 'password'))
            authType = os.environ.get('EWS_AUTH_TYPE', self.cfg.get('EWS', 'auth_type'))
            credentials = Credentials(username=username, password=password)

            ews_server = os.environ.get('EWS_SERVER', self.cfg.get('EWS', 'server'))
            smtp_address = os.environ.get('EWS_SMTP_ADDRESS', self.cfg.get('EWS', 'smtp_address'))

            self.logger.debug('EWS, server: {}, username: {}, authtype: {}, smtp address: {}'.format(ews_server, username, authType, smtp_address))
 
            if authType == 'NTLM':
                config = Configuration(server=ews_server,
                    credentials=credentials,
                    auth_type=NTLM)
            elif authType == 'None':
                #O365 does not use NTLM auth
                config = Configuration(server=ews_server,
                    credentials=credentials,
                    auth_type=None)
            else:
                raise ValueError(authType)

            account = Account(primary_smtp_address=smtp_address,
                config=config, autodiscover=False, access_type=DELEGATE)

            return account
        except ValueError:
            self.logger.error('authType not supported: %s', authType)
            raise
        except Exception as e:
            self.logger.error('Failed to get account', exc_info=True)
            raise


    def scan(self, folderName):
        #returns a query set of unread emails
        #<class 'exchangelib.queryset.QuerySet'>

        self.logger.info('%s.scan starts', __name__)

        folder = None
        try:
            #get the folder first
            if folderName == 'inbox':
                folder = self.account.inbox
            else:
                for f in self.account.root.walk():
                    if f.name == folderName:
                        folder = f

            if folder is None:
                raise ValueError('folder %s not found', folderName)

            unread = folder.filter(is_read = False)

            return unread

        except Exception as e:
            self.logger.error('Failed to get unread emails', __name__, exc_info = True)
            raise

    def markAsRead(self, msg):
        self.logger.info('%s.markAsRead starts', __name__)
        msg.is_read = True
        msg.save()
        return msg
