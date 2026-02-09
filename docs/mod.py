from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField

@register_snippet
class WhitepaperCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    order = models.IntegerField(default=0)

    panels = [
        FieldPanel('name'),
    ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "whitepaper categories"


@register_snippet
class WhitepaperClient(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
    ]

    def __str__(self):
        return self.name


class WhitepaperIndexPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    subpage_types = ['WhitepaperPage']

    def get_context(self, request):
        context = super().get_context(request)

        # Base queryset
        whitepapers = (
            WhitepaperPage.objects
            .live()
            .descendant_of(self)
            .order_by('-date')
            .select_related("client", "preview_image")
            .prefetch_related("categories")
        )

        # Category Filtering
        category_slug = request.GET.get("category")
        if category_slug:
            whitepapers = whitepapers.filter(categories__slug=category_slug)

        # Search Filtering
        search_query = request.GET.get("q")
        if search_query:
            whitepapers = whitepapers.search(search_query)

        context["whitepapers"] = whitepapers
        context["categories"] = WhitepaperCategory.objects.all()
        context["current_category"] = category_slug
        context["search_query"] = search_query
        return context



@register_snippet
class WhitepaperTemplate(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=255)

    preview_template = models.CharField(max_length=255)
    landing_template = models.CharField(max_length=255)
    thankyou_template = models.CharField(max_length=255)

    inline_form = models.BooleanField(default=False)
    theme_config = models.JSONField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("preview_template"),
        FieldPanel("landing_template"),
        FieldPanel("thankyou_template"),
        FieldPanel("inline_form"),
        FieldPanel("theme_config"),
    ]

    def __str__(self):
        return self.name


class FormSchema(models.Model):
    name = models.CharField(max_length=255)
    submit_text = models.CharField(max_length=100, default="Download Now")
    success_text = models.TextField(blank=True)
    is_email_gate = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default="v1")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class FormField(models.Model):
    FIELD_TYPES = [
        ("text", "Text"),
        ("email", "Email"),
        ("select", "Select"),
        ("radio", "Radio"),
        ("checkbox", "Checkbox"),
        ("phone", "Phone"),
    ]

    schema = models.ForeignKey(FormSchema, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=255)
    name = models.SlugField()
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    placeholder = models.CharField(max_length=255, blank=True)

    # Nested logic
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.CASCADE, related_name="children"
    )
    show_when_value = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("schema", "name")

        def __str__(self):
            return f"{self.schema.name} - {self.label}"
    


class FormOption(models.Model):
    field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        
        def __str__(self):
            return self.label



class DisclaimerBlock(models.Model):
    title = models.CharField(max_length=255, blank=True)
    body = RichTextField()
    requires_checkbox = models.BooleanField(default=False)
    checkbox_label = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
    def __str__(self):
        return self.title or "Disclaimer"



class ConsentProfile(models.Model):
    name = models.CharField(max_length=255)
    default_text = RichTextField()
    privacy_url = models.URLField(blank=True)
    version = models.CharField(max_length=20, default="v1")

    def __str__(self):
        return self.name



class CountryConsentRule(models.Model):
    profile = models.ForeignKey(ConsentProfile, on_delete=models.CASCADE, related_name="rules")
    country_code = models.CharField(max_length=2)
    text = RichTextField()
    checkbox_required = models.BooleanField(default=True)



class Lead(models.Model):
    whitepaper = models.ForeignKey("WhitepaperPage", on_delete=models.CASCADE, related_name="leads")
    email = models.EmailField()

    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField()

    utm_source = models.CharField(max_length=255, blank=True)
    utm_campaign = models.CharField(max_length=255, blank=True)
    referer = models.URLField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.whitepaper.title}"



class LeadFieldValue(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="values")
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField()



class DownloadToken(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)




class WhitepaperPage(RoutablePageMixin, Page):
    date = models.DateField("Publish date")
    description = RichTextField()
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    client = models.ForeignKey(
        WhitepaperClient,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    categories = ParentalManyToManyField(WhitepaperCategory, blank=True)

    template = models.ForeignKey(
        WhitepaperTemplate,
        on_delete=models.PROTECT
    )

    form_schema = models.ForeignKey(
        FormSchema,
        on_delete=models.PROTECT
    )

    consent_profile = models.ForeignKey(
        ConsentProfile,
        on_delete=models.PROTECT
    )

    disclaimers = ParentalManyToManyField(DisclaimerBlock, blank=True)

    pdf_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("description"),
        FieldPanel("preview_image"),
        FieldPanel("client"),
        FieldPanel("categories"),
        FieldPanel("template"),
        FieldPanel("form_schema"),
        FieldPanel("consent_profile"),
        FieldPanel("disclaimers"),
        FieldPanel("pdf_file"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("description"),
    ]

    @route(r"^$")
    def preview(self, request):
        return render(request, self.template.preview_template, {
            "page": self,
        })

    @route(r"^landing/$")
    def landing(self, request):
        return render(request, self.template.landing_template, {
            "page": self,
        })

    @route(r"^submit/$", methods=["POST"])
    def submit(self, request):
        # create Lead
        # create LeadFieldValue
        # create DownloadToken
        # redirect to thank-you
        pass

    @route(r"^thank-you/$")
    def thank_you(self, request):
        return render(request, self.template.thankyou_template, {
            "page": self,
        })

    @route(r"^download/$")
    def download(self, request):
        # validate token
        # serve file
        pass




class WhitepaperView(models.Model):
    whitepaper = models.ForeignKey("WhitepaperPage", on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)



class DownloadEvent(models.Model):
    token = models.ForeignKey(DownloadToken, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
