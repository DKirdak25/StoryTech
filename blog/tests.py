from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Post, PostBlock
from .views import BlogPostList, BlogDetailView


# ============================================================
# Post Model Tests
# ============================================================

class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.test_image = SimpleUploadedFile(
            "test.jpg",
            b"fake-image-content",
            content_type="image/jpeg"
        )

    def test_post_creation(self):
        post = Post.objects.create(
            title="My Post",
            author=self.user,
            image=self.test_image,
        )
        self.assertIsNotNone(post.id)
        self.assertEqual(post.title, "My Post")
        self.assertEqual(post.author, self.user)

    def test_post_str_method(self):
        post = Post.objects.create(
            title="String Test",
            author=self.user,
            image=self.test_image,
        )
        self.assertEqual(str(post), "String Test")

    def test_get_absolute_url(self):
        post = Post.objects.create(
            title="URL Test",
            author=self.user,
            image=self.test_image,
        )
        expected = reverse("blog_detail", args=[post.pk])
        self.assertEqual(post.get_absolute_url(), expected)


# ============================================================
# PostBlock Model Tests (text + code)
# ============================================================

class PostBlockModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.test_image = SimpleUploadedFile(
            "img.jpg",
            b"fake-image-content",
            content_type="image/jpeg"
        )
        self.post = Post.objects.create(
            title="Block Parent",
            author=self.user,
            image=self.test_image
        )

    def test_text_block_creation(self):
        block = PostBlock.objects.create(
            post=self.post,
            type="text",
            value="This is a text block.",
            order=1
        )
        self.assertEqual(block.type, "text")
        self.assertEqual(block.value, "This is a text block.")

    def test_code_block_creation(self):
        block = PostBlock.objects.create(
            post=self.post,
            type="code",
            value="print('Hello')",
            order=2
        )
        self.assertEqual(block.type, "code")
        self.assertEqual(block.value, "print('Hello')")

    def test_block_ordering(self):
        b1 = PostBlock.objects.create(post=self.post, type="text", value="Block B", order=5)
        b2 = PostBlock.objects.create(post=self.post, type="code", value="Block A", order=1)

        blocks = list(PostBlock.objects.filter(post=self.post))
        self.assertEqual(blocks, [b2, b1])


# ============================================================
# Blog List View Tests
# ============================================================

class BlogPostListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.test_image = SimpleUploadedFile(
            "list.jpg",
            b"fake-image-content",
            content_type="image/jpeg"
        )
        self.post = Post.objects.create(
            title="List Post",
            author=self.user,
            image=self.test_image
        )

    def test_list_url_resolves(self):
        view = resolve(reverse("blog_list")).func.view_class
        self.assertEqual(view, BlogPostList)

    def test_list_view_status_code(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_template_used(self):
        response = self.client.get(reverse("blog_list"))
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_list_displays_posts(self):
        response = self.client.get(reverse("blog_list"))
        self.assertContains(response, "List Post")


# ============================================================
# Blog Detail View Tests
# ============================================================

class BlogDetailViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.test_image = SimpleUploadedFile(
            "detail.jpg",
            b"fake-image-content",
            content_type="image/jpeg"
        )
        self.post = Post.objects.create(
            title="Detail Post",
            author=self.user,
            image=self.test_image
        )

        PostBlock.objects.create(post=self.post, type="text", value="This is a text block.", order=1)
        PostBlock.objects.create(post=self.post, type="code", value="print('Hi')", order=2)

    def test_detail_url_resolves(self):
        view = resolve(reverse("blog_detail", args=[self.post.pk])).func.view_class
        self.assertEqual(view, BlogDetailView)

    def test_detail_view_status_code(self):
        response = self.client.get(reverse("blog_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_template_used(self):
        response = self.client.get(reverse("blog_detail", args=[self.post.pk]))
        self.assertTemplateUsed(response, "blog/blog_detail.html")

    def test_detail_displays_blocks(self):
       post = Post.objects.create(title="Test", author=self.user)
       PostBlock.objects.create(
           post=post,
           type="code",
           value="print('Hi')",
           order=1
       )

       url = reverse("blog_detail", args=[post.pk])
       response = self.client.get(url)

       self.assertContains(response, "print(&#x27;Hi&#x27;)")  # Django escapes quotes inside <code> blocks
       escaped_code = "print(&#x27;Hi&#x27;)"
       self.assertContains(response, escaped_code)