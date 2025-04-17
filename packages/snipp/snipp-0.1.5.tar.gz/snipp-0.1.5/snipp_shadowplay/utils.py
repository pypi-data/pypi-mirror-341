import os
import time
from colorama import Fore, Style

def wait_for_file_completion(file_path):
  start_time = time.time()
  size = -1
  while time.time() - start_time < 10:
    if not os.access(file_path, os.R_OK):
      time.sleep(0.2)
      continue
    current_size = os.path.getsize(file_path)
    if current_size == size and current_size > 0:
      return True
    size = current_size
    time.sleep(0.2)
  print(f"{Fore.LIGHTYELLOW_EX}[WARNING] Waiting for clip to finish processing...{Style.RESET_ALL}")
  return False