import re

def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]
     
buffer = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global buffer
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', buffer, re.DOTALL | re.MULTILINE) # look for colon
             if match:
                 lengthStr, buffer = match.groups()
                  try: 
                       msgLength = int(lengthStr)
                  except:
                       if len(buffer):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(buffer) >= msgLength:
                 payload = buffer[0:msgLength]
                 buffer = buffer[msgLength:]
                 return payload
         r = sock.recv(100)
         buffer += r
         if len(r) == 0:
             if len(buffer) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, buffer))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, buffer))
