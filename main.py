from rembg import remove
import requests
from PIL import Image
from io import BytesIO
import os

os.makedirs('original', exist_ok=True)
os.makedirs('masked', exist_ok=True)

# img_url = 'https://nationaltoday.com/wp-content/uploads/2020/12/National-Horse-Day-1-640x514.jpg'
img_url = 'https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop' \
          '=4560,2565,x790,y784,safe&width=1200 '
img_name = img_url.split('/')[-1][:-1]+'.jpg'
img_name

img = Image.open(BytesIO(requests.get(img_url).content))
img.save('original/' + img_name, format='jpeg')

output_path = 'masked/' + img_name
output_path

with open(output_path, 'wb') as f:
    input = open('original/' + img_name, 'rb').read()
    subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=50)
    f.write(subject)

background_img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/A_black_image.jpg/640px-A_black_image.jpg'
background_img = Image.open(BytesIO(requests.get(background_img).content))

background_img = background_img.resize((img.width, img.height))

foreground_img = Image.open(output_path)
background_img.paste(foreground_img, (0, 0), foreground_img)
background_img.save('masked/background.jpg', format='jpeg')
