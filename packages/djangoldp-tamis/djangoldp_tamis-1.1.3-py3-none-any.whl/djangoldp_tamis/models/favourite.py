from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.fields import LDPUrlField
from djangoldp.models import Model
from djangoldp.permissions import (AuthenticatedOnly, OwnerCreatePermission,
                                   OwnerPermissions)


class Favourite(Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="favourites",
        null=True,
        blank=True,
    )
    favourite = LDPUrlField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} -> {} ({})".format(self.user.username, self.favourite, self.urlid)

    class Meta(Model.Meta):
        verbose_name = _("Favourite")
        verbose_name_plural = _("Favourites")

        auto_author = "user"
        owner_field = "user"
        unique_together = [["user", "favourite"]]

        serializer_fields = [
            "@id",
            "user",
            "favourite",
            "creation_date",
            "update_date",
        ]
        rdf_type = "tamis:Favourite"
        permission_classes = [
            AuthenticatedOnly,
            OwnerCreatePermission,
            OwnerPermissions,
        ]
