import os
import time
import requests
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style
from .utils import wait_for_file_completion

init()

os.system('cls' if os.name == 'nt' else 'clear')

class VideoHandler(FileSystemEventHandler):
  def __init__(self, api_key):
    self.api_key = api_key

  def on_created(self, event):
    if not event.is_directory and event.src_path.lower().endswith(".mp4"):
      print(f"{Fore.LIGHTBLUE_EX}[INFO] New video file detected. Uploading...{Style.RESET_ALL}")
      upload_video(event.src_path, self.api_key)

def upload_video(file_path, api_key):
  if not wait_for_file_completion(file_path):
    return
  file_size = os.path.getsize(file_path)
  if file_size > 1_073_741_824:
    print(f"{Fore.LIGHTRED_EX}[ERROR] Upload skipped: File size exceeds upload limit.{Style.RESET_ALL}")
    return
  try:
    with open(file_path, "rb") as video_file:
      files = {"file": (os.path.basename(file_path), video_file, "video/mp4")}
      response = requests.post(
        "https://eu-west.snipp.gg/upload",
        headers={"api-key": api_key, "Accept": "application/json"},
        files=files
      )
    if response.status_code in (200, 201):
      try:
        url = response.json().get("url")
        if url:
          pyperclip.copy(url)
          print(f"{Fore.LIGHTGREEN_EX}[SUCCESS] Uploaded clip: {url}{Style.RESET_ALL}")
      except ValueError:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Invalid response: {response.text}{Style.RESET_ALL}")
    else:
      try:
        error_message = response.json().get("error", response.text)
      except ValueError:
        error_message = response.text
      print(f"{Fore.LIGHTRED_EX}[ERROR] Upload failed: {error_message}{Style.RESET_ALL}")
  except Exception as e:
    print(f"{Fore.LIGHTRED_EX}[ERROR] Upload failed: {e}{Style.RESET_ALL}")

def start_watching(api_key):
  videos_path = os.path.join(os.path.expanduser("~"), "Videos")
  if not os.path.exists(videos_path):
    print(f"{Fore.LIGHTRED_EX}[ERROR] Directory not found: {videos_path}{Style.RESET_ALL}")
    return

  observer = Observer()
  observer.schedule(VideoHandler(api_key), videos_path, recursive=True)
  observer.start()
  print(f"{Fore.LIGHTBLUE_EX}[INFO] Snipp + ShadowPlay started.{Style.RESET_ALL}")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
    print(f"{Fore.LIGHTBLUE_EX}[INFO] Snipp + ShadowPlay stopped.{Style.RESET_ALL}")
  observer.join()