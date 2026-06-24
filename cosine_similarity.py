import os
import numpy as np
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key = api_key)

sentences = ["java is a OOPS language","i like anime ","What should i watch"]
embedding = []
for i in sentences:
    sen = client.models.embed_content(
    model="gemini-embedding-2",
    contents=i)
    sen = sen.embeddings[0].values
    embedding.append(sen)

def cosine_similaruty(e1,e2):
   return  np.dot(e1,e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))


print(len(embedding[0]))