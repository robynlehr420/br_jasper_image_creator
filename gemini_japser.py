from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from taipy import Gui


MODEL_ID = "gemini-2.0-flash-exp"
jasper_img="first_test_image.jpeg"
CACHED_FILE="cached.name"    # holds name of cached image file in Google Drive
location=""

def location_changed(state,var_name,value):
    print("Enter pressed")
    if len(state.location)==0:
        print("Empty location")
    else:
        prompt="""The attached image is a picture of Brother Jasper.
          He is the mascot of Manhattan University.
          Generate a picture of him near a well-known landmark located in """+state.location+".\n"
          
        print(prompt)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                image,
                prompt
                 ],
                  config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
        )
        for part in response.candidates[0].content.parts:
             if part.text is not None:
                 print("TEXT PART:",part.text)
             elif part.inline_data is not None:
                 print("image found")
                 data = part.inline_data.data
                 state.jasper_img=data
                 state.location=""


load_dotenv() # GEMINI_API_KEY should be defined in a .env file
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

perform_upload=True   # we should upload the image to Google
if os.path.exists(CACHED_FILE):
    with open(CACHED_FILE, "r", encoding="utf-8") as f:
            fn=f.read()
    print("Reading Cached file name:",fn)
    try:
        image=client.files.get(name=fn)   # check if cached file exists
        perform_upload=False # file already at Google, don't upload
    except Exception as e:
        print(f"Problem accessing cached file: {e}\n Uploading again.")
        
if perform_upload:
    image = client.files.upload(file="first_test_image.jpeg")
    print("Uploaded the file, the name is:",image.name)
    # Save image name to the file for later use
    with open(CACHED_FILE, "w", encoding="utf-8") as f:
        f.write(image.name)

page="""
# Jasper Photo Generator
 
<|{jasper_img}|image|>

### Enter the location, somewhere in the world, as the setting for the picture. 

### For example:  New York City, Brazil, Korea, Egypt, etc.

<|{location}|input|change_delay=-1|on_action=location_changed|>


"""

Gui(page).run(port="auto", use_reloader=True)


