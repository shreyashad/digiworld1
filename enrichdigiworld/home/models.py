from django.db import models
from django.utils.text import slugify

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, ChoiceBlock,
    URLBlock, IntegerBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# =====================================================
# SNIPPETS (Reusable Content)
# =====================================================
@register_snippet
class StatsCounter(ClusterableModel):
    """Statistics counter for the stats section"""
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    symbol = models.CharField(
        max_length=10,
        blank=True,
        choices=[
            ('%', '%'),
            ('k', 'k'),
            ('k+', 'k+'),
            ('+', '+'),
            ('x', 'x'),
            ('M+', 'M+'),
            ('', 'None'),
        ],
        default='',
        help_text='Symbol to display after the value (e.g., %, k, +)'
    )
    description = models.TextField(
        blank=True,
        help_text='Description text for the statistic (e.g., "Follow a hashtag growth total posts, videos and images.")'
    )
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Icon for this statistic'
    )
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('label'),
        FieldPanel('value'),
        FieldPanel('symbol'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Stats Counters'

    def __str__(self):
        return f"{self.label}: {self.value}{self.symbol}"


@register_snippet
class Service(ClusterableModel):
    """Service offered by the company"""
    title = models.CharField(max_length=255)
    description = RichTextField()
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Icon for this service'
    )
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


@register_snippet
class Testimonial(ClusterableModel):
    """Customer testimonial"""
    text = RichTextField()
    author_name = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255, blank=True)
    author_company = models.CharField(max_length=255, blank=True)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('text'),
        FieldPanel('author_name'),
        FieldPanel('author_title'),
        FieldPanel('author_company'),
        FieldPanel('author_image'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Testimonial by {self.author_name}"


@register_snippet
class NetworkLink(ClusterableModel):
    """Social/Network links"""
    name = models.CharField(max_length=255)
    url = models.URLField()
    icon_class = models.CharField(
        max_length=255,
        default='fab fa-linkedin',
        help_text='Bootstrap icon class (e.g., fab fa-linkedin, fab fa-twitter)'
    )
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('icon_class'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# =====================================================
# STREAMFIELD BLOCKS
# =====================================================
class CTAButtonBlock(StructBlock):
    """Single CTA Button"""
    text = CharBlock(max_length=100)
    link = URLBlock()
    button_style = ChoiceBlock(
        choices=[
            ('primary', 'Primary (Blue)'),
            ('secondary', 'Secondary (Gray)'),
            ('outline', 'Outline'),
            ('white', 'White'),
        ],
        default='primary'
    )

    class Meta:
        icon = 'link'


class HeroSlideBlock(StructBlock):
    """Single slide for the hero carousel"""
    title = CharBlock(max_length=255, help_text='Hero slide title')
    subtitle = CharBlock(max_length=500, help_text='Hero slide subtitle', required=False)
    background_image = ImageChooserBlock(help_text='Background image for hero slide')
    overlay_opacity = IntegerBlock(
        min_value=0,
        max_value=100,
        default=40,
        help_text='Opacity of dark overlay (0-100)'
    )
    cta_buttons = ListBlock(CTAButtonBlock())

    class Meta:
        icon = 'image'
        label = 'Hero Slide'


class HeroBlock(StructBlock):
    """Hero section with a carousel of slides"""
    slides = ListBlock(HeroSlideBlock(), min_num=1, help_text='Add one or more slides for the hero carousel')

    class Meta:
        icon = 'image'
        label = 'Hero Section'


class LogoCloudBlock(StructBlock):
    """Client logos section"""
    title = CharBlock(max_length=255, help_text='Section title')
    subtitle = CharBlock(max_length=500, required=False)
    section_title = CharBlock(
        max_length=100,
        default='Our Clients',
        help_text='Display label for clients'
    )

    class Meta:
        icon = 'image'
        label = 'Logo Cloud (Clients)'


class StatsBlock(StructBlock):
    """Statistics section - displays stat cards from database snippets"""
    background_image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'graph'
        label = 'Statistics Section'


class ServiceGridBlock(StructBlock):
    """Services/Features section - 2 column layout with heading on left"""
    # Left column content
    heading = CharBlock(
        max_length=255,
        help_text="Main heading (e.g., 'We provide that service.')"
    )
    description = RichTextBlock(
        required=False,
        help_text="Description text for the left column"
    )
    cta_text = CharBlock(
        max_length=100,
        default='Learn more',
        required=False,
        help_text="Call-to-action button text"
    )
    cta_url = URLBlock(
        required=False,
        help_text="URL for the CTA button"
    )
    # Right column styling
    background_color = CharBlock(
        max_length=7,
        default='#F5F7FA',
        help_text='Background color for service cards section (hex code)'
    )

    class Meta:
        icon = 'fa-th'
        label = 'Services Section'


class WhitepaperCarouselBlock(StructBlock):
    """Latest whitepapers section"""
    title = CharBlock(max_length=255, default='Latest Whitepapers')
    subtitle = CharBlock(max_length=500, required=False)
    limit = IntegerBlock(default=6, help_text='Number of whitepapers to display')
    show_filters = models.BooleanField(default=True, help_text='Show category filters')

    class Meta:
        icon = 'doc-full'
        label = 'Whitepapers Section'


class TestimonialCarouselBlock(StructBlock):
    """Testimonials section"""
    title = CharBlock(max_length=255, default='What Our Clients Say')
    subtitle = CharBlock(max_length=500, required=False)

    class Meta:
        icon = 'comment'
        label = 'Testimonials Section'


class NetworkBlock(StructBlock):
    """Social/Network links section"""
    title = CharBlock(max_length=255, default='Connect With Us')
    subtitle = CharBlock(max_length=500, required=False)

    class Meta:
        icon = 'link'
        label = 'Networks Section'


class NewsletterBlock(StructBlock):
    """Newsletter signup section"""
    title = CharBlock(max_length=255, default='Subscribe to Our Newsletter')
    subtitle = CharBlock(max_length=500, required=False)
    description = RichTextBlock(required=False)
    placeholder = CharBlock(max_length=100, default='Enter your email address')
    button_text = CharBlock(max_length=50, default='Subscribe')
    background_image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'mail'
        label = 'Newsletter Signup'


# =====================================================
# HOME PAGE MODEL
# =====================================================
class HomePage(Page):
    """
    Home page with multiple customizable sections.
    Uses StreamField for flexibility in arranging content blocks.
    """
    introduction = models.TextField(
        blank=True,
        help_text='Brief introduction text for the homepage'
    )

    # StreamField for flexible content management
    body = StreamField([
        ('hero', HeroBlock()),
        ('logo_cloud', LogoCloudBlock()),
        ('stats', StatsBlock()),
        ('services', ServiceGridBlock()),
        ('whitepapers', WhitepaperCarouselBlock()),
        ('testimonials', TestimonialCarouselBlock()),
        ('networks', NetworkBlock()),
        ('newsletter', NewsletterBlock()),
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('body'),
    ]

    subpage_types = ['whitepapers.WhitepaperIndexPage', 'aboutus.AboutUsPage', 'signup.SignupPage', 'core.PolicyPage']

    def __str__(self):
        return self.title
