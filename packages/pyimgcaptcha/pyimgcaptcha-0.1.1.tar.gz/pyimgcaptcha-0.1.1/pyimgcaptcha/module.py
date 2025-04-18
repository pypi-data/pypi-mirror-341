from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha(filename: str, width: int = 300, height: int = 200):
    image = Image.new('RGB', (width, height), "white")
    draw = ImageDraw.Draw(image)  
    
    try:
        font = ImageFont.truetype("arial.ttf", 30) 
    except:
        font = ImageFont.load_default(30)
    
    chars = string.ascii_uppercase.replace("O", "").replace("I", "") + \
            string.digits.replace("0", "").replace("1", "")
    captcha_text = ''.join(random.choices(chars, k=6))
    
    for i, char in enumerate(captcha_text):

        x = 50 + i * 40 + random.randint(-5, 5)
        y = 80 + random.randint(-30, 30)
        angle = random.randint(-30, 30)

        char_image = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((10, 10), char, font=font, fill="black")
        char_image = char_image.rotate(angle, expand=1)
        
        image.paste(char_image, (x, y), char_image)
    
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=random.choice(["black", "gray", "red", "blue"]))
    
    for _ in range(7):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill="gray", width=1)
    
    image.save(filename)
    #image.show()
    return captcha_text

if __name__ == "__main__":
    #captcha_text = generate_captcha("captcha.png")

    while True:
        captcha_text = generate_captcha("captcha.png")
        answer = input("answer = ")
        if (answer == captcha_text): print("Success") 
        else: print("Error")