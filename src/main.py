import os
from dotenv import load_dotenv
load_dotenv(os.path.join("Config", "local.env"))

from Service import service

if __name__ == "__main__":
    service.run()