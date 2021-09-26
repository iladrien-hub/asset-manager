import json
import sys

import bpy

DEBUG = False

kwargs = {}
for arg in sys.argv:
    if arg.count('=') == 1:
        key, value = arg.split('=', 1)
        kwargs[key] = value

for ob in bpy.data.objects:
    bpy.data.objects.remove(ob, do_unlink=True)

if DEBUG:
    kwargs.update({
        "rinput": "E:\\Projects\\.minectaft\\core\\run\\assets\\2021-06-10_22.25.11.json",
        "routput": "E:\\Projects\\.minectaft\\core\\run\\assets\\spinset\\2021-06-10_22.25.11.png",
    })

print(kwargs)

# Папка с ресурсами
RESOURCES = "E:\\Projects\\.minectaft\\admin\\backend\\resources\minecraft\\"
# Таблица с моделями
MODELS = {}
# Карта расположения текстур на тайлсете
with open("E:\\Projects\\.minectaft\\admin\\backend\\map.json") as f:
    MAP = json.load(f)

TILESET = bpy.data.materials.new(name="tileset")
TILESET.use_nodes = True

bsdf = TILESET.node_tree.nodes["Principled BSDF"]
output = TILESET.node_tree.nodes["Material Output"]

bsdf.inputs[5].default_value = 0
bsdf.inputs[7].default_value = 1

texImage = TILESET.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load(f"E:\\Projects\\.minectaft\\admin\\backend\\map.png")

transp = TILESET.node_tree.nodes.new('ShaderNodeBsdfTransparent')
mix_shader = TILESET.node_tree.nodes.new('ShaderNodeMixShader')

TILESET.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
TILESET.node_tree.links.new(mix_shader.inputs[0], texImage.outputs['Alpha'])
TILESET.node_tree.links.new(mix_shader.inputs[2], bsdf.outputs['BSDF'])
TILESET.node_tree.links.new(mix_shader.inputs[1], transp.outputs['BSDF'])
TILESET.node_tree.links.new(output.inputs["Surface"], mix_shader.outputs['Shader'])
TILESET.node_tree.nodes["Image Texture"].interpolation = 'Closest'

TILESET.blend_method = 'CLIP'


# Функция для определения uv координат для текстуры из тайлсета
def get_coords(texture, uv):
    x, y = MAP["textures"][texture]["x"], MAP["map_height"] - MAP["textures"][texture]["y"] - MAP["resolution"]

    x_1 = (x + uv[0]) / MAP["map_width"]
    x_2 = (x + uv[2]) / MAP["map_width"]

    y_1 = (y + uv[1]) / MAP["map_height"]
    y_2 = (y + uv[3]) / MAP["map_height"]
    return x_1, y_1, x_2, y_2


