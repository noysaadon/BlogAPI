import uuid
from django.db import models

# Create your models here.

class Blog(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    publisher = models.ForeignKey("authenticate.User", related_name="user", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    user = models.ForeignKey("authenticate.User", related_name="likeuser", on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey("blog.Blog", related_name="likeblog", on_delete=models.CASCADE, null=True, blank=True)