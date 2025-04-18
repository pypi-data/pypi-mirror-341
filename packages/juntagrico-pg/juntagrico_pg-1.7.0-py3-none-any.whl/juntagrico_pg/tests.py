from django.contrib.auth.models import Permission
from django.urls import reverse

from juntagrico.tests import JuntagricoTestCase


class PGTests(JuntagricoTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.member.user.user_permissions.add(Permission.objects.get(codename='can_sql'))
        cls.member.user.save()

    def test_view_protection(self):
        self.assertGet(reverse('jpg:home'), 302, self.member2)
        self.assertGet(reverse('jpg:sql'), 302, self.member2)

    def test_home(self):
        self.assertGet(reverse('jpg:home'))

    def test_sql_get(self):
        self.assertGet(reverse('jpg:sql'), 404)

    def test_sql_post(self):
        response = self.assertPost(reverse('jpg:sql'), {'sql': 'SELECT 1'})
        self.assertEqual(response.content, b'+---+\n| 1 |\n+===+\n| 1 |\n+---+\nROWS: -1')

    def test_sql_special_command(self):
        self.assertPost(reverse('jpg:sql'), {'sql': '\\h'})

    def test_sql_error(self):
        self.assertPost(reverse('jpg:sql'))
