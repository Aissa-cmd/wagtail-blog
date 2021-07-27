from django.db import models
from django.contrib.auth import get_user_model

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from . import blocks
from home.models import HomePage


@register_snippet
class Topic(models.Model):
	name  = models.CharField(max_length=255, blank=False, null=False)
	image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="+",
		help_text="The image to be show in the blog home page"
	)

	panels = [
		FieldPanel('name'),
		ImageChooserPanel('image'),
	]

	def __str__(self):
		return self.name


class BlogPage(Page):
	template = 'blog/posts_listing_page.html'

	def get_context(self, request):
		context = super().get_context(request)
		context['menu_items'] = HomePage.objects.first().get_children().live().public().in_menu()
		context['trending_topics'] = HomePage.objects.first().trending_topics.all()
		context['popular_posts'] = HomePage.objects.first().popular_posts.all()
		return context


class PostPage(Page):
	image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="+",
		help_text="The image to be show in the blog home page"
	)
	content = StreamField([
		('text', blocks.TextBlock()),
		('image', blocks.ImageBlock()),
		('paragraph', blocks.ParagraphBlock()),
		('quote', blocks.QuoteBlock())
	], min_num=1, null=True, help_text="Please note that these will be appear in the page in the same order you specify them.")

	parent_page_types = ["blog.BlogPage"]
	subpage_types = []

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			ImageChooserPanel('image'),
		], heading='Post Meta data', help_text="This data is used in the posts list page."),
		MultiFieldPanel([
			InlinePanel('post_topics', min_num=1, max_num=3, label="Topic"),
		], heading='Topics', help_text="A post must at least belong to one topic, A post can belong to a maximum 3 topics."),
		FieldPanel('content'),
	]

	def get_context(self, request):
		context = super().get_context(request)
		context['menu_items'] = HomePage.objects.first().get_children().live().public().in_menu()
		return context


class PostTopics(Orderable):
	page  = ParentalKey("blog.PostPage", related_name="post_topics")
	topic = models.ForeignKey(
		'blog.Topic',
		on_delete=models.SET_NULL,
		blank=False,
		null=True
	)

	panels = [
		SnippetChooserPanel('topic'),
	]


class AboutUsPage(Page):
	heading_title = models.CharField(max_length=255, null=False, blank=False)
	text  = models.TextField(blank=False, null=False)
	image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="+",
		help_text="The image to show in the heading."
	)
	content = StreamField([
		('text', blocks.TextBlock()),
		('image', blocks.ImageBlock()),
		('paragraph', blocks.ParagraphBlock()),
		('quote', blocks.QuoteBlock())
	], min_num=1, null=True, help_text="Please note that these will be appear in the page in the same order you specify them.")

	max_count = 1

	template = 'blog/about_page.html'

	subpage_types = []

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('heading_title'),
			FieldPanel('text'),
			ImageChooserPanel('image')
		], heading="Heading Options"),
		FieldPanel('content'),
	]

	def get_context(self, request):
		context = super().get_context(request)
		context['menu_items'] = HomePage.objects.first().get_children().live().public().in_menu()
		context['trending_topics'] = HomePage.objects.first().trending_topics.all()
		context['popular_posts'] = HomePage.objects.first().popular_posts.all()
		return context


class ContactUsPage(Page):
	heading_title = models.CharField(max_length=255, null=False, blank=False)
	text  = models.TextField(blank=False, null=False)
	image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="+",
		help_text="The image to show in the heading."
	)
	content = StreamField([
		('text', blocks.TextBlock()),
		('image', blocks.ImageBlock()),
		('paragraph', blocks.ParagraphBlock()),
		('quote', blocks.QuoteBlock())
	], min_num=1, null=True, help_text="Please note that these will be appear in the page in the same order you specify them.")

	max_count = 1

	template = 'blog/contact_page.html'

	subpage_types = []

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('heading_title'),
			FieldPanel('text'),
			ImageChooserPanel('image')
		], heading="Heading Options"),
		FieldPanel('content'),
	]

	def get_context(self, request):
		context = super().get_context(request)
		context['menu_items'] = HomePage.objects.first().get_children().live().public().in_menu()
		context['trending_topics'] = HomePage.objects.first().trending_topics.all()
		context['popular_posts'] = HomePage.objects.first().popular_posts.all()
		return context

