from PIL import Image
import svgwrite

def red2blue():
    im = Image.new("RGB", (256, 256))
    
    for i in range(256):
        for j in range(256):
            im.putpixel((i, j), (i, 0, j))
    im.show()


def zadani3_B_c():
    polomer = 100
    krok = 9
    dwg = svgwrite.Drawing("results/kulata_mriz.svg")
    offset = polomer
    for i in range(krok/2, polomer+1, krok):
        x = i
        y = (polomer**2 - x ** 2) ** 0.5
        dwg.add(dwg.line((x + offset, y + offset), (x + offset, -y + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.add(dwg.line((-x + offset, y + offset), (-x + offset, -y + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.add(dwg.line((-y + offset, x + offset), (y + offset, x + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.add(dwg.line((-y + offset, -x + offset), (y + offset, -x + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
    dwg.save()

if __name__ == '__main__':
    zadani3_B_c()
