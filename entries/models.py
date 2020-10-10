
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entry(models.Model):
    entry_title = models.CharField(max_length=255)
    entry_text = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_author = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_likes = models.ManyToManyField(User, related_name='web_post')

    def total_likes(self):
        return self.entry_likes.count()

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return f'{self.entry_title}'

class Comment(models.Model):
    post = models.ForeignKey(Entry, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies',  on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.entry_title, self.content)