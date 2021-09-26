from pprint import pprint

from assets.models import Relation

SIDES = {
    "north": 0,
    "west": 1,
    "south": 2,
    "east": 3,
}

SIDES_LIST = list(SIDES.keys())


def iterate_sides(start=0):
    size = len(SIDES_LIST)
    for i in range(size):
        yield SIDES_LIST[(i + start) % size]


def get_side(asset, side):
    res = []
    res.extend([{
        "pk": item.pk,
        "angle": item.angle,
        "asset": item.second,
    } for item in Relation.objects.all() if item.first == asset and item.direction == side])

    secondary = [item for item in Relation.objects.all() if item.second == asset]

    res.extend([{
        "pk": item.pk,
        "angle": item.angle,
        "asset": item.first,
    } for item in secondary if item.direction == SIDES_LIST[(SIDES[side] + 2) % 4] and item.angle == 0])
    res.extend([{
        "pk": item.pk,
        "angle": item.angle,
        "asset": item.first,
    } for item in secondary if item.direction == side and item.angle == 180])
    res.extend([{
        "pk": item.pk,
        "angle": item.angle,
        "asset": item.first,
    } for item in secondary if item.direction == SIDES_LIST[(SIDES[side] + 3) % 4] and item.angle == 90])
    res.extend([{
        "pk": item.pk,
        "angle": item.angle,
        "asset": item.first,
    } for item in secondary if item.direction == SIDES_LIST[(SIDES[side] + 1) % 4] and item.angle == 270])

    return res


def get_east(asset):
    return get_side(asset, "east")


def get_west(asset):
    return get_side(asset, "west")


def get_north(asset):
    return get_side(asset, "north")


def get_south(asset):
    return get_side(asset, "south")


def get_down(asset):
    return [
        *[{
            "pk": item.pk,
            "angle": item.angle,
            "asset": item.second,
        } for item in Relation.objects.all() if item.first == asset and item.direction == "down"],
        *[{
            "pk": item.pk,
            "angle": item.angle,
            "asset": item.first,
        } for item in Relation.objects.all() if item.second == asset and item.direction == "top"],

    ]


def get_top(asset):
    return [
        *[{
            "pk": item.pk,
            "angle": item.angle,
            "asset": item.first,
        } for item in Relation.objects.all() if item.second == asset and item.direction == "down"],
        *[{
            "pk": item.pk,
            "angle": item.angle,
            "asset": item.second,
        } for item in Relation.objects.all() if item.first == asset and item.direction == "top"],

    ]