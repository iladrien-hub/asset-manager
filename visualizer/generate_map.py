import json
import os

from PIL import Image

if __name__ == '__main__':

    path = "./resources/minecraft/textures/block"
    walk = next(os.walk(path))
    files = iter([file for file in walk[2] if file.endswith(".png")])
    print(len([file for file in walk[2] if file.endswith(".png")]))

    width = 24
    height = 29
    size = 16

    res = Image.new("RGBA", (width * size, height * size))
    res_data = {
        "map_width": width * size,
        "map_height": height * size,
        "resolution": size,
        "textures": {}
    }

    try:
        for x in range(width):
            for y in range(height):
                file = next(files)
                image = Image.open(path + "/" + file)
                x_cord, y_cord = x * size, y * size
                res.paste(image, (x_cord, y_cord))
                res_data["textures"][file.replace(".png", "")] = {"x": x_cord, "y": y_cord}
    except StopIteration:
        pass

    res.save("map.png")
    with open("map.json", "w", encoding="utf-8") as f:
        json.dump(res_data, f, ensure_ascii=False, indent=1)
