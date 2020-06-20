from kubernetes import client, config
import os
import logging
from kubernetes.client import ApiClient


# noinspection PyTypeChecker
class ApiClient(object):
    @property
    def apiclient(self) -> object:
        if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token'):
            with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as file:
                token = file.read()
            aConfiguration = client.Configuration()
            aConfiguration.host = "https://kubernetes.default.svc"
            if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'):
                aConfiguration.verify_ssl=True
                aConfiguration.ssl_ca_cert="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
            else:
                aConfiguration.verify_ssl=False
            aConfiguration.api_key = {"authorization": "Bearer " + token}
            logging.info('Initiating kubeapi session with auth token')
            apiclient = client.ApiClient(aConfiguration)
            return apiclient
        elif os.path.exists(os.path.expanduser("~") + '/.kube/config'):
            config.verify_ssl = False
            config.load_kube_config()
            k8sclient = client  # type: ApiClient
            logging.info('Found kubeconfig file on {configpath}'.format(configpath=os.path.expanduser("~") + '/.kube/config'))
            return k8sclient
        else:
            raise Exception('Unauthorized: No kubeconfig file or Bearer token detected so cannot instantiate client instance')
