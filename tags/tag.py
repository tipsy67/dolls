from django.conf import settings


class CheckedTag:

    def __init__(self, request, model: str):
        self.session = request.session
        tags = self.session.get(settings.TAGS_SESSION_ID + model)
        if tags is None:
            tags = self.session[settings.TAGS_SESSION_ID + model] = set()
        self.tags = tags
        self.model = model

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
        del self.session[settings.TAGS_SESSION_ID + self.model]
        self.save()


class ArticleCheckedTag(CheckedTag):

    def __init__(self, request, model='Article'):
        super().__init__(request, model)


class ProductCheckedTag(CheckedTag):

    def __init__(self, request, model='Product'):
        super().__init__(request, model)
