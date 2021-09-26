from django.contrib import admin

from assets.models import Asset, Relation, Spinset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass


@admin.register(Relation)
class TopDownRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Spinset)
class SpinsetAdmin(admin.ModelAdmin):
    pass
