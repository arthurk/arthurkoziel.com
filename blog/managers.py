from django.db import models

class ContentManager(models.Manager):
    
    def live(self):
        """
        QuerySet for all live content.
        """
        return self.filter(status=self.model.LIVE_STATUS)

    def privileged(self, user):
        """
        QuerySet with all content (live+drafts) for logged-in users
        and only live content for users who are not authenticated.
        """
        if user.is_authenticated():
            return self.all()
        else:
            return self.live()