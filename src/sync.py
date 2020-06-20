from __future__ import absolute_import
from src.apiclient import ApiClient
from kubernetes.client.rest import ApiException
from src.actions import Actions
import sys
import logging
import yaml

class Sync(object):
    def __init__(self, namespace):
        self.namespace = namespace
    def syncToVault(self):
        k8s_client = ApiClient().apiclient
        api_instance = kubernetes.client.CoreV1Api(k8s_client)
        try:
            resource_list = api_instance.list_namespaced_secret(self.namespace, pretty=True, timeout_seconds=30)
            logging.info('Retrieved list of secrets from project ' + self.namespace)
        except ApiException as e:
            logging.error('Error encountered when calling CoreV1Api --> list_namespaced_secret ' + str(e))
            sys.exit(1)
        secdict = []
        for resource in resource_list.items:
            secdict.append(resource.metadata.name)
        logging.info('Secret list is ' + str(secdict))
        for secret in secdict:
            try:
                fullyaml = api_instance.read_namespaced_secret(secret, self.namespace, pretty=True)
                yamlresponse = yaml.safe_load(str(fullyaml))
                yamldata = yamlresponse['V1Secret[Secret]']['data']
                for key, value in yamldata.iteritems():
                    try:
                        Actions(secret_path=self.namespace + '/' + secret, mount_point='secret', secret={ key: value }).toVault()
                        logging.info('Secret ' + secret + ' key ' + key + ' added to hashicorp vault')
                    except Exception as e:
                        logging.error('Error pushing secret key ' + key + ' from secret ' + secret + ' to hashicorp vault. See ERROR: ' + str(e))
            except ApiException as e:
                logging.error('Encountered error while calling CoreV1Api --> read_namespaced_secret for secret' + secret + ' Error: ' + str(e))
            logging.info('All secrets in namespace ' + self.namespace + ' pushed to Vault')