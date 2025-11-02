from openai import OpenAI
from dotenv import load_dotenv
import os

dotenv_path = r"d:\asus\Coding\.env"  
load_dotenv(dotenv_path=dotenv_path)
print("Cek key:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    models = client.models.list()
    print('Sukses!')
except Exception as e:
    print(f'Error: {e}')
