import asyncio
import random
import math
from PIL import Image, ImageDraw

def getDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def getNormalizedDistance(point1, point2, size):
    return min(1, float(getDistance(point1, point2)) / (math.sqrt(2) * size / 2))

def getRandomRGB(min = 0, max = 255):
    return [random.randrange(min, max), random.randrange(min, max), random.randrange(min, max)]

def RGB2HSV(rgb):
    r, g, b = rgb
    r1, g1, b1 = (r / 255, g / 255, b / 255)
    
    cMax = max(r1, g1, b1)
    cMin = min(r1, g1, b1)
    cDelta = cMax - cMin

    if cDelta == 0:
        hue = 0
    else:
        if cMax == r1:
            hue = 60 * (((g1 - b1) / cDelta) % 6)
        elif cMax == b1:
            hue = 60 * ((b1 - r1) / cDelta + 2)
        else:
            hue = 60 * ((r1 - b1) / cDelta + 4)
    
    if cMax == 0:
        saturation = 0
    else:
        saturation = cDelta / cMax
    
    value = cMax

    return (hue, saturation, value)

def HSV2RGB(hsv):
    h, s, v = hsv

    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r1 = c
        g1 = x
        b1 = 0
    elif h < 120:
        r1 = x
        g1 = c
        b1 = 0
    elif h < 180:
        r1 = 0
        g1 = c
        b1 = x
    elif h < 240:
        r1 = 0
        g1 = x
        b1 = c
    elif h < 300:
        r1 = x
        g1 = 0
        b1 = c
    else:
        r1 = c
        g1 = 0
        b1 = x
    
    r = (r1+m)*255
    g = (g1+m)*255
    b = (b1+m)*255

    return (r, g, b)

def createRandomGradient(size = 1024, filename='gradient', overlay=None):
    tenPercent = int(size / 10)

    gradientCenter = (random.randrange(tenPercent, size - tenPercent), random.randrange(tenPercent, size - tenPercent))

    gradient = Image.new('RGBA', (size, size))

    color1 = getRandomRGB(min = 0, max = 255)
    color2 = getRandomRGB(min = 0, max = 255)
    
    # https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python
    for y in range(size):
        for x in range(size):
            point = (x, y)

            normDistanceToCenter = getNormalizedDistance(point, gradientCenter, size)

            r = color1[0] * normDistanceToCenter + color2[0] * (1 - normDistanceToCenter)
            g = color1[1] * normDistanceToCenter + color2[1] * (1 - normDistanceToCenter)
            b = color1[2] * normDistanceToCenter + color2[2] * (1 - normDistanceToCenter)
            rgb = (int(r), int(g), int(b))

            gradient.putpixel(point, rgb)
    
    gradientAlpha = Image.new("L", (size, size), 0)
    alphaDraw = ImageDraw.Draw(gradientAlpha)
    alphaDraw.ellipse((0, 0, size - 1, size - 1), fill = 255)

    gradient.putalpha(gradientAlpha)

    if overlay is not None:
        overlay = Image.open(f'overlay/{overlay}.png').convert('RGBA')
        gradient = overlayImage(overlay, gradient)

    gradient.save(f'{filename}.png')

def overlayImage(source, dest, resizeRatio = 1.25, opacity=0.6):
    sourceSize = source.size
    destSize = dest.size

    maxSize = (destSize[0] / resizeRatio, destSize[1] / resizeRatio)

    if (sourceSize[0] > maxSize[0]) or (sourceSize[1] > maxSize[1]):
        # we need to resize
        sizeMultipliers = (sourceSize[0] / maxSize[0], sourceSize[1] / maxSize[1])
        sizeMultiplier = max(sizeMultipliers)

        source = source.resize((int(sourceSize[0] / sizeMultiplier), int(sourceSize[1] / sizeMultiplier)))
        sourceSize = source.size

    sourceMask = source.split()[-1].point(lambda p: p * opacity)

    pasteOffsets = (int((destSize[0] - sourceSize[0]) / 2), int((destSize[1] - sourceSize[1]) / 2))

    dest.paste(source, pasteOffsets, sourceMask)

    return dest