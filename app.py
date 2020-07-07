

import json
import time
import requests
import demisto_client.demisto_api
from datetime import datetime
from demisto_client.demisto_api.rest import ApiException
from flask import Flask, json, request, Response, jsonify

host = 'https://192.168.55.129'

#Reads the API key from a file
with open('apikeys.txt') as json_file:
    data = json.load(json_file)
    json_file.close()
    apikey = data['api_key']


app = Flask(__name__)


@app.route('/prismaupdate', methods=['GET'])
def create_inc():
    #Demisto - Create a new incident that runs a playbook
    api_instance = demisto_client.configure(base_url=host, api_key=apikey, debug=False, verify_ssl=False)

    create_incident_request = demisto_client.demisto_api.CreateIncidentRequest()
    create_incident_request.name = 'Prisma Update: {}'.format(datetime.now())
    create_incident_request.owner = 'admin'
    create_incident_request.type = 'Prisma Update'
    create_incident_request.labels = [demisto_client.demisto_api.Label('Instance', 'Demisto Py Client')]
    create_incident_request.source_brand = 'API'
    create_incident_request.playbook_id = 'afad7092-4458-457f-8ac7-9ddca16961fc'

    try:
        api_response = api_instance.create_incident(create_incident_request=create_incident_request)
        #return(api_response)
        return(f"(200) Incident: {create_incident_request.name}  Successfully Created")

    except ApiException as e:
        return("Exception when calling DefaultApi->create_incident: %s\n" % e)


@app.route('/json', methods=['POST'])
def json_req():
    #The Palo Alto Networks FW triggers on a log event then POST's JSON to this function
    #This pulls all the fields into the code from the POST. There are empty fields for future use
    request_json = request.get_json()

    lt = request_json['logtype']
    sv = request_json['severity']
    ip = request_json['ip']
    ct = request_json['category']
    ap = request_json['app']
    ur = request_json['url']
    a1 = request_json['additional_info']['value1']
    a2 = request_json['additional_info']['value2']

    at0 = request_json['attributes'][0]
    at1 = request_json['attributes'][1]
    at2 = request_json['attributes'][2]

    bol = request_json['boolean_test']



    api_instance = demisto_client.configure(base_url=host, api_key=apikey, debug=False, verify_ssl=False)

    create_incident_request = demisto_client.demisto_api.CreateIncidentRequest()
    create_incident_request.name = 'IOC Incident: {}'.format(datetime.now())
    create_incident_request.owner = 'admin'
    create_incident_request.type = 'Unclassified'
    create_incident_request.playbook_id = '55b582f7-899f-4d5f-8009-93dc5cf8cbb9'
    create_incident_request.details = ip

    try:
        api_response = api_instance.create_incident(create_incident_request=create_incident_request)
        print(api_response)
        return '''
           The Log Type value is: {}
           The Severity value is: {}
           The IP address is: {}
           The URL is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(lt, sv, ip, ur, at0, bol)

    except ApiException as e:
        return("Exception when calling DefaultApi->create_incident: %s\n" % e)




if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')