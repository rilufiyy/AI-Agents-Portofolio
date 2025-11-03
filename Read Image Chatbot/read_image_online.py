from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

image_url = 'https://cdna.artstation.com/p/assets/images/images/059/692/466/large/cameron-gould-study-of-the-starry-night-vincent-van-gogh-2400.jpg?1676947822'

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role':'user', 'content':[
            {'type':'text', 'text':'Can you please describe this image?'},
            {'type':'image_url', 'image_url':{'url':image_url}}
        ]}
    ]
)

print(response.choices[0].message.content)
