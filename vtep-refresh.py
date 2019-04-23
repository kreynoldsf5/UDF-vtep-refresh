#!/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
###
import urllib3
urllib3.disable_warnings()

#import needed vars from env
bipMGMT = os.getenv('BIP')
bipUser = os.getenv('BIPUSER')
bipPass = os.getenv('BIPPASS')
bipPodCIDR = os.getenv('BIPPODCIDR')
bipName = os.getenv('BIPNAME')
bipFlanPIP = os.getenv('BIPFLANPIP')
k8 = os.getenv('K8')
k8Token = os.getenv('K8TOKEN')

#Find new VTEP MAC address on the BIG-IP
try:
    br = requests.get('https://{}/mgmt/tm/net/tunnels/tunnel/~Common~flannel_vxlan/stats?options=all-properties'.format(bipMGMT), verify=False, auth=HTTPBasicAuth(bipUser, bipUser))
    br.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(err)
    sys.exit(1)
try:
    vtepMAC = br.json()['entries']['https://localhost/mgmt/tm/net/tunnels/tunnel/~Common~flannel_vxlan/~Common~flannel_vxlan/stats.nestedStats.entries.macAddr.description']
except json.decoder.JSONDecodeError as err:
    print(err)
    sys.exit(1)

#Create our node payload
node = {"kind": "Node", "spec": {"podCIDR": bipPodCIDR}, "apiVersion": "v1", "metadata": {"name": bipName, "annotations": {"flannel.alpha.coreos.com/backend-data": {"VtepMAC": vtepMAC}, "flannel.alpha.coreos.com/public-ip": bipFlanPIP, "flannel.alpha.coreos.com/backend-type": "vxlan", "flannel.alpha.coreos.com/kube-subnet-manager": "true"}}}

#Make request to kube master
headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(k8Token)}
try:
    kr = requests.post('https://{}/api'.format(k8), verify=False, headers=headers, data=json.dumps(node))
    kr.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(err)
    sys.exit(1)

print(kr.json())
sys.exit(0)
