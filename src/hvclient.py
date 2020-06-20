import hvac
import os
import sys
import json
import logging

class HvClient(object):
    def __init__(self, configpath: object = None) -> object:
        self.configpath = configpath
    def newClient(self) -> object:
        if self.configpath != None:
            logging.info('Found the vault config file in {cfg}'.format(cfg=self.configpath))
            config = open(self.configpath, 'r')
            jsonconfig = json.load(config)
            url, token = jsonconfig['url'], jsonconfig['auth_token']
            client_cert = jsonconfig.get('certpath', 'NotFound')
            client_key = jsonconfig.get('keypath', 'NotFound')
            server_cert_path = jsonconfig.get('server_cert_path', 'NotFound')
        elif os.path.exists(os.path.expanduser("~") + '/hvac.json'):
            logging.info('Found the vault config file in {path}'.format(path=os.path.expanduser("~") + '/hvac.json'))
            config = open(os.path.expanduser("~") + '/hvac.json', 'r')
            jsonconfig = json.load(config)
            url, token = jsonconfig['url'], jsonconfig['auth_token']
            client_cert = jsonconfig.get('certpath', 'NotFound')
            client_key = jsonconfig.get('keypath', 'NotFound')
            server_cert_path = jsonconfig.get('server_cert_path', 'NotFound')
        else:
            logging.info('File not found in {path} checking the env vars now'.format(path=self.configpath))
            try:
                url, token, client_cert, client_key, server_cert_path = os.environ['VAULT_HOST'], os.environ['VAULT_TOKEN'], os.environ['VAULT_CERT'], os.environ['VAULT_KEY'], os.environ['SERVER_CERT_PATH']
                logging.info('Environment variables needed to connect to the cluster is fetched')
            except KeyError:
                logging.error('Error encountered {err}'.format(err=str(KeyError)))
                sys.exc_clear()
        logging.info("client_cert: {certfile}".format(certfile=client_cert))
        if os.path.exists(client_cert) and os.path.exists(client_key) and os.path.exists(server_cert_path):
            client = hvac.Client(
             url=url,
             token=token,
             cert=(client_cert_, client_key),
             verify=server_cert_path,
            )
        else:
            client = hvac.Client(
             url=url,
             token=token,
             verify=False,
            )
        try:
            if client.sys.is_initialized() and client.is_authenticated():
             return client
        except Exception as e:
            logging.error("Exception encountered {err}".format(err=str(e)))
