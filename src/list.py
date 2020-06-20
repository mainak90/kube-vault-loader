from __future__ import absolute_import
#from apiclient import ApiClient
#from create import Create
from actions import Actions
from kubernetes.client.rest import ApiException
import yaml
import sys
import logging
'''
class List(ApiClient):
    def __init__(self):
        super(List, self).__init__()
    def listPods(self):
        client = super().apiclient
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)) 
'''

#List().listPods()
#Create('Secret', 'default', '/Users/mdhar/test.secret.yaml').createResource()
val = Actions(configpath='/Users/mdhar/hvac.json', mount_point='secret', secret_path='development').listFromVault()
print(val)