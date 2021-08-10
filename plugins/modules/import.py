from __future__ import absolute_import, division, print_function

import os
import requests
import random, string

from requests.exceptions import RequestException
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = "type"

ANSIBLE_METADAT = {'metadata_version' : '1.1', 'status':['preview'], 'supported_by':'community'}

DOCUMENTATION = '''
---
module: import
short_description: Importing a ScadaLTS project configuration
description:
 - Connects and creates a session with with ScadaBR server.
 - Uploads the .zip configuration and updates the server..
 
version_added: '2.10.3'
options:
    username:
        description:
            - The username of the admin user for importing to ScadaLTS. 
        type: str
        default: admin
    password:
        description:
            - The password of the admin user for importing to ScadaLTS.
        type: str
        default: admin
    url:
        description:
            - The base URL for the ScadaLTS instance.
        type: str
        required: True
    src:
        description:
            - The source zip file for uploading to ScadaLTS.
        type: path
        aliases: [path]
        required: True
requirements:
    - requests
author:
    - David Allison
'''
EXAMPLES = '''
# Import file.zip to ScadaLTS running on localhost as admin:admin.
- ait.scadalts.import:
    username: admin
    password: admin
    url: http://localhost/ScadaBR
    src: /path/to/my/file.zip
'''
RETURN = '''

'''

def to_plain_text(data):
    txt = ""
    for key,val in data.items():
        txt += key + "=" + val + "\n"
    return txt

def scada_import(username, password, url, src):
    
    # Data for Requests
    auth = {"username": username,"password": password}
    
    import_file = {"importFile": (os.path.basename(src), open(src,"rb"), "application/zip")}
    
    sess_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=35))
    
    init_poll = {
        "callCount":"1",
        "page":"/ScadaBR/import_project.htm",
        "httpSessionId":"",
        "scriptSessionId" : sess_id,
        "c0-scriptName":"MiscDwr",
        "c0-methodName":"initializeLongPoll",
        "c0-id":"0",
        "c0-param0":"number:683118918",
        "c0-param1":"Object_Object:{}",
        "batchId":"0"
    }
    
    load = {
        "callCount":"1",
        "page":"/ScadaBR/import_project.htm",
        "httpSessionId":"",
        "scriptSessionId" : sess_id,
        "c0-scriptName":"EmportDwr",
        "c0-methodName":"loadProject",
        "c0-id":"0",
        "batchId":"1"
    }
    
    update = {
        "callCount":"1",
        "page":"/ScadaBR/import_project.htm",
        "httpSessionId":"",
        "scriptSessionId":sess_id,
        "c0-scriptName":"EmportDwr",
        "c0-methodName":"importUpdate",
        "c0-id":"0",
        "batchId":"2"
    }

    # Login
    s = requests.Session()
    s.post(url+'/login.htm', data=auth)

    # Upload File
    s.post(url+"/import_project.htm", files=import_file)

    # Initialize 'Long Poll'
    s.post(url+"/dwr/call/plaincall/MiscDwr.initializeLongPoll.dwr", data = to_plain_text(init_poll))

    # Load Project
    s.post(url+'/dwr/call/plaincall/EmportDwr.loadProject.dwr', data = to_plain_text(load))

    # Update Project
    s.post(url+'/dwr/call/plaincall/EmportDwr.importUpdate.dwr', data = to_plain_text(update))


def main():

    argument_spec = { 
        "username" : {
            "type" : "str",
            "default" : "admin"
        },
        "password" : {
            "type" : "str",
            "no_log" : True,
            "default" : "admin"
        },
        "url" : {
            "type" : 'str',
            "required" : True
        },
        "src" : {
            "type" : "path",
            "alises" : ["path"],
            "required" : True
        }
    }

    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode = False
    )

    username = module.params["username"]
    password = module.params["password"]
    url = module.params["url"]
    src = module.params["src"]

    
    try:
        scada_import(username, password, url, src)
    except RequestException as e:
        module.fail_json(msg = str(e))

    module.exit_json(changed=True)

if __name__ == "__main__":
    main()
