from actions import Actions
import base64
import yaml
import json
import os

val = Actions(mount_point='kv/', secret_path='test/my-secret').fromVault()
for key, value in val.iteritems():
    newval = base64.b64encode(value.encode("utf-8"))
    val[key] = newval

yamldata = yaml.safe_load(open('template/secret.yaml').read())
secname = "test/my-secret".split('/')[1]
yamldata['metadata']['name'] = secname
yamldata['data'] = val

print yamldata

print json.load(open(os.path.expanduser("~") + '/hvac.json', 'r'))['ctx']