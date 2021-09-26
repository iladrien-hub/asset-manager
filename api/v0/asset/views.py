import os
from threading import Thread
from time import time

from PIL import Image
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import Asset, Spinset
from backend.settings import MEDIA_ROOT
from .serializers import AssetShortSerializer, AssetDetailSerializer, AssetStructureSerializer, AssetSpinsetSerializer


def generate_images(asset):
    os.makedirs(MEDIA_ROOT / f"images/{asset.pk}", exist_ok=True)
    os.makedirs(MEDIA_ROOT / f"images/{asset.pk}/spinset", exist_ok=True)

    filename = str(asset.pk)
    with open(f"./storage/tmp/{filename}.json", "w") as f:
        f.write(asset.structure)

    spinset = Spinset()
    spinset.status = Spinset.SPINSET_RENDERING
    spinset.path = f"/storage/images/{asset.pk}/spinset"
    spinset.save()

    asset.spinset = spinset
    asset.save()

    command = [
        'cmd /C',
        'E:\\Projects\\.minectaft\\admin\\backend\\visualizer\\blender.lnk',
        '-b',
        '--python',
        'E:\\Projects\\.minectaft\\admin\\backend\\visualizer\\blender.py',
        f'rot={asset.defaultAngle}',
        f'rinput="E:\\Projects\\.minectaft\\admin\\backend\\storage\\tmp\\{filename}.json"',
        f'routput="E:\\Projects\\.minectaft\\admin\\backend\\storage\\images\\{asset.pk}\\spinset\\spinset-{asset.pk}.png"',
    ]

    command_str = " ".join(command)
    os.system(command_str)

    spinset.status = Spinset.SPINSET_DONE
    spinset.save()

    image = Image.open(MEDIA_ROOT / f"images/{asset.pk}/spinset/spinset-{asset.pk}__deg-0__.png")
    image.resize((60, 33), Image.ANTIALIAS).save(MEDIA_ROOT / f"images/{asset.pk}/{asset.pk}-tiny.png", quality=100)
    image.resize((600, 337), Image.ANTIALIAS).save(MEDIA_ROOT / f"images/{asset.pk}/{asset.pk}-small.png", quality=100)

    # files = os.listdir(MEDIA_ROOT / f"images/{asset.pk}/spinset/")
    # for idx, file in enumerate(files):
    #     coordinates = Image.open(BASE_DIR / f"resources/visualizer/sideways_spinset/{idx}.png")
    #
    #     image = Image.open(MEDIA_ROOT / f"images/{asset.pk}/spinset/{file}")
    #     image.paste(coordinates, (image.size[0] - coordinates.size[0], image.size[1] - coordinates.size[1]))
    #     image.save(MEDIA_ROOT / f"images/{asset.pk}/spinset/{file}", quality=100)


class AssetRetrieveView(generics.RetrieveAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetDetailSerializer


class AssetView(APIView):

    def get(self, request, format=None):
        assets = AssetShortSerializer(Asset.objects.all(), many=True).data
        return Response(assets)

    def post(self, request, format=None):
        asset = Asset()
        asset.title = request.data["title"]
        asset.className = request.data["className"]
        asset.structure = request.data["structure"]
        asset.allowedOnGround = request.data["allowedOnGround"]
        asset.allowedInAir = request.data["allowedInAir"]
        asset.defaultAngle = request.data["defaultAngle"]
        asset.save()

        Thread(target=generate_images, args=(asset, )).start()

        return Response(
            {"success": True, "message": f"{asset.title}<{asset.pk}> created successfully!", "data": {"id": asset.pk}})


class AssetStructureView(generics.RetrieveAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetStructureSerializer


class SpinsetView(generics.RetrieveAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSpinsetSerializer


class __SpinsetView(APIView):

    def get(self, request):
        # for idx in range(20):
        #     coordinates = Image.open(BASE_DIR / f"resources/visualizer/sideways_spinset/{idx}.png")
        #     coordinates = coordinates.resize((300, 168), Image.ANTIALIAS)
        #     coordinates.save(BASE_DIR / f"resources/visualizer/sideways_spinset/{idx}.png", quality=100)
        # return Response({"ok": "ok"})

        for asset in Asset.objects.all():
            if asset.spinset is None:
                generate_images(asset)
        return Response({"ok": "ok"})
