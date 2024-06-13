from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
       
    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()
        
    class Meta:
        abstract = True
