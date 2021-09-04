from django.apps import AppConfig


class BidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bid'
    # def ready(self):
    #     from scheduler import categorise_bids
    #     categorise_bids.start()
