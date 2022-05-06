import json
import socket
import traceback
import time


def createmsg(
    sender_name="Controller", request="null", term="null", key="null", value="null"
):
    msg = json.load(open("Message.json"))

    msg["sender_name"] = sender_name
    msg["request"] = request
    msg["term"] = term
    msg["key"] = key
    msg["value"] = value

    return msg


def trySending(msg, target="node4", port=5555, sender="Controller"):

    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    skt.bind((sender, port))
    try:
        # Encoding and sending the message
        skt.sendto(json.dumps(msg).encode("utf-8"), (target, port))
    except:
        #  socket.gaierror: [Errno -3] would be thrown if target IP container does not exist or exits, write your listener
        print(f"ERROR WHILE SENDING REQUEST ACROSS : {traceback.format_exc()}")




# REQUESTS
time.sleep(5)
msg = createmsg(request="STORE")
trySending(msg)


