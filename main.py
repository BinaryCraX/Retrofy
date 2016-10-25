#!/usr/bin/python

import alsaaudio, time, audioop, requests, json

currentState = False
lastState = False

debug_values = False
counter = 0

threshold = 500

url = "http://localhost:6680/mopidy/rpc"

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, "hw:1,0")

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(640)

while True:
    # Read data from device
    l,data = inp.read()
    if l:
        # calculate the biggest difference
        minmax = audioop.minmax(data, 2)
        diff = (minmax[0] - minmax[1]) * -1

        if diff <= threshold:
            currentState = False
        else:
            currentState = True


        if currentState != lastState:
            method = ""
            if currentState == True:
                method = "core.playback.play"
            else:
                method = "core.playback.pause"

            payload = { "method": method,
                "jsonrpc": "2.0",
                "id": 1 }

            response = requests.post(url, data=json.dumps(payload))

            lastState = currentState
            print(currentState)

        if counter >= 500 and debug_values:
            print('---')
            print(audioop.minmax(data, 2))
            print(audioop.avg(data, 2))
            print(audioop.max(data, 2))
            print(diff)
            print('---')
            counter = 0

        lastState = currentState
        counter += 1