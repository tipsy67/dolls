from django.conf import settings


class CheckedTag:

    def __init__(self, request):
        self.session = request.session
        tags = self.session.get(settings.TAGS_SESSION_ID)
        if tags is None:
            tags = self.session[settings.TAGS_SESSION_ID] = set()
        self.tags = tags

    def change(self, tag_pk):
        tag_pk = str(tag_pk)
        if tag_pk not in self.tags:
            self.tags.add(tag_pk)
        else:
            self.tags.remove(tag_pk)
        self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def __str__(self):
        return "/".join(self.tags)

    def __iter__(self):
        for item in self.tags:
            yield item

    def __len__(self):
        return len(self.tags)

    def clear(self):
        del self.session[settings.TAGS_SESSION_ID]
        self.save()