def texture_east(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[3].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[0].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[1].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[2].uv = (x_1, y_2)


def texture_south(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[7].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[4].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[5].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[6].uv = (x_1, y_2)


def texture_west(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[11].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[8].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[9].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[10].uv = (x_1, y_2)


def texture_north(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[15].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[12].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[13].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[14].uv = (x_1, y_2)


def texture_down(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[16].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[17].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[18].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[19].uv = (x_1, y_2)


def texture_up(ob, texture, uv):
    x_1, y_1, x_2, y_2 = get_coords(texture, uv)

    ob.data.uv_layers[0].data[20].uv = (x_1, y_1)
    ob.data.uv_layers[0].data[21].uv = (x_2, y_1)
    ob.data.uv_layers[0].data[22].uv = (x_2, y_2)
    ob.data.uv_layers[0].data[23].uv = (x_1, y_2)


TEXTURING = {
    "down": texture_down,
    "up": texture_up,
    "east": texture_east,
    "west": texture_west,
    "north": texture_north,
    "south": texture_south,
}


def load_model_node(name):
    with open(f"{RESOURCES}models\\block\\{name}.json") as f:
        data = json.load(f)

    parent = data.get("parent", None)
    model = load_model_node(parent.split("/")[-1]) if parent else {
        "textures": {},
        "elements": []
    }

    model["textures"].update(data.get("textures", {}))
    model["elements"].extend(data.get("elements", []))

    return model


def load_model(name):
    model = MODELS.get(name, None)
    if model:
        return model
    model = load_model_node(name)
    return model


def instantiate(model):
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0.5, 0.5, 0.5),
                                    scale=(0.5, 0.5, 0.5))
    parent = bpy.context.selected_objects[0]
    parent.hide_viewport = True
    parent.hide_render = True

    elements = []

    for element in model["elements"]:
        x1, z1, y1 = element["from"]
        x2, z2, y2 = element["to"]

        scale = ((x2 - x1) / 32, (y2 - y1) / 32, (z2 - z1) / 32)
        location = (x1 + x2) / 32 - 0.5, (y1 + y2) / 32 - 0.5, (z1 + z2) / 32 - 0.5

        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=location, scale=scale)
        ob = bpy.context.selected_objects[0]
        ob.data.materials.append(TILESET)

        elements.append(ob)

        for face in element["faces"].keys():

            material = element["faces"][face]["texture"]
            while material.startswith("#"):
                material = model["textures"][material.replace("#", "")]
            TEXTURING[face](ob, material.split("/")[-1], element["faces"][face].get("uv", (0, 0, 16, 16)))

        ob.parent = parent
    return parent


class Block:

    def __init__(self, idx, element):
        self.idx = idx
        self.element = element
        self.attrs = {}
        for attr in self.element["attrs"]:
            self.attrs[attr["type"]] = attr["value"]

    def instantiate(self):
        model = load_model(self.idx)
        block = instantiate(model)
        facing = self.attrs.get("BlockStateProperties.HORIZONTAL_FACING", None)
        if facing:
            if facing == "WEST":
                block.rotation_euler[2] = 1.5708 * 2
            elif facing == "SOUTH":
                block.rotation_euler[2] = 1.5708
            elif facing == "NORTH":
                block.rotation_euler[2] = 1.5708 * 3
        return block


class Trapdoor(Block):

    def instantiate(self):
        block = super().instantiate()
        if self.attrs["BlockStateProperties.OPEN"]:
            block.rotation_euler[1] = 1.5708
        return block


class Stairs(Block):

    def instantiate(self):
        block = super().instantiate()
        if self.attrs["BlockStateProperties.HALF"] == "TOP":
            block.scale[2] = -1
        return block


CLASSES = {
    "trapdoor": Trapdoor,
    'acacia_trapdoor': 'trapdoor',
    'birch_trapdoor': 'trapdoor',
    'crimson_trapdoor': 'trapdoor',
    'dark_oak_trapdoor': 'trapdoor',
    'iron_trapdoor': 'trapdoor',
    'jungle_trapdoor': 'trapdoor',
    'oak_trapdoor': 'trapdoor',
    'spruce_trapdoor': 'trapdoor',
    'warped_trapdoor': 'trapdoor',
    "stairs": Stairs,
    'acacia_stairs': 'stairs',
    'andesite_stairs': 'stairs',
    'birch_stairs': 'stairs',
    'blackstone_stairs': 'stairs',
    'brick_stairs': 'stairs',
    'cobblestone_stairs': 'stairs',
    'crimson_stairs': 'stairs',
    'dark_oak_stairs': 'stairs',
    'dark_prismarine_stairs': 'stairs',
    'diorite_stairs': 'stairs',
    'end_stone_brick_stairs': 'stairs',
    'granite_stairs': 'stairs',
    'jungle_stairs': 'stairs',
    'mossy_cobblestone_stairs': 'stairs',
    'mossy_stone_brick_stairs': 'stairs',
    'nether_brick_stairs': 'stairs',
    'oak_stairs': 'stairs',
    'polished_andesite_stairs': 'stairs',
    'polished_blackstone_brick_stairs': 'stairs',
    'polished_blackstone_stairs': 'stairs',
    'polished_diorite_stairs': 'stairs',
    'polished_granite_stairs': 'stairs',
    'prismarine_brick_stairs': 'stairs',
    'prismarine_stairs': 'stairs',
    'purpur_stairs': 'stairs',
    'quartz_stairs': 'stairs',
    'red_nether_brick_stairs': 'stairs',
    'red_sandstone_stairs': 'stairs',
    'sandstone_stairs': 'stairs',
    'smooth_quartz_stairs': 'stairs',
    'smooth_red_sandstone_stairs': 'stairs',
    'smooth_sandstone_stairs': 'stairs',
    'spruce_stairs': 'stairs',
    'stone_brick_stairs': 'stairs',
    'stone_stairs': 'stairs',
    'warped_stairs': 'stairs'
}


def draw(structure):
    for element in structure:
        idx = element["id"].replace("minecraft:", "")

        _class = CLASSES.get(idx, Block)
        while type(_class) == str:
            _class = CLASSES.get(_class, Block)

        block = _class(idx, element).instantiate()
        block.location[0] += element["pos"]["x"] - 3.5
        block.location[1] += element["pos"]["z"] - 3.5
        block.location[2] += element["pos"]["y"]


def render():
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                    scale=(0.5, 0.5, 0.5))
    parent = bpy.context.selected_objects[0]
    parent.hide_viewport = True
    parent.hide_render = True
    parent.name = "Camera Parent"

    RAD = 0.01745333333

    LIGHTS = [
        {
            "location": (0, 13.0133, 12.8613),
            "rotation": (-180 * RAD, 135 * RAD, -89.9996 * RAD),
            "color": (1, 1, 1),
            "power": 2000
        },
        {
            "location": (-13.5268, 0, 14.3044),
            "rotation": (0 * RAD, 45 * RAD, 180 * RAD),
            "color": (1, 0.723849, 0.540594),
            "power": 1500
        },
        {
            "location": (10, -11.5, 19.3),
            "rotation": (48.6 * RAD, 0 * RAD, 42.8 * RAD),
            "color": (0.517344, 1, 1),
            "power": 1500
        },
    ]

    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                    scale=(0.5, 0.5, 0.5))
    light_parent = bpy.context.selected_objects[0]
    light_parent.hide_viewport = True
    light_parent.hide_render = True
    light_parent.name = "Camera Parent"

    rot = int(kwargs["rot"])

    for light in LIGHTS:
        bpy.ops.object.light_add(type='AREA', align='WORLD', location=light["location"], rotation=light["rotation"],
                                 scale=(8, 8, 8))
        light_obj = bpy.context.selected_objects[0]
        light_obj.data.energy = light["power"]
        light_obj.data.color = light["color"]
        light_obj.parent = light_parent
    #        light_obj.parent = parent
    light_parent.rotation_euler[2] = (180 + rot) * RAD

    # Камера
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-13, 13, 9), rotation=(1.17164, 0, 3.92699),
                              scale=(1, 1, 1))
    camera = bpy.context.selected_objects[0]
    camera.parent = parent
    bpy.context.scene.camera = camera

    # Прозрачный фон
    bpy.context.scene.render.film_transparent = True


    iterations = 20
    step = 360 / iterations

    for i in range(iterations):
        parent.rotation_euler[2] = (rot + 180 + step * i) * RAD
        # light_parent.rotation_euler[2] = (180 + step * i) * RAD
        bpy.context.scene.render.filepath = kwargs["routput"].replace(".png", f"__deg-{i}__.png")
        bpy.ops.render.render(write_still=True)


# Создание структуры
with open(kwargs["rinput"]) as f:
    structure = json.load(f)
draw(structure)
render()

print()
