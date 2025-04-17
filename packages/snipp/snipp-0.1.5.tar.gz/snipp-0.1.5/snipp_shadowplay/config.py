import os

def get_api_key():
  return os.getenv("SNIPP_API_KEY") or load_from_config()

def load_from_config():
  config_path = os.path.expanduser("~/.snipp_uploader")
  if os.path.exists(config_path):
    with open(config_path) as f:
      return f.read().strip()
  raise RuntimeError("API key environmental variable (SNIPP_API_KEY) not found.") 