import json
import os
import shutil
from pprint import pprint

from rest_framework.response import Response
from rest_framework.views import APIView

from api.v0.relations.getters import get_top, get_down, get_east, get_west, get_north, get_south, SIDES_LIST, SIDES, \
    iterate_sides
from assets.models import Relation, Asset


# noinspection PyUnresolvedReferences
class RelationView(APIView):

    def post(self, request):
        relation = Relation()
        relation.first = Asset.objects.get(pk=request.data["first"])
        relation.second = Asset.objects.get(pk=request.data["second"])
        relation.angle = request.data["angle"]
        relation.direction = request.data["direction"]
        relation.save()
        return Response({
            "success": True,
            "message": f"Relation {relation} created successfully!"
        })

    def delete(self, request):
        obj = Relation.objects.get(pk=request.data["pk"])
        name = str(obj)
        obj.delete()
        return Response({
            "success": True,
            "message": f"Relation {name} deleted successfully!"
        })


class GeneratorView(APIView):
    ASSET_PACKAGE = "E:\\Projects\\.minectaft\\core\\src\\main\\java\\ua\\iladrien\\buildinggenerator\\generator\\assets\\"
    GENERATOR_PACKAGE = "E:\\Projects\\.minectaft\\core\\src\\main\\java\\ua\\iladrien\\buildinggenerator\\generator\\"

    EMPTY = 59

    def get(self, request):
        self.clear_folders()

        empty_relations = {
            "top": [],
            "down": [],
            "east": [],
            "west": [],
            "south": [],
            "north": [],
        }

        for asset in Asset.objects.all():
            self.generate_asset(asset, empty_relations)
        self.generate_assets_list()

        self.generate_empty_asset(empty_relations)

        return Response({
            "success": True,
            "message": "Relations updated successfully!"
        })

    def clear_folders(self):
        for filename in os.listdir(self.ASSET_PACKAGE):
            file_path = os.path.join(self.ASSET_PACKAGE, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def generate_assets_list(self):
        with open("./resources/generator/Assets.java") as f:
            template = f.read()

        imports = []
        assets = []

        imports.append(f"import ua.iladrien.buildinggenerator.generator.assets.Empty;")
        assets.append(f"public static final Asset EMPTY = register(new Empty());")

        for asset in Asset.objects.all():
            for angle in (0, 90, 180, 270):
                className = asset.className.replace("Asset", f"_{angle}_Asset")
                imports.append(f"import ua.iladrien.buildinggenerator.generator.assets.{className};")
                assets.append(
                    f"public static final Asset {asset.title.upper().replace(' ', '_')}_{angle} = register(new {className}());")
            assets.append(f"")

        template = template.replace("{{imports}}", "\n".join(imports))
        template = template.replace("{{assets}}", "\n\t".join(assets))

        with open(f"{self.GENERATOR_PACKAGE}Assets.java", "w") as f:
            f.write(template)

    def generate_empty_asset(self, empty_relations):
        with open("./resources/generator/Asset.java") as f:
            template = f.read()

        template = template.replace("{{class_name}}", "Empty")
        template = template.replace("{{static_blocks}}", "")
        template = template.replace("{{structure}}", "")
        template = template.replace("{{angle}}", str(0))

        # Permissions
        template = template.replace("{{allowedInAir}}", "true")
        template = template.replace("{{allowedOnGround}}", "true")
        for direction in SIDES:
            template = template.replace(f"{{{{allowedOn{direction.capitalize()}Edge}}}}", "true")

        for direction in empty_relations:
            relations = [f"Assets.EMPTY"]
            for asset, angle in empty_relations[direction]:
                relations.append(f"Assets.{asset.title.upper().replace(' ', '_')}_{angle}")
            template = template.replace(f"{{{{relations_{direction}}}}}", ",\n\t\t\t".join(relations))

        with open(f"{self.ASSET_PACKAGE}Empty.java", "w") as f:
            f.write(template)

    def generate_asset(self, asset, empty_relations):
        vertical_relations = {
            "top": get_top(asset),
            "down": get_down(asset),
        }
        horizontal_relations = {
            "north": get_north(asset),
            "west": get_west(asset),
            "south": get_south(asset),
            "east": get_east(asset),
        }

        for direction, relation_list in horizontal_relations.items():
            if len(relation_list) == 0:
                for i, angle in enumerate((0, 90, 180, 270)):
                    side = SIDES_LIST[(SIDES[direction] + i) % 4]
                    empty_relations[side].append((asset, angle))
        for direction, relation_list in vertical_relations.items():
            if len(relation_list) == 0:
                side = "top" if direction == "down" else "down"
                for angle in (0, 90, 180, 270):
                    empty_relations[side].append((asset, angle))

        for angle in (0, 90, 180, 270):
            with open("./resources/generator/Asset.java") as f:
                template = f.read()

            # Structure
            data = json.loads(asset.structure)
            blocks = []
            block_pos = []
            for block in data:
                states = []
                for attr in block["attrs"]:
                    value_class = attr['valueClass'].replace('$', '.')
                    if value_class == "java.lang.Boolean":
                        states.append(f".setValue({attr['type']}, {str(attr['value']).lower()})")
                    else:
                        states.append(f".setValue({attr['type']}, {value_class}.{attr['value']})")
                state = "".join(states)
                state = f"Blocks.{block['id'].replace('minecraft:', '').upper()}.defaultBlockState(){state};"

                blocks.append(state)
                block_pos.append((block['pos'], state))
            static_blocks = {
                block: f"BLOCK_{idx}" for idx, block in enumerate(set(blocks))
            }
            prsf = "\n\t".join(f"private static final BlockState {val} = {key}" for key, val in static_blocks.items())
            structure = "\n\t\t".join(
                [f"data[{pos['y']}][{pos['x']}][{pos['z']}] = {static_blocks[block]};" for pos, block in block_pos])

            className = asset.className.replace("Asset", f"_{angle}_Asset")

            template = template.replace("{{class_name}}", className)
            template = template.replace("{{static_blocks}}", prsf)
            template = template.replace("{{structure}}", structure)
            template = template.replace("{{angle}}", str((angle + asset.defaultAngle) % 360))

            # Permissions
            template = template.replace("{{allowedInAir}}", str(asset.allowedInAir).lower())
            template = template.replace("{{allowedOnGround}}", str(asset.allowedOnGround).lower())

            # Relations
            for direction, relation_list in vertical_relations.items():
                template = self.generate_relations(template, relation_list, direction, angle)

            for direction, relation_list in zip(iterate_sides(angle // 90), horizontal_relations.values()):
                template = template.replace(f"{{{{allowedOn{direction.capitalize()}Edge}}}}", str(len(relation_list) == 0).lower())
                template = self.generate_relations(template, relation_list, direction, angle)

            with open(f"{self.ASSET_PACKAGE}{className}.java", "w") as f:
                f.write(template)

    def generate_relations(self, template, relations_list, direction, angle):
        relations = []
        if len(relations_list) > 0:
            for relation in relations_list:
                angle_ = (relation['angle'] + angle) % 360
                relations.append(f"Assets.{relation['asset'].title.upper().replace(' ', '_')}_{angle_}")
            return template.replace(f"{{{{relations_{direction}}}}}", ",\n\t\t\t".join(relations))
        else:
            return template.replace(f"{{{{relations_{direction}}}}}", "Assets.EMPTY")
