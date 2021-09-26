import base64
import json
import os

from rest_framework import serializers

from api.v0.relations.getters import get_north, get_south, get_west, get_east, get_down, get_top


# noinspection PyAbstractClass
from assets.models import Spinset


class AssetShortSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    title = serializers.CharField(max_length=100)
    className = serializers.CharField(max_length=100)

    allowedOnGround = serializers.BooleanField()
    allowedInAir = serializers.BooleanField()

    image_tiny = serializers.SerializerMethodField()
    image_small = serializers.SerializerMethodField()

    def get_image_tiny(self, obj):
        return f"/storage/images/{obj.pk}/{obj.pk}-tiny.png"

    def get_image_small(self, obj):
        return f"/storage/images/{obj.pk}/{obj.pk}-small.png"


# noinspection PyAbstractClass
class RelationSerializer(serializers.Serializer):

    pk = serializers.SerializerMethodField()
    angle = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()

    def get_pk(self, obj):
        return obj["pk"]

    def get_angle(self, obj):
        return obj["angle"]

    def get_asset(self, obj):
        return AssetShortSerializer(obj["asset"]).data


# noinspection PyUnresolvedReferences
# noinspection PyAbstractClass
class AssetDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    title = serializers.CharField(max_length=100)
    className = serializers.CharField(max_length=100)

    images = serializers.SerializerMethodField()

    allowedOnGround = serializers.BooleanField()
    allowedInAir = serializers.BooleanField()

    defaultAngle = serializers.IntegerField()

    top = serializers.SerializerMethodField()
    down = serializers.SerializerMethodField()
    east = serializers.SerializerMethodField()
    west = serializers.SerializerMethodField()
    north = serializers.SerializerMethodField()
    south = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [f"/storage/images/asset-{obj.pk}_{(i + obj.defaultAngle // 90) % 4}.png" for i in range(4)]

    def get_top(self, obj):
        return RelationSerializer(get_top(obj), many=True).data

    def get_down(self, obj):
        return RelationSerializer(get_down(obj), many=True).data

    def get_east(self, obj):
        return RelationSerializer(get_east(obj), many=True).data

    def get_west(self, obj):
        return RelationSerializer(get_west(obj), many=True).data

    def get_north(self, obj):
        return RelationSerializer(get_north(obj), many=True).data

    def get_south(self, obj):
        return RelationSerializer(get_south(obj), many=True).data


# noinspection PyAbstractClass
class AssetStructureSerializer(serializers.Serializer):
    structure = serializers.SerializerMethodField()

    def get_structure(self, obj):
        structure = json.loads(obj.structure)

        result = {}
        for item in structure:
            blocks = result.get(item["id"], [])

            blocks.append(item)

            result[item["id"]] = blocks

        return [{"item": item, "entries": result[item]} for item in result]


# noinspection PyAbstractClass
class AssetSpinsetSerializer(serializers.Serializer):

    status = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.spinset is not None

    def get_data(self, obj):
        images = []
        if obj.spinset is not None:
            if obj.spinset.status == Spinset.SPINSET_DONE:
                for idx in range(20):
                    images.append(f"{obj.spinset.path}/spinset-{obj.pk}__deg-{idx}__.png")
                return {
                    "done": True,
                    "message": "Spinset is ok",
                    "images": images
                }
            else:
                return {
                    "done": obj.spinset.status == Spinset.SPINSET_DONE,
                    "message": "Spinset is rendering now",
                    "images": images
                }
        return {
            "done": False,
            "message": "There is no spinset",
            "images": images
        }