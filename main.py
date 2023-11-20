from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
from base64 import b64decode
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


def generate_image(prompt):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    try:
        response = client.images.generate(
            prompt=prompt,
            size="256x256",
            response_format="b64_json",
            model="dall-e-2"

        )
    except Exception as error:
        print(error)
        return


    file_name = "image.png"
    image_data = b64decode(response.data[0].b64_json)

    with open(file_name, mode= "wb") as png:
        png.write(image_data)

    image = ImageTk.PhotoImage(Image.open("image.png"))
    image_label.configure(image=image)
    image_label.image = image

def handle_generate(event):
    prompt = entry.get()
    print(f"User prompt: {prompt}")
    if prompt.strip() == "":
        print("You need to enter a prompt to generate an image.")
    elif len(prompt) < 10:
        print("The prompt needs to be at lease 10 characters long")
    else:
        generate_image(prompt)


load_dotenv(find_dotenv())

window = tk.Tk()
window.title("Image Generator")
style = ttk.Style()
style.configure("TEntry", padding=10)
greeting = tk.Label(text="Enter prompt to generate image.", padx=10, pady=10)
greeting.pack()
entry = ttk.Entry(width=50)
entry.pack()
button = ttk.Button(text="Generate", padding=10)
button.pack()
button.bind("<Button-1>", handle_generate)

image_label = ttk.Label()
image_label.pack()

window.mainloop()


