from __future__ import absolute_import
from src.apiclient import ApiClient
from kubernetes.client.rest import ApiException
import yaml
import sys
import logging



class Create(ApiClient):
    def __init__(self, resource_type,namespace,filepath):
        self.resource_type = resource_type
        self.namespace = namespace
        self.filepath = filepath
        super(Create, self).__init__()

    def createResource(self):
        logging.info("Creating {type} {path} into namespace {namespace}".format(type=self.resource_type, path=self.filepath, namespace=self.namespace))
        with open(self.filepath) as resource:
            resource_dict=yaml.load(resource)	 #config.load_kube_config()
            name=resource_dict['metadata']['name']
            data=resource_dict['data']
        k8s_client = super().apiclient
        api_instance = k8s_client.CoreV1Api()
        sec  = k8s_client.V1Secret()  # type: object
        try:
            sec.metadata = k8s_client.V1ObjectMeta(name=name)
            sec.type = "Opaque"
            sec.data = data
            resp: object = api_instance.create_namespaced_secret(namespace=self.namespace, body=sec)
            return resp
        except ApiException as e:
            logging.error("Exception occured while invoking CoreV1Api --> create_namespaced_secret {err}".format(err=str(e)))
            sys.exc_clear()
