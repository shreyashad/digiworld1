from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import register_setting
try:
    from wagtail.contrib.settings.models import BaseSetting
except ImportError:
    # Wagtail 4.x+ moved BaseSetting or consolidated it
    from django.db import models as wagtail_models 
    from wagtail.models import Page
    # In newer Wagtail, we just inherit from models.Model or SiteSetting/BaseGenericSetting
    from wagtail.contrib.settings.models import BaseSiteSetting as BaseSetting
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField


@register_snippet
class FooterColumn(ClusterableModel):
    """Snippet for custom footer columns - admin can create and manage footer columns"""
    title = models.CharField(
        max_length=255,
        help_text="Column title/heading"
    )
    column_type = models.CharField(
        max_length=50,
        choices=[
            ('menu', 'Menu Links'),
            ('text', 'Text Content'),
            ('custom', 'Custom HTML'),
        ],
        default='menu',
        help_text="Type of content for this column"
    )
    menu = models.ForeignKey(
        'core.NavigationMenu',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Select a menu (for Menu Links type)'
    )
    content = RichTextField(
        blank=True,
        help_text='Rich text content (for Text Content type)'
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order in footer'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('column_type'),
        FieldPanel('menu'),
        FieldPanel('content'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']
        verbose_name = 'Footer Column'
        verbose_name_plural = 'Footer Columns'

    def __str__(self):
        return self.title


@register_setting
class SiteBrandingSettings(BaseSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    primary_color = models.CharField(
        max_length=20, default="#000000", help_text="Hex color code for primary theme"
    )
    secondary_color = models.CharField(
        max_length=20, default="#ffffff", help_text="Hex color code for secondary theme"
    )
    font_family = models.CharField(
        max_length=100,
        choices=[
            ("sans-serif", "Sans Serif"),
            ("serif", "Serif"),
            ("mono", "Monospace"),
        ],
        default="sans-serif",
    )

    # Contact Information
    contact_address = models.CharField(
        max_length=255, 
        default="925 Filbert Street Pennsylvania 18072",
        help_text="Physical address"
    )
    contact_phone = models.CharField(
        max_length=50, 
        default="+ 45 34 11 44 11",
        help_text="Phone number"
    )
    contact_email = models.EmailField(
        default="info@gmail.com",
        help_text="Contact email address"
    )

    # Social Media Links
    social_facebook = models.URLField(blank=True, help_text="Facebook URL")
    social_twitter = models.URLField(blank=True, help_text="Twitter URL")
    social_instagram = models.URLField(blank=True, help_text="Instagram URL")

    # Footer Policy Pages
    privacy_policy_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Link to Privacy Policy page"
    )
    terms_conditions_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Link to Terms & Conditions page"
    )

    footer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo to display in the footer (usually white/light version)"
    )
    
    # Footer columns - managed through FooterColumn snippet
    footer_description = models.TextField(
        blank=True,
        help_text="Description text for the footer logo section"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("footer_logo"),
                FieldPanel("favicon"),
            ],
            heading="Branding Images",
        ),
        MultiFieldPanel(
            [
                FieldPanel("primary_color"),
                FieldPanel("secondary_color"),
                FieldPanel("font_family"),
            ],
            heading="Theme Styles",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_address"),
                FieldPanel("contact_phone"),
                FieldPanel("contact_email"),
            ],
            heading="Contact Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("social_facebook"),
                FieldPanel("social_twitter"),
                FieldPanel("social_instagram"),
            ],
            heading="Social Media",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_description"),
            ],
            heading="Footer Settings",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("privacy_policy_page"),
                PageChooserPanel("terms_conditions_page"),
            ],
            heading="Footer Policy Pages",
        ),
    ]


class NavigationMenuItem(Orderable):
    parent = ParentalKey(
        "core.NavigationMenu", related_name="menu_items", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    link_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Custom URL (used if no page is selected)",
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url

    panels = [
        FieldPanel("label"),
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
    ]


@register_snippet
class NavigationMenu(ClusterableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated from title")

    panels = [
        FieldPanel("title"),
        InlinePanel("menu_items", label="Menu Items"),
    ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PolicyPage(Page):
    """Page type for policy pages (Privacy Policy, Terms & Conditions, etc.)"""
    body = RichTextField(blank=True, help_text="Page content")

    panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Policy Page"
        verbose_name_plural = "Policy Pages"

    def __str__(self):
        return self.title
