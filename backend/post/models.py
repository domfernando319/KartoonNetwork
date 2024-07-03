import uuid 
from django.db import models
from django.utils.timesince import timesince
from account.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

# Create your models here.

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    liked_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to ="post_attachments")
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)
    
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)


    # when is it created and by who
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at', )
    
    def created_at_formatted(self):
        return naturaltime(timesince(self.created_at))