from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock

class TwoColumnBlock(StructBlock):
    title = CharBlock(required=True)
    description = RichTextBlock(required=True)
    image = ImageChooserBlock(required=True)

    class Meta:
        template = "aboutus/blocks/two_column_block.html"
        icon = "columns"
        label = "Info Section (2 Columns)"

class FeatureBlock(StructBlock):
    title = CharBlock(required=True)
    description = CharBlock(required=True)
    icon = ImageChooserBlock(required=False)

    class Meta:
        icon = "plus"

class ProcessSectionBlock(StructBlock):
    title = CharBlock(required=True)
    subtitle = CharBlock(required=False)
    features = ListBlock(FeatureBlock())

    class Meta:
        template = "aboutus/blocks/process_section.html"
        icon = "list-ul"
        label = "Process/Features Section"

class AboutUsPage(Page):
    hero_title = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('two_column', TwoColumnBlock()),
        ('process_section', ProcessSectionBlock()),
        ('rich_text', RichTextBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_image'),
        FieldPanel('body'),
    ]

    parent_page_types = ['home.HomePage']
    template = "aboutus/about_us_page.html"

    class Meta:
        verbose_name = "About Us Page"
