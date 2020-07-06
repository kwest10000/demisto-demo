
import demisto_client.demisto_api
from demisto_client.demisto_api.rest import ApiException
from flask import Flask, json, request, Response, jsonify
import json
import logging


#hello world


#Reads the API key from a file
with open('apikeys.txt') as json_file:
    data = json.load(json_file)
    json_file.close()

    apikey = data['api_key']


app = Flask(__name__)


@app.route('/json-pan', methods=['POST'])
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
    

    

    #Demisto - Create a new incident that runs a playbook
    host = 'https://api.demistodemo.io' 
    #host = 'https://192.168.55.166'

    api_instance = demisto_client.configure(base_url=host, api_key=apikey, debug=False, verify_ssl=False)

    create_incident_request = demisto_client.demisto_api.CreateIncidentRequest()
    create_incident_request.name = 'Simulation Incident 420'
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
    app.run(host = '0.0.0.0',port=4000)