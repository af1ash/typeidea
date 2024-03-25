from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(
            first_name='tester'
        )
        test_category = Category.objects.create(
            name='test_catgory',
            owner=test_user
        )
        Post.objects.create(
            title="post1",
            desc="test post",
            content="test post content",
            category=test_category,
            owner=test_user
        )

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Post.objects.get(title="post1")
        self.assertEqual(lion.desc, 'test post')