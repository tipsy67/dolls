from django.db import models
from django.urls import reverse

class Tag(models.Model):
    tag = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.tag

    def get_url_change(self):
        return reverse('tags:change_tag', kwargs={'tag_pk': self.pk})

    def str_pk(self):
        return str(self.pk)