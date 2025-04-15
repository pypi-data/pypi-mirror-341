from django.apps import AppConfig


class DjangoldpTamisConfig(AppConfig):
    name = "djangoldp_tamis"

    def ready(self):
        try:
            from djangoldp_tamis.models.step import Step

            Step.objects.get_or_create(name="Refusé")
            Step.objects.get_or_create(name="Validation")
            Step.objects.get_or_create(name="Livraison")
        except Exception as e:
            if 'relation "djangoldp_tamis_step" does not exist' in str(e):
                pass
            else:
                raise
