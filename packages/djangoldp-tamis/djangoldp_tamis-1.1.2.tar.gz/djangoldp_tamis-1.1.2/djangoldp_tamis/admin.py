from django.contrib import admin
from django.contrib.auth.models import Group
from djangoldp.admin import DjangoLDPAdmin

from djangoldp_tamis.forms import GroupAdminForm
from djangoldp_tamis.models import *


@admin.register(
    Agent,
    Client,
    Commande,
    EditorialWork,
    EditorialWorkTag,
    Favourite,
    Format,
    Identifiant,
    Programme,
    Provider,
    Season,
    Serie,
    Step,
    TamisProfile,
)
class TamisModelAdmin(DjangoLDPAdmin):
    readonly_fields = (
        "creation_date",
        "update_date",
    )
    exclude = ("is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(
    Asset,
    AudioTrack,
    StepToTemplate,
    Track,
    VideoTrack,
)
class EmptyAdmin(TamisModelAdmin):
    def get_model_perms(self, request):
        return {}


class PrestationStepInline(admin.TabularInline):
    model = StepToTemplate
    exclude = ("is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(PrestationStep)
class PrestationStepAdmin(TamisModelAdmin):
    inlines = [PrestationStepInline]


class AssetInline(admin.TabularInline):
    model = Asset
    exclude = ("is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(Prestation)
class PrestationAdmin(TamisModelAdmin):
    inlines = [AssetInline]


class TrackInline(admin.TabularInline):
    model = Track
    exclude = ("is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(MediaResource)
class MediaResourceAdmin(TamisModelAdmin):
    inlines = [TrackInline]


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    readonly_fields = ("name",)

    def get_model_perms(self, request):
        return {}
