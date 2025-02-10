from django.test import TestCase

from tunes.models import Feedback, Quote, Contact, TunesDict


class TunesAppTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.feedback = Feedback.objects.create(name='Feedback for test')
        cls.quote = Quote.objects.create(name='Quote for test')
        cls.contact = Contact.objects.create(country='test', inn='test', address='test', phone='test', email='test@test.test')
        cls.tunesdict = TunesDict.objects.create(key='TunesDict for test')

    def test_feedback_model(self):
        feedback = Feedback.objects.get(id=self.feedback.pk)

        field_label = Feedback._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Имя')
        field_label = Feedback._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Телефон')
        field_label = Feedback._meta.get_field('message').verbose_name
        self.assertEqual(field_label, 'Сообщение')
        field_label = Feedback._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'Создано')
        field_label = Feedback._meta.get_field('is_read').verbose_name
        self.assertEqual(field_label, 'Прочитано')
        field_label = Feedback._meta.get_field('is_published').verbose_name
        self.assertEqual(field_label, 'Публиковать')

        max_length = Feedback._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)
        max_length = Feedback._meta.get_field('phone').max_length
        self.assertEqual(max_length, 20)

        expected_object_name = '%s, %s' % (feedback.name, feedback.created_at)
        self.assertEqual(expected_object_name, str(feedback))

        self.assertEqual(feedback.is_read, False)
        self.assertEqual(feedback.is_published, False)

    def test_quote_model(self):
        quote = Quote.objects.get(id=self.quote.pk)

        field_label = Quote._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Имя')
        field_label = Quote._meta.get_field('quote').verbose_name
        self.assertEqual(field_label, 'Цитата')
        field_label = Quote._meta.get_field('is_published').verbose_name
        self.assertEqual(field_label, 'Публиковать')

        max_length = Quote._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

        expected_object_name = '%s' % (quote.name)
        self.assertEqual(expected_object_name, str(quote))

        self.assertEqual(quote.is_published, False)


    def test_сontact_model(self):
        сontact = Contact.objects.get(id=self.contact.pk)

        field_label = Contact._meta.get_field('country').verbose_name
        self.assertEqual(field_label, 'Страна')
        field_label = Contact._meta.get_field('inn').verbose_name
        self.assertEqual(field_label, 'ИНН')
        field_label = Contact._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'Адрес')
        field_label = Contact._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Телефон')
        field_label = Contact._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Эл.почта')
        field_label = Contact._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

        max_length = Contact._meta.get_field('country').max_length
        self.assertEqual(max_length, 50)
        max_length = Contact._meta.get_field('inn').max_length
        self.assertEqual(max_length, 20)
        max_length = Contact._meta.get_field('address').max_length
        self.assertEqual(max_length, 255)
        max_length = Contact._meta.get_field('phone').max_length
        self.assertEqual(max_length, 30)

        expected_object_name = '%s' % (сontact.email)
        self.assertEqual(expected_object_name, str(сontact))

    def test_tunesDict_model(self):
        tunesDict = TunesDict.objects.get(id=self.tunesdict.pk)

        field_label = TunesDict._meta.get_field('key').verbose_name
        self.assertEqual(field_label, 'Ключ')
        field_label = TunesDict._meta.get_field('value_int').verbose_name
        self.assertEqual(field_label, 'Целочисленное значение')
        field_label = TunesDict._meta.get_field('value_char').verbose_name
        self.assertEqual(field_label, 'Строковое значение')
        field_label = TunesDict._meta.get_field('value_time').verbose_name
        self.assertEqual(field_label, 'Константа времени')
        field_label = TunesDict._meta.get_field('value_date').verbose_name
        self.assertEqual(field_label, 'Константа даты')

        max_length = TunesDict._meta.get_field('key').max_length
        self.assertEqual(max_length, 30)

        expected_object_name = '%s' % (tunesDict.key)
        self.assertEqual(expected_object_name, str(tunesDict))

