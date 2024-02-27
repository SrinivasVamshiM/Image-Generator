import json
import signal
import sys
from threading import Thread
import replicate
import requests
import websockets
import asyncio
import http.server
import socketserver
import os
from gtts import gTTS 

SDxl_Call = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
LLava_Call = "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5"
WS_PORT = 7890
HTTP_PORT = 8080

httpserver = None
ws_server = None


def start_http_server():
    handler = http.server.SimpleHTTPRequestHandler
    global httpserver
    httpserver = socketserver.TCPServer(("", HTTP_PORT), handler)
    print("serving at port", HTTP_PORT)
    try:
        httpserver.serve_forever()
    finally:
        print("Shutting down http ", HTTP_PORT)
        httpserver.server_close()
        httpserver.shutdown()


def start_ws_server():
    print("starting ws server ", WS_PORT)
    global ws_server
    ws_server = websockets.serve(ws_handler, "localhost", WS_PORT)
    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()


async def ws_handler(websocket, path):
    print("Client connected")
    # Handle incoming messages
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            event = json.loads(message)
            if event["type"] == "desc":
                image_url = gen_image_for_text(event["content"])
                event = {
                    "type": "image",
                    "image": image_url,
                }
                await websocket.send(json.dumps(event))
            elif event["type"] == "query":
                response, audio_url = query_on_image(event["imageurl"], event["content"])
                event = {
                    "type": "answer",
                    "answer": response,
                    "audio_url": audio_url
                }
                await websocket.send(json.dumps(event))
            else:
                print("Invalid ws message type")
    # Handle Disconnection
    except websockets.exceptions.ConnectionClosed as e:
        print("client disconnected")
    finally:
        print("client gone")


def gen_image_for_text(text):
    output = replicate.run(SDxl_Call, input={"width": 768, "height": 768,
                                             "prompt": text,
                                             "scheduler": "K_EULER", "lora_scale": 0.7, "num_outputs": 1,
                                             "guidance_scale": 10,
                                             "apply_watermark": False,
                                             "high_noise_frac": 0.8, "negative_prompt": "",
                                             "prompt_strength": 0.9, "num_inference_steps": 25,
                                             "refine": "expert_ensemble_refiner"
                                             }
                           )
    global output_url
    output_url = output[0]
    print("Image generated at url ", output_url)
    response = requests.get(output_url)
    return output_url


def query_on_image(output_url, query):
    print("Reading query for image ", output_url)
    output = replicate.run(LLava_Call,
                           input={"image": output_url, "top_p": 1, "prompt": query, "max_tokens": 1024,
                                  "temperature": 0.2})
    print("\nBelow is the answer for the above question: \n")
    response = ""
    for item in output:
        print(item, end="")
        response = response + item
    language = 'en'
    myobj = gTTS(text=response, lang=language, slow=False)
    audio_file = "audio.mp3"
    myobj.save(audio_file)
    return response, "/audio.mp3"


def signal_term_handler(frame):
    print('Shutting down!!! \n')
    ws_server.ws_server.close(True)
    httpserver.server_close()
    httpserver.shutdown()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_term_handler)

thread = Thread(target=start_http_server)
thread.start()
start_ws_server()