from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import textwrap

apiKey = 'INSERT OPENAI API KEY'
client = OpenAI(api_key=apiKey)

def generate(prompt, hasText, hasBrainrot):
    """
    prompt: String
    hasText: bool
    hasBrainrot: bool
    """

    imageURL = getImage(prompt)

    if hasText:
        text = getText(prompt, hasBrainrot)[1:-1]
        addText(text, imageURL)
    else:
        img_bytes = requests.get(imageURL).content
        with open("image.jpg", "wb") as img_file:
            img_file.write(img_bytes) 

def getImage(thisPrompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt = thisPrompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def getText(prompt, brainrot):
    if brainrot:
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI named B-Rot, B-Rot stands for Brain Rot because gen alpha person, a gen alpha person talks really weird and sometimes incorporates vocabulary such as gyatt (noun), skibidi (adjective), rizz (noun), rizzler (someone with a lot of rizz), fanum tax (verb, used like “I will fanum tax you”) sigma (nickname for cool guy), Ohio (another word for weird), Ohio Sigma (King of sigmas), Mewing (verb), mog (verb), and edging (verb). Each message you send will always be maximum 50 characters."},
            {"role": "user", "content": "Generate a meme caption to a photo with the prompt \""+prompt+"\". Common practice with meme captions can include one or some of the follwing: beginning with \"Me when\", \"When you\", \"When someone\" or \"Why yes,\", dad jokes, and/or references to other memes or pop culture."}
        ]
        )
    else:
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI named B-Rot, B-Rot stands for Brain Rot because gen alpha person, a gen alpha person talks really weird and sometimes incorporates odd vocabulary. Each message you send will always be maximum 50 characters."},
            {"role": "user", "content": "Generate a meme caption to a photo with the prompt \""+prompt+"\". Common practice with meme captions can include one or some of the follwing: beginning with \"Me when\", \"When you\", \"When someone\" or \"Why yes,\", dad jokes, and/or references to other memes or pop culture."}
        ]
        )
    return response.choices[0].message.content

def addText(text, imageURL):
    try:
        # Load the image from the URL
        response = requests.get(imageURL)
        response.raise_for_status()  # Check for HTTP errors
        img = Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        print(f"Error fetching the image: {e}")
        img = None
    except IOError as e:
        print(f"Error opening the image: {e}")
        img = None

    if img:
        # Create a new image with the desired size
        new_width, new_height = 1024, 1224
        new_img = Image.new("RGB", (new_width, new_height), "white")

        # Paste the original image at the bottom
        new_img.paste(img, (0, new_height - 1024))

        # Draw text on the top white rectangle
        draw = ImageDraw.Draw(new_img)
        font_size = 50

        try:
            font = ImageFont.truetype("symbola.ttf", font_size, encoding="unic")
        except IOError:
            font = ImageFont.load_default()

        # Define the maximum width for the text
        max_text_width = new_width * 0.8

        # Calculate the width of the text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # Wrap text if it exceeds the maximum width
        if text_width > max_text_width:
            wrapped_text = textwrap.fill(text, width=40)  # Adjust width as needed
        else:
            wrapped_text = text

        # Calculate each line's size after wrapping
        lines = wrapped_text.split('\n')
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines]

        # Calculate the total height of the wrapped text
        total_height = sum(line_heights) + (len(lines) - 1) * 10  # Adding some space between lines

        # Calculate position to center text vertically
        text_y = (new_height - 1024 - total_height) / 2

        # Draw each line of text centered
        for line, line_height in zip(lines, line_heights):
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            text_x = (new_width - line_width) / 2
            draw.text((text_x, text_y), line, font=font, fill="black")
            text_y += line_height + 10  # Move to the next line position

        # Save the final image
        new_img.save("image.jpg")
        new_img.show()
    else:
        print("Image could not be processed.")


## EXAMPLE USAGE
prompt = 'among us impostors pointing at each other'
text = True
brainrot = False
generate(prompt, text, brainrot)