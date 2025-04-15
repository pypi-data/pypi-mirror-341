from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import (AuthenticatedOnly, CreateOnly,
                                   InheritPermissions)

from djangoldp_tamis.models.__base import baseAsset
from djangoldp_tamis.models.prestation import Prestation


class Asset(baseAsset):
    prestation = models.ForeignKey(
        Prestation,
        on_delete=models.CASCADE,
        related_name="assets",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    description = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")

        serializer_fields = [
            "@id",
            "identifiants",
            "name",
            "description",
            "media_resources",
            "prestation",
            "creation_date",
            "update_date",
        ]
        nested_fields = [
            "identifiants",
            "media_resources",
            "prestation",
        ]
        rdf_type = "ec:Asset"
        permission_classes = [AuthenticatedOnly & (InheritPermissions | CreateOnly)]
        inherit_permissions = ["prestation"]
