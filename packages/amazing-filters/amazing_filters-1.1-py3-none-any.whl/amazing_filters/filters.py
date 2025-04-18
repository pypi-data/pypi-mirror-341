def black_and_white(r, g, b):
    avg = int((r + g + b) / 3)
    return (avg, avg, avg)

def invert(r, g, b):
    return (255 - r, 255 - g, 255 - b)

FILTERS = { 
    'black_and_white': black_and_white,
    'invert': invert
}
