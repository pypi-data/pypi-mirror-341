
import asyncio
import threading
import websockets
import base64
import http.server
import socketserver
import socket
import os
from typing import Optional
import flet_webview as fwv
import shutil
from urllib.parse import urlparse
import flet as ft



def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def load_camera_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    


class CameraWebView(fwv.WebView):
    latest_frame: Optional[str] = None

    def __init__(self, page: ft.Page, html_path="src"):
        parsed = urlparse(page.url)
        host, port = parsed.hostname, parsed.port
        self.host = host
        self.ws_port = 8765
        self.http_port = port


        default_path = os.path.join(os.path.dirname(__file__), "assets", "camera.html")

        project_path = os.path.join(os.getcwd(), html_path, "assets", "camera.html")


        
        if not os.path.exists(project_path):
            shutil.copy2(default_path, project_path)
            print(f"Файл camera.html скопирован в {project_path}")


        self._started = False
        self._start_services()
        url = f"http://{self.host}:{self.http_port}/camera.html"
        super().__init__(url=url, expand=True)

    def _start_services(self):
        if self._started:
            return
        self._started = True

        threading.Thread(target=lambda: asyncio.run(self._start_ws_server()), daemon=True).start()

    async def _start_ws_server(self):
        async def handler(websocket):
            try:
                async for message in websocket:
                    if message.startswith("data:image"):
                        self.latest_frame = message
            except:
                pass
        async with websockets.serve(handler, self.host, self.ws_port):
            # print(f"🚀 WebSocket: ws://{self.host}:{self.ws_port}")
            await asyncio.Future()

    def get_frame(self) -> Optional[str]:
        return self.latest_frame

    def get_image_bytes(self) -> Optional[bytes]:
        if not self.latest_frame:
            return None
        try:
            b64 = self.latest_frame.split(",")[1]
            return base64.b64decode(b64)
        except:
            return None
