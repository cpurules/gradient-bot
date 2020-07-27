import random
import math
from PIL import Image, ImageDraw

def getDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def getNormalizedDistance(point1, point2):
    return min(1, float(getDistance(point1, point2)) / (math.sqrt(2) * 1024 / 2))

def getRandomRGB(min = 0, max = 255):
    return [random.randrange(min, max), random.randrange(min, max), random.randrange(min, max)]

def createRandomGradient(size = (1024, 1024), filename='gradient'):
    tenPercentX = int(size[0] / 10)
    tenPercentY = int(size[1] / 10)

    gradientCenter = (random.randrange(tenPercentX, size[0] - tenPercentX), random.randrange(tenPercentY, size[1] - tenPercentY))

    gradient = Image.new('RGBA', size)

    color1 = getRandomRGB(min = 0, max = 255)
    color2 = getRandomRGB(min = 0, max = 255)
    
    # https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python
    for y in range(size[1]):
        for x in range(size[0]):
            point = (x, y)

            normDistanceToCenter = getNormalizedDistance(point, gradientCenter)

            r = color1[0] * normDistanceToCenter + color2[0] * (1 - normDistanceToCenter)
            g = color1[1] * normDistanceToCenter + color2[1] * (1 - normDistanceToCenter)
            b = color1[2] * normDistanceToCenter + color2[2] * (1 - normDistanceToCenter)
            rgb = (int(r), int(g), int(b))

            gradient.putpixel(point, rgb)
    
    gradientAlpha = Image.new("L", size, 0)
    alphaDraw = ImageDraw.Draw(gradientAlpha)
    alphaDraw.ellipse((0, 0, size[0] - 1, size[1] - 1), fill = 255)

    gradient.putalpha(gradientAlpha)

    gradient.save(f'{filename}.png')