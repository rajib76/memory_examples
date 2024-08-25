import os

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
NEO4J_URI = os.environ.get('NEO4J_URI')
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": username,
            "password": password
        }
    },
    "version": "v1.1"
}

client = m = Memory.from_config(config_dict=config)
openai_client = OpenAI()
user = "mohan"

memory = client.get_all(user_id=user)

print("memory ", memory)