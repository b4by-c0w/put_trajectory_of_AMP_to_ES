import requests
import json
from ssl import create_default_context
from elasticsearch import Elasticsearch
import uuid

#API key&clientID
amp_client_id = 'abc'
amp_api_key = '12345'


#info connect to ES
#if use SSL, replace file path have cert
context = create_default_context(cafile="ca.crt")
#username&password
es = Elasticsearch("https://elasticsearch:9200", http_auth=('elastic','password'),ssl_context=context)

#API to get in4 computer
#reference: https://api-docs.amp.cisco.com/api_actions/details?api_action=GET+%2Fv1%2Fcomputers&api_host=api.apjc.amp.cisco.com&api_resource=Computer&api_version=v1
url = 'https://api.apjc.amp.cisco.com/v1/computers'
request = requests.get(url, auth=(amp_client_id, amp_api_key))
data = request.json()

#Get trajectory through computer_guid
for i in range(len(data['data'])):
	link_trajectory = data['data'][i]['links']['trajectory']
	req_trajectory = requests.get(link_trajectory, auth=(amp_client_id, amp_api_key))
	json_str = json.dumps(req_trajectory.json(), indent=4, sort_keys=True)
	data_trajec = req_trajectory.json()
	time.sleep(10)
	#get detail data_event
	for k in range(len(data_trajec['data']['events'])):
		#define env
		ver = data_trajec['version']
		connector_guid = data_trajec['data']['computer']['connector_guid']
		host_name= data_trajec['data']['computer']['hostname']
		active_status = data_trajec['data']['computer']['active']
		connector_version = data_trajec['data']['computer']['connector_version']
		operating_system = data_trajec['data']['computer']['operating_system']
		internal_ips=data_trajec['data']['computer']['internal_ips']
		external_ip = data_trajec['data']['computer']['external_ip']
		group_guid = data_trajec['data']['computer']['group_guid']
		network_addresses = data_trajec['data']['computer']['network_addresses']
		policy_guid = data_trajec['data']['computer']['policy']['guid']
		policy_name = data_trajec['data']['computer']['policy']['name']
		date = data_trajec['data']['events'][k]['date']
		event_type = data_trajec['data']['events'][k]['event_type']
		try:
			detection = data_trajec['data']['events'][k]['detection']
		except:
			detection = 'unknown'
		group_guids = data_trajec['data']['events'][k]['group_guids']
		try:
			disposition = data_trajec['data']['events'][k]['file']['disposition']
		except:
			disposition = 'unknown'
		try:
			file_name = data_trajec['data']['events'][k]['file']['file_name']
		except:
			file_name = 'unknown'
		try: 
			file_path = data_trajec['data']['events'][k]['file']['file_path']
		except:
			file_path = 'unknown'
		try:
			file_type = data_trajec['data']['events'][k]['file']['file_type']
		except:
			file_type = 'unknown'
		try:
			file_sha256 = data_trajec['data']['events'][k]['file']['identity']['sha256']
		except:
			file_sha256 = 'unknown'
		try:
			parent_disposition = data_trajec['data']['events'][k]['file']['parent']['disposition']
		except:
			parent_disposition= 'unknown'
		try:
			parent_identity_sha256 = data_trajec['data']['events'][k]['file']['parent']['indentity']['sha256']
		except:
			parent_identity_sha256 = 'unknown'

		#put to ES
		req_elk = es.index(index ="trajectory", id=uuid.uuid4(), body ={
			"timestamp": date, 
			"version": ver, 
			"connector_guid": connector_guid,
			"host_name":host_name,
			"active_status":active_status,
			"connector_version":connector_version,
			"operating_system":operating_system,
			"internal_ips":internal_ips,
			"external_ip": external_ip,
			"group_guid":group_guid,
			"network_addresses":network_addresses,
			"policy_guid": policy_guid,
			"policy_name":policy_name,
			"event_type":event_type,
			"detection":detection,
			"disposition":disposition,
			"file_name":file_name,
			"file_path":file_path,
			"file_type":file_type,
			"file_sha256":file_sha256,
			"parent_disposition":parent_disposition,
			"parent_identity_sha256":parent_identity_sha256
		})
		print(req_elk['result'])

