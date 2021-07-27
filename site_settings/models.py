from django.db import models

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class LogoSettings(BaseSetting):
	dark_logo = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.PROTECT,
		blank=True,
		null=True,
		related_name="+",
		help_text="The Dark Theme Logo."
	)
	light_log = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.PROTECT,
		blank=True,
		null=True,
		related_name="+",
		help_text="The Light Theme Logo."
	)

	panels = [
		ImageChooserPanel('dark_logo'),
		ImageChooserPanel('light_log'),
	]


class LinkBlock(blocks.StructBlock):
	name = blocks.CharBlock(max_length=255, required=True, help_text="The name of the social media, Ex: Facebook, Twitter, etc...")
	url  = blocks.URLBlock(max_length=200, required=True, help_text="The link to the social media page or profile, ...")

	class Meta:
		template = 'block_templates/social_link.html'
		icon = 'link'
		lable = 'Add Link'


@register_setting
class SocialMediaLinksSettings(BaseSetting):
	links = StreamField([
		('Link', LinkBlock())
	], min_num=1, max_num=10)

	panels = [
		FieldPanel('links')
	]
