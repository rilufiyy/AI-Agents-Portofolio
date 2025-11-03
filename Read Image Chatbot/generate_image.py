from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_KEY_API')
)

prompt = 'Beautiful aerial view of Bunaken Island, North Sulawesi, Indonesia, crystal clear blue ocean, coral reefs, tropical paradise, high detail, natural lighting'

# Generate image
response = client.images.generate(
    model='dall-e-3',
    prompt=prompt,
    size='1024x1024',
    quality='hd',
    n=1
)

# Get image URL
image_url = response.data[0].url
print(f'URL: {image_url}')

# Download image
image_data = requests.get(image_url).content

# Safe filename (no spaces or colons)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f'gambar_{timestamp}.png'

with open(file_name, 'wb') as f:
    f.write(image_data)

print(f"Gambar berhasil disimpan sebagai: {file_name}")