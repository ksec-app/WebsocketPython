# WebsocketPython
Python application to consume Ksec live feeds. 


<br>

## Prerequisite:
```sh
python --version
```
>Python 3.10.8

```sh
pip --version
```
>pip 22.3.1
```sh
pip install -r requirements.txt
```

<br>

## Interactive:
```sh
python client.py
```

- Client Key
    - Your consumer key. (required)
- Client Secret
    - Your consumer secret. (required)
- Application
    - Application used for connecting websocket, "default" will be selected if nothing provided.
- Scope
    - all: access token generated will be valid for any type of feed (default).
    - prices: access token generated will be valid for price feed only.
    - orders: access token generated will be valid for order feed only.
- Feedtype
    - prices: /marketlive/prices path will be selected during websocket handshake (default).
    - orders: /marketlive/orders path will be selected during websocket handshake.
- Scripts
    - wtoken for price feed. User can type allowed number of wtokens comma separated.  


<br>

## Simple:
```sh
python client.py arg1 arg2 ...
```

- arg1
    - Your consumer key. (required)
- arg2
    - Your consumer secret. (required)
- arg3
    - Application used for connecting websocket, "default" will be selected if nothing provided.
- arg4
    - all: access token generated will be valid for any type of feed (default).
    - prices: access token generated will be valid for price feed only.
    - orders: access token generated will be valid for order feed only.
- arg5
    - prices: /marketlive/prices path will be selected during websocket handshake (default).
    - orders: /marketlive/orders path will be selected during websocket handshake.
- arg6
    - wtoken for price feed. User can type allowed number of wtokens comma separated.  

.... <br><br>
This is unofficial version of software used to consume live market feed. For more details visit https://wstreamer.kotaksecurities.com/marketlive 