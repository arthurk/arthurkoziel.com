from django.db import models
from django.db.models import Q

class ContentManager(models.Manager):
    """
    Custom manager for the ``Content`` model.
    """
    def live(self):
        """
        Returns a ``QuerySet`` of all Content which has the ``LIVE_STATUS`` 
        status.
        """
        return self.filter(status=self.model.LIVE_STATUS)

    def privileged(self, user):
        """
        Returns a ``QuerySet`` of all Content which has the ``LIVE_STATUS`` 
        status if the user is not authenticated or all Content records 
        if the user is authenticated.
        """
        if user.is_authenticated():
            return self.all()
        else:
            return self.exclude(status=self.model.DRAFT_STATUS)
                               