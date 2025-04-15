from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import AuthenticatedOnly

from djangoldp_tamis.models.client import Client
from djangoldp_tamis.models.identifiant import Identifiant
from djangoldp_tamis.models.provider import Provider


class Commande(Model):
    title = models.CharField(max_length=254, blank=True, null=True, default="")
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="clients",
        blank=True,
        null=True,
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="commandes",
        blank=True,
        null=True,
    )
    # TODO: Delete on cascade
    identifiants = models.ManyToManyField(
        Identifiant,
        blank=True,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return "{} ({})".format(self.title, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("Commande")
        verbose_name_plural = _("Commandes")

        serializer_fields = [
            "@id",
            "title",
            "client",
            "provider",
            "identifiants",
            "prestations",
            "creation_date",
            "update_date",
        ]
        nested_fields = ["identifiants", "prestations"]
        rdf_type = "sib:Commande"
        permission_classes = [AuthenticatedOnly]
