from django.test import TestCase

from tunes.models import Feedback, TunesDict


class TunesAppTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.feedback = Feedback.objects.create(name='Feedback for test')
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
