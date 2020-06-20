from hvclient import HvClient
import logging


class Actions(HvClient):
    def __init__(self, key=None, configpath=None, mount_point='', secret_path='', secret=None):
        self.key = key
        self.configpath = configpath
        self.secret = secret
        self.mount_point = mount_point
        self.secret_path = secret_path
        super(Actions, self).__init__(configpath=self.configpath)

#Actions(key='key', configpath='$HOME/hvac.json', mount_point='secret', secret_path='development/foo').fromVault()
    def fromVault(self):
        client = super().newClient()
        read_secret_latest_version = client.secrets.kv.v2.read_secret_version(
            path=str(self.secret_path),
            mount_point=str(self.mount_point)
        )
        version = read_secret_latest_version['data']['metadata']['version']
        read_secret_result = client.secrets.kv.v2.read_secret_version(
            path=str(self.secret_path),
            mount_point=str(self.mount_point),
            version=version
        )
        if self.key == None:
            return read_secret_result['data']['data']
        else:
            return read_secret_result['data']['data'][self.key]

    def listFromVault(self):
        client = super().newClient()
        read_secret_result = client.secrets.kv.v2.list_secrets(
            mount_point=str(self.mount_point),
            path=str(self.secret_path),
        )
        return read_secret_result['data']['keys']

    def toVault(self):
        client = super().newClient()
        try:
            client.secrets.kv.v2.create_or_update_secret(
                path=self.secret_path,
                secret=self.secret,
                mount_point=self.mount_point
            )
            logging.info('The kv {secret} has been added into path {mp}/{spath}'.format(secret=self.secret, mp=self.mount_point, spath=self.secret_path))
        except Exception as e:
            logging.error('Exception encountered while pushing into vault : {err}'.format(err=str(e)))
