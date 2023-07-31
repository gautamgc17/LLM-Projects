from fastapi import FastAPI 
import openai
from pydantic import BaseModel


app = FastAPI()
openai.api_key = ""


class Product(BaseModel):
    name: str
    features: list[str]
    category: str


@app.get("/check")
async def check():
    return {"message": "Hello World"}


def generate_description(input):  
    try:
        messages = [
            {"role": "system", "content": "You are a Product Description Generator. Generate multi-paragraph rich text product descriptions with emojis from the information provided to you."},
            {"role": "user", "content": f"{input}"}
        ]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        result = completion.choices[0].message.content

    except Exception as e:
        print(e)
        result = "Request Failed!!"
       
    return result


@app.post("/generate-description")
async def generate_product_description(product: Product):
   description = generate_description(f"Product Name: {product.name}, Product Features: {product.features} and Product Category: {product.category}")
   return  {"Product Description": description}


# REQUEST
# curl -X 'POST' \
#   'http://127.0.0.1:8000/generate-description' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "name": "Samsung Galaxy Book2 (NP750)",
#   "features": [
#     "12th Generation Intel Core i7-1255U processor", "Silver color", "16GB RAM", "15.6 inch display"
#   ],
#   "category": "Gaming Laptop"
# }'


# RESPONSE
# {
#   "Product Description": "Get ready for an ultimate gaming experience with the all-new Samsung Galaxy Book2 (NP750) gaming laptop! 🎮🔥\n\nFeaturing a powerful 12th Generation Intel Core i7-1255U processor, this gaming laptop is built to handle intense gaming sessions and deliver lightning-fast performance. 💪💨 The Silver color gives it a sleek and modern look, making it a stylish choice for gamers.\n\nWith a massive 16GB of RAM, this laptop ensures smooth multitasking and enables you to switch between multiple applications effortlessly. 🚀💼 Whether you're browsing the web, streaming your favorite games, or editing videos, this gaming laptop can handle it all.\n\nGet immersed in stunning visuals on the 15.6-inch display of the Samsung Galaxy Book2 (NP750). 🌟🎮 With high resolution and vibrant colors, every game you play will come to life, offering an immersive gaming experience like never before. The large screen size further enhances your overall gaming experience, providing a wider field of view.\n\nEquipped with the latest features and the power to run demanding games, this Samsung gaming laptop is optimized to deliver exceptional performance. 🏆💻 Whether you're a casual gamer or a professional, this gaming laptop is designed to fulfill all your gaming needs and take your skills to the next level.\n\nUpgrade your gaming setup with the Samsung Galaxy Book2 (NP750) gaming laptop. Experience top-notch performance, stunning visuals, and seamless multitasking in one stylish package. 🎉🖥️ Get ready to dominate the gaming world with this powerful gaming laptop by your side!"
# }
