from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextBlock(blocks.TextBlock):
	
	class Meta:
		template = "block_templates/text_block.html"
		icon = "edit"
		label = "Add Text"


class ParagraphBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=False, max_length=255, help_text="The paragraph's title.")
	content = blocks.RichTextBlock(required=True, help_text="The papragraph's content")

	class Meta:
		template = "block_templates/paragraph_block.html"
		icon = "doc-full"
		label = "Add Paragraph"


class ImageBlock(blocks.StructBlock):
	image = ImageChooserBlock(required=True)
	title = blocks.CharBlock(required=False, max_length=255, help_text="The text to show underneat the image.")

	class Meta:
		template = "block_templates/image_block.html"
		icon = "placeholder"
		lable = "Add Image"


class QuoteBlock(blocks.TextBlock):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.help_text = "Add a quote, PS: don't put the quote betwwen quotes \"\"\" those will be added automatically"

	class Meta:
		template = "block_templates/quote_block.html"
		icon = "edit"
		lable = "Add Quote"
