
import requests
import base64
import json
import socketio
import sys
from printy import inputy, printy
import threading

printy('-------------------------------------------------------------------')
printy('-                      [mB]Websocket-Live@                        -')
printy('-                 Kotak Securities (Market Feed)                  -')
printy('-                      [mB]Python SDK v1.0@                       -')
printy('-------------------------------------------------------------------')
printy('')

sio = socketio.Client()
argmnts = sys.argv
f = open('params.json')
params = json.load(f)


def getClientDetails():
    printy("Arguments provided: ")
    print(argmnts)
    printy("Params provided: ")
    print(params)
    print('')
    global feedType, clientKey, clientSecret, scope, application
    clientKey = argmnts[1] if len(
        argmnts) > 1 else params["clientKey"] if 'clientKey' in params and params['clientKey'] != '' else input("Client Key: ")
    clientSecret = argmnts[2] if len(
        argmnts) > 2 else params["clientSecret"] if 'clientSecret' in params and params['clientSecret'] != '' else input("Client Secret: ")
    application = argmnts[4] if len(argmnts) > 4 else params["application"] if 'application' in params and params['application'] != '' else inputy(
        "Application ([nB]default@): ") or "default"
    scope = argmnts[3] if len(
        argmnts) > 3 else params["scope"] if 'scope' in params and params['scope'] != '' else ""
    while scope != "all" and scope != "prices" and scope != "orders":
        scope = inputy("Scope ([nB]all@|prices|orders): ") or "all"
    feedType = argmnts[5] if len(
        argmnts) > 5 else params["feedType"] if 'feedType' in params and params['feedType'] != '' else ""
    while feedType != "prices" and feedType != "orders":
        feedType = inputy("Feed ([nB]prices@|orders): ") or "prices"

    print('')
    generateToken()


domain = "https://wstreamer.kotaksecurities.com"


def generateToken():
    basic_auth_string = clientKey + ':' + clientSecret
    basic_auth = base64.b64encode(
        basic_auth_string.encode("ascii")).decode("ascii")

    url = domain + "/marketlive/auth/token"
    payload = 'scope='+scope+'&application='+application
    headers = {
        'Authorization': 'Basic ' + basic_auth,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    global _response
    _response = json.loads(response.text)
    if _response['status'] == 'success':
        print('-------------------------------------------------------------------')
        print('access_token: ' + _response['result']['access_token'])
        print('')
        print('expiry: ' + _response['result']['expiry'])
        print('-------------------------------------------------------------------')
        print('')
    else:
        print(_response['result'])
        sys.exit(0)


def getScripts():
    scripts = argmnts[6] if len(
        argmnts) > 6 else params["scripts"] if 'scripts' in params and params['scripts'] != '' else ""
    while scripts == None or scripts == "":
        scripts = inputy("Scripts (eg. wtoken1,wtoken2,...,wtoken10): ") or ""
    print('')
    return scripts


def configWebsocket():
    return {"websocket_url": domain, "websocket_token":
            _response['result']['access_token'], "websocket_path": '/marketlive/orders' if feedType == "orders" else '/marketlive/prices'}


def startWebsocket(websocket_url, websocket_token, websocket_path, scripts):

    @sio.event
    def connect():
        print('Connected...')
        if feedType == "prices":
            sio.emit('stockload', {
                     'wtokens': scripts, 'json': 'true'})

        if feedType == "orders":
            sio.emit('json', 'true')

    @ sio.event
    def disconnect():
        print('Disconnected...')

    @ sio.event
    def connect_error(data):
        print("Error: " + data)

    @ sio.on('broadcast')
    def on_broadcast(msg):
        print('broadcast: ', msg)

    @ sio.on('getstock')
    def on_getdata(data):
        print('getstock: ', json.loads(data))

    @ sio.on('ping')
    def on_ping():
        sio.emit('ping', sio.get_sid())

    sio.connect(websocket_url, headers={'Authorization': 'Bearer ' +
                                        websocket_token}, transports=["websocket"], socketio_path=websocket_path)


def main():
    getClientDetails()
    if _response['status'] == 'success':
        websocketConfig = configWebsocket()
        t1 = threading.Thread(target=startWebsocket, args=(
            websocketConfig['websocket_url'], websocketConfig['websocket_token'], websocketConfig['websocket_path'], getScripts()))
        start = input("Start websocket? (y|n): ")
        if start == 'y':
            t1.start()
            t1.join()
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
