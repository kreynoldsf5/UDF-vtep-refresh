#!/usr/bin/python
import requests
import json
import os

#import needed vars from env
bipMGMT = os.getenv('BIP')
bipUser = os.getenv('BIPUSER')
bipPass = os.getenv('BIPPASS')
bipPodCIDR = os.getenv('BIPPODCIDR')
bipName = os.getenv('BIPNAME')
bipFlanPIP = os.getenv('BIPFLANPIP')
k8 = os.getnenv('K8')
k8Token = os.getenv('K8TOKEN')

#Find new VTEP MAC address on the BIG-IP
br = requests.get('https://{}/mgmt/tm/net/tunnels/tunnel/~Common~flannel_vxlan/stats?options=all-properties'.format(bipMGMT), verify=False, auth=HTTPBasicAuth(bipUser, bipUser))
vtepMAC = br.json().entries.https://localhost/mgmt/tm/net/tunnels/tunnel/~Common~flannel_vxlan/~Common~flannel_vxlan/stats.nestedStats.entries.macAddr.description

#Setup our node payload
node = {"kind": "Node", "spec": {"podCIDR": bipPodCIDR}, "apiVersion": "v1", "metadata": {"name": bipName, "annotations": {"flannel.alpha.coreos.com/backend-data": {"VtepMAC": vtepMAC}, "flannel.alpha.coreos.com/public-ip": bipFlanPIP, "flannel.alpha.coreos.com/backend-type": "vxlan", "flannel.alpha.coreos.com/kube-subnet-manager": "true"}}}

#Make request to kube master
headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(k8Token)}
kr = requests.post('https://{}/api'.format(k8), verify=False, headers=headers, data=json.dumps(node))
print(kr.status_code)
