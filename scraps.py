import Image

def red2blue():
    im = Image.new("RGB", (256, 256))
    
    for i in range(256):
        for j in range(256):
            im.putpixel((i, j), (i, 0, j))
    im.show()
