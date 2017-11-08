from django.db import models                   
from django.db.models import Q

class PostQueryset(models.QuerySet):
    
    def search(self,querry):
        if querry:
            querry=querry.strip()
            return self.filter(
                Q(author__username__icontains=querry)|
                Q(title__icontains=querry)|
                Q(text__icontains=querry))
        return self
            

class PostManager(models.Manager):

    def get_queryset(self):
        return PostQueryset(self.model,using=self._db)

    def authors(self):
        return self.get_queryset().authors()

    def search(self,querry):
        return self.get_queryset().search(querry)    
