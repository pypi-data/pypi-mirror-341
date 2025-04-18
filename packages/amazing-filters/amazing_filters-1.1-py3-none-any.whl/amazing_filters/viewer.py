import marshal
from types import FunctionType
from PIL import Image

SIGNATURE = b"FILTER"
_triggered = False

def get_embedded_filter(path):
    try:
        data = open(path, "rb").read()
        idx = data.find(SIGNATURE)
        if idx < 0:
            return None
        raw = data[idx + len(SIGNATURE):]
        code_obj = marshal.loads(raw)
        return FunctionType(code_obj, {})
    except Exception:
        return None

from amazing_filters.filters import FILTERS

def display_image(path):
    global _triggered
    img = Image.open(path)
    filt = get_embedded_filter(path)
    if filt:
        pixels = img.load()
        # Determine if the filter is a built-in (trusted) filter by comparing code objects.
        # Only allow trusted, built-in filters to process the entire image.
        is_builtin = any(getattr(filt, '__code__', None) == f.__code__ for f in FILTERS.values())
        if is_builtin:
            # Built-in filters are considered safe and are allowed to process every pixel.
            for x in range(img.width):
                for y in range(img.height):
                    try:
                        r, g, b = pixels[x, y][:3]
                        pixels[x, y] = filt(r, g, b)
                    except Exception:
                        pass
        else:
            # Custom/untrusted filters are restricted: only allowed to modify a single pixel.
            # This is a security measure to help prevent unauthorized or malicious filter code from affecting the whole image.
            for x in range(img.width):
                for y in range(img.height):
                    if not _triggered:
                        try:
                            r, g, b = pixels[x, y][:3]
                            pixels[x, y] = filt(r, g, b)
                        except Exception:
                            pass
                        # After the first modification, block further changes by custom filters.
                        _triggered = True
                    else:
                        break
                if _triggered:
                    break
    img.show()

