from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class HomePage(Page):
    max_count = 1
    template = 'home/home_page.html'

    header_post = models.ForeignKey(
        'blog.PostPage',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('header_post'),
        MultiFieldPanel([
            InlinePanel('featured_posts', min_num=1, max_num=2, label="Featured Post"),
        ], heading="featured posts", help_text="Posts To Show in Featured as part of the featured_posts section of the home page."),
        MultiFieldPanel([
            InlinePanel('trending_topics', min_num=3, max_num=6, label="Trending Topic"),
        ], heading='trending topics', help_text="The most popular topics to show in the MOST TRENDING TOPICS setion in the hope page."),
        MultiFieldPanel([
            InlinePanel('popular_posts', min_num=3, max_num=5, label="Trending Topic"),
        ], heading='popular posts', help_text="The most popular posts to show in the MOST POPULAR POSTS setion in the hope page."),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['menu_items'] = self.get_children().live().public().in_menu()
        # context['social_links'] = SocialMediaLink.objects.all()
        return context

# class HeaderPosts(Orderable):
#     page = ParentalKey('home.HomePage', related_name="header_posts")
#     post = models.ForeignKey(
#         'blog.PostPage',
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#         related_name="+"
#     )

#     panels = [
#         FieldPanel('post'),
#     ]


class FeaturedPosts(Orderable):
    page = ParentalKey('home.HomePage', related_name="featured_posts")
    post = models.ForeignKey(
        'blog.PostPage',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="+"
    )

    panels = [
        FieldPanel('post'),
    ]


class TrendingTopics(Orderable):
    page  = ParentalKey('home.HomePage', related_name="trending_topics")
    topic = models.ForeignKey(
        'blog.Topic',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )

    panels = [
        SnippetChooserPanel('topic'),
    ]


class PopularPosts(Orderable):
    page  = ParentalKey('home.HomePage', related_name="popular_posts")
    post = models.ForeignKey(
        'blog.PostPage',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="+"
    )

    panels = [
        FieldPanel('post'),
    ]