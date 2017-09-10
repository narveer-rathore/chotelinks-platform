from chotelinks.utils import code_generator, create_shortcode
from django.db import models

# Overriding Model Manager
class ChoteLinkManger(models.Manager):
    # return qs with objects which are active
    def all(self, *args, **kwargs):
        qs = super(ChoteLinkManger, self).all(*args, **kwargs)
        qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self):
        qs = ChoteLink.objects.filter(id__gte=1)
        no_of_refreshed = 0
        for obj in qs:
            obj.short_code = create_shortcode(obj)
            obj.save()
            no_of_refreshed += 1
        return "Refreshed codes for {i} urls.".format(i=no_of_refreshed)

# URL Model
class ChoteLink(models.Model):
    url         = models.CharField(max_length=220,)
    short_code  = models.CharField(max_length=15, unique=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)

    # overide default model manager
    objects = ChoteLinkManger

    # overide default save
    def save(self, *args, **kwargs):
        if self.short_code is None or self.short_code == "":
            self.short_code = create_shortcode(self)
        super(ChoteLink, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
