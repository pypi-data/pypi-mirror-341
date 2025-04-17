from .watcher import start_watching
from .config import get_api_key
from colorama import Fore, Style

def main():
  try:
    api_key = get_api_key()
    start_watching(api_key)
  except Exception as e:
    print(f"{Fore.LIGHTRED_EX}[ERROR] Something went horribly wrong: {e}{Style.RESET_ALL}")