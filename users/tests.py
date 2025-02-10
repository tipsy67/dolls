from django.test import TestCase

from users.models import User


class UsersAppTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test') #, inn='test', address='test', phone='test', email='test@test.test')

    def test_user_model(self):
        user = User.objects.get(id=self.user.pk)

        field_label = User._meta.get_field('tg_chat_id').verbose_name
        self.assertEqual(field_label, 'телеграм chat id')
        field_label = User._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'аватар')
        field_label = User._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'фото')
        field_label = User._meta.get_field('is_medic').verbose_name
        self.assertEqual(field_label, 'это медик')
        field_label = User._meta.get_field('profession').verbose_name
        self.assertEqual(field_label, 'профессия')
        field_label = User._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'телефон')
        field_label = User._meta.get_field('token').verbose_name
        self.assertEqual(field_label, 'токен')

        max_length = User._meta.get_field('tg_chat_id').max_length
        self.assertEqual(max_length, 50)
        max_length = User._meta.get_field('profession').max_length
        self.assertEqual(max_length, 100)
        max_length = User._meta.get_field('phone').max_length
        self.assertEqual(max_length, 30)
        max_length = User._meta.get_field('token').max_length
        self.assertEqual(max_length, 100)

        expected_object_name = '%s %s.' % (user.last_name, user.first_name[:1])
        self.assertEqual(expected_object_name, str(user))

        self.assertEqual(user.is_medic, False)


    def test_fio(self):
        user = User.objects.get(id=self.user.pk)

        expected_object_name = '%s %s' % (user.last_name, user.first_name)
        self.assertEqual(expected_object_name, user.fio)


    def test_generate_password(self):
        user = User.objects.get(id=self.user.pk)

        self.assertEqual(len(user.generate_password(8)), 8)
