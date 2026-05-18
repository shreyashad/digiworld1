from django.db import models
from django.core.exceptions import ValidationError
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from django.core.paginator import Paginator
from wagtail.models import Page, Orderable
from wagtail.images import get_image_model_string
from wagtail.fields import RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.models import ClusterableModel
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from wagtail.fields import StreamField
from .blocks import AWSTemplateBlock, LenovoTemplateBlock, DefaultTemplateBlock, LenovoTemplate1Block, LenovoTemplate2Block, LenovoTemplate3Block



def generate_unique_slug(instance, value, field_name="slug"):
    """
    Generates a unique slug for a given model instance.
    - instance: The model instance (e.g., self)
    - value: The string to slugify (e.g., self.name)
    - field_name: The name of the field to check uniqueness against (default: "slug")
    """
    from django.utils.text import slugify
    slug = slugify(value)
    if not slug:
        slug = "untitled"
        
    model = instance.__class__
    unique = slug
    counter = 1
    
    # Base queryset excluding the current instance if it already exists
    qs = model._default_manager.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
        
    while qs.filter(**{field_name: unique}).exists():
        unique = f"{slug}-{counter}"
        counter += 1
    return unique



def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Take the first IP in the list
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")




@register_snippet
class WhitepaperCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    order = models.IntegerField(default=0)

    panels = [
        FieldPanel("name"),
        FieldPanel("order"),
    ]

    search_fields = [
        index.SearchField("name"),
    ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if WhitepaperCategory.objects.exclude(id=self.id).filter(slug=self.slug).exists():
            raise ValidationError("Category with this slug already exists.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "whitepaper categories"



@register_snippet
class WhitepaperClient(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    website = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("logo"),
        FieldPanel("website"),
        FieldPanel("is_featured"),
        FieldPanel("order"),
    ]

    search_fields = [
        index.SearchField("name"),
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
        verbose_name_plural = "whitepaper clients"






class WhitepaperIndexPage(Page):
    """
    Main landing page for all whitepapers.
    Acts as:
    - SEO entry point
    - Filter/search hub
    - Marketing landing page
    """

    template = "whitepapers/whitepaper_index_page.html"

    # Hero / marketing section
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=500, blank=True)
    hero_background = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_background"),
    ]

    # Structure enforcement
    parent_page_types = ["home.HomePage"]
    subpage_types = ["whitepapers.WhitepaperPage"]

    search_fields = Page.search_fields + [
        index.SearchField("hero_title"),
        index.SearchField("hero_subtitle"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        whitepapers = (
            WhitepaperPage.objects
            .live()
            .descendant_of(self)
            .select_related("client")
            .prefetch_related("categories")
            .order_by("-date")
        )

        # Category filter
        category_slug = request.GET.get("category")
        if category_slug:
            whitepapers = whitepapers.filter(categories__slug=category_slug)

        # Search
        search_query = request.GET.get("q")
        if search_query:
            try:
                whitepapers = whitepapers.search(search_query)
            except:
                whitepapers = whitepapers.filter(title__icontains=search_query)

        # Pagination
        paginator = Paginator(whitepapers, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context.update({
            "whitepapers": page_obj,
            "categories": WhitepaperCategory.objects.order_by("order"),
            "current_category": category_slug,
            "search_query": search_query,
            "page_obj": page_obj,
        })

        return context





class WhitepaperPage(RoutablePageMixin, Page):
    """
    Core business controller for a single whitepaper funnel.
    Handles:
    preview → landing → submit → thank-you → download
    """

    # Structure enforcement
    parent_page_types = ["whitepapers.WhitepaperIndexPage"]
    subpage_types = []

    # Content
    date = models.DateField("Publish date")

    client = models.ForeignKey(
        "whitepapers.WhitepaperClient",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    categories = ParentalManyToManyField(
        "whitepapers.WhitepaperCategory",
        blank=True
    )

    # Dynamic engines
    template_content = StreamField(
        [
            ("default", DefaultTemplateBlock()),
            ("aws", AWSTemplateBlock()),
            ("lenovo", LenovoTemplateBlock()),
            ("lenovo_template2", LenovoTemplate2Block()),
            ("lenovo_template3", LenovoTemplate3Block()),
        ],
        use_json_field=True,
        min_num=1,
        max_num=1,
        help_text="Select a theme and fill in its content."
    )

    # Marketing flags
    is_featured = models.BooleanField(default=False)
    language = models.CharField(max_length=10, blank=True)

    # CMS panels
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("client"),
        FieldPanel("categories"),
        FieldPanel("template_content"),
        FieldPanel("is_featured"),
        FieldPanel("language"),
    ]

    # Search
    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("seo_title"),
    ]

    # Helpers
    def get_template_block(self):
        """Helper to get the active template block from template_content StreamField."""
        if self.template_content and len(self.template_content) > 0:
            return self.template_content[0]
        return None

    def get_preview_image(self):
        """Returns a representative image from the template block."""
        block = self.get_template_block()
        if not block or not block.value:
            return None
        return block.value.get('background_image') or block.value.get('cover_image') or block.value.get('logo') or block.value.get('background') or block.value.get("preview_banner") or block.value.get("landing_image")

    def get_summary(self):
        """Returns a representative description/summary from the template block."""
        block = self.get_template_block()
        if not block or not block.value:
            return ""
        # Try different summary field names used across themes
        val = block.value.get('description') or \
              block.value.get('intro_text') or \
              block.value.get('landing_description') or \
              block.value.get('heading') or \
              ""
        return val

    def get_card_title(self):
        """Returns a representative title for index cards."""
        block = self.get_template_block()
        if not block or not block.value:
            return self.title
        return block.value.get('title') or \
               block.value.get('hero_title') or \
               block.value.get('heading') or \
               self.title

    def get_pdf_file(self):
        """Returns the PDF document from the template block."""
        block = self.get_template_block()
        if not block:
            return None
        return block.value.get('pdf_file')

    def get_theme_template(self, template_name):
        """Helper to resolve template paths based on theme."""
        block = self.get_template_block()
        if not block:
            return f"whitepapers/{template_name}.html"
        
        theme_map = {
            'aws': 'whitepapers/themes/aws_theme/',
            'lenovo': 'whitepapers/themes/lenovo_theme/',
            'lenovo_template2': 'whitepapers/themes/lenovo_theme_template2/',
            'lenovo_template3': 'whitepapers/themes/lenovo_theme_template3/',
            'default': 'whitepapers/themes/default_theme/'
        }
        base_path = theme_map.get(block.block_type, 'whitepapers/')

        # Special casing for AWS which has distinct preview/landing
        if block.block_type == 'aws':
            if template_name == 'preview': return base_path + 'preview.html'
            if template_name == 'landing': return base_path + 'landing.html'
        
        if block.block_type == 'lenovo':
            if template_name == 'preview': return base_path + 'preview.html'
            if template_name == 'landing': return base_path + 'landing.html'
        
        if block.block_type == 'lenovo_template2':
            if template_name == 'preview': return base_path + 'preview.html'
            if template_name == 'landing': return base_path + 'landing.html'
        
        if block.block_type == 'lenovo_template3':
            if template_name == 'preview': return base_path + 'preview.html'
            if template_name == 'landing': return base_path + 'landing.html'
        
        
        # Others use whitepaper_page.html for both
        if template_name in ['preview', 'landing']:
            return base_path + 'whitepaper_page.html'
        
        # thank_you.html is common
        return base_path + template_name + '.html'

    # Validation
    def clean(self):
        super().clean()
        block = self.get_template_block()
        if block:
            if not block.value.get('pdf_file'):
                raise ValidationError({'template_content': "The selected theme must have a PDF file assigned."})

    def get_form_class(self):
        from django import forms
        fields = {}
        block = self.get_template_block()
        
        if block and 'form_fields' in block.value:
            for field_data in block.value['form_fields']:
                f_type = field_data['field_type']
                f_label = field_data['label']
                f_name = field_data['name']
                f_required = field_data.get('required', True)
                f_placeholder = field_data.get('placeholder', '')
                f_choices = field_data.get('choices', []) or []
                
                if f_type == 'heading':
                    choices = [(c['value'], c['label']) for c in f_choices]

                    field = forms.ChoiceField(
                       label=f_label,
                       required=f_required,
                       choices=[("", "Select an option")] + choices,
                        widget=forms.Select(attrs={"class": "heading-select"})
                    )
                    field.is_heading = True  # ?? custom flag
                    fields[f_name] = field

                elif f_type == 'email':
                    fields[f_name] = forms.EmailField(label=f_label, required=f_required, widget=forms.EmailInput(attrs={'placeholder': f_placeholder}))
                elif f_type == 'select' or f_type == 'radio':
                    choices = [("", f_placeholder or "Select an option")]
                    choices += [(c['value'], c['label']) for c in f_choices]
                    widget = forms.Select if f_type == 'select' else forms.RadioSelect
                    fields[f_name] = forms.ChoiceField(label=f_label, required=f_required, choices=choices, widget=widget)
                elif f_type == 'checkbox':
                    fields[f_name] = forms.BooleanField(label=f_label, required=f_required, widget=forms.CheckboxInput(), initial=False)
                else:
                    fields[f_name] = forms.CharField(label=f_label, required=f_required, widget=forms.TextInput(attrs={'placeholder': f_placeholder}))
        
        return type("WhitepaperLeadForm", (forms.Form,), fields)

    def get_form(self, data=None, initial=None):
        form_class = self.get_form_class()
        return form_class(data=data, initial=initial)

    # -------- ROUTES (Dynamic Templates) -------- #

    @route(r"^$")
    def preview(self, request):
        WhitepaperView.objects.create(
            whitepaper=self,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")
        )

        block = self.get_template_block()
        return render(
            request,
            self.get_theme_template('preview'),
            {
                "page": self,
                "block": block,
                "block_value": block.value if block else None,
                "form": self.get_form()
            }
        )

    @route(r"^landing/$")
    def landing(self, request):
        email = request.GET.get("email") or request.session.get("verified_email")
        block = self.get_template_block()
        return render(
            request,
            self.get_theme_template('landing'),
            {
                "page": self,
                "block": block,
                "block_value": block.value if block else None,
                "form": self.get_form(initial={"email": email} if email else None)
            }
        )

    @route(r"^submit/$")
    def submit(self, request):
        form = self.get_form(request.POST)
        if form.is_valid():
    # Process Lead
            ip = get_client_ip(request)
        

            lead, created = Lead.objects.get_or_create(
                whitepaper=self,
                email=form.cleaned_data.get("email"),
                defaults={
                    "ip_address": ip,
                    "country": request.META.get("HTTP_X_COUNTRY", "Unknown"),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "utm_source": request.GET.get("utm_source", ""),
                    "utm_campaign": request.GET.get("utm_campaign", ""),
                    "referer": request.META.get("HTTP_REFERER", "")
                }
            )
            
            # Save field values
            for name, value in form.cleaned_data.items():
                LeadFieldValue.objects.update_or_create(
                    lead=lead,
                    field_name=name,
                    defaults={"value": str(value)}
                )
            
            # Create Download Token
            import secrets
            from django.utils import timezone
            from datetime import timedelta
            token = secrets.token_urlsafe(32)
            DownloadToken.objects.create(
                lead=lead,
                token=token,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            
            request.session["download_token"] = token
            return redirect(self.url + self.reverse_subpage("thank_you"))
        
        return render(
            request,
            self.get_theme_template('landing'),
            {"page": self, "block": self.get_template_block(), "form": form}
        )

    @route(r"^thank-you/$")
    def thank_you(self, request):
        token = request.session.get("download_token")
        return render(
            request,
            self.get_theme_template('thank_you'),
            {
                "page": self,
                "block": self.get_template_block(),
                "download_token": token
            }
        )

    @route(r"^download/$")
    def download(self, request):
        token_str = request.GET.get("token") or request.session.get("download_token")
        if not token_str:
            return redirect(self.url)

        try:
            token = DownloadToken.objects.get(token=token_str, is_active=True)
            if not token.is_valid():
                return render(request, "whitepapers/errors/token_expired.html", {"page": self})
            
            # Log event
            DownloadEvent.objects.create(token=token)
            
            # Serve File
            block = self.get_template_block()
            pdf_file = block.value.get('pdf_file')
            if not pdf_file:
                return redirect(self.url)

            from django.http import FileResponse
            response = FileResponse(pdf_file.file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{pdf_file.title}.pdf"'
            return response

        except (DownloadToken.DoesNotExist, AttributeError):
            return redirect(self.url)


# -------- Tracking Models -------- #

class WhitepaperView(models.Model):
    whitepaper = models.ForeignKey("WhitepaperPage", on_delete=models.CASCADE, related_name="views")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("exported", "Exported"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
    ]

    whitepaper = models.ForeignKey(
        "WhitepaperPage",
        on_delete=models.CASCADE,
        related_name="leads"
    )

    email = models.EmailField()
    full_name = models.CharField(max_length=255, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField()

    utm_source = models.CharField(max_length=255, blank=True)
    utm_campaign = models.CharField(max_length=255, blank=True)
    referer = models.URLField(blank=True)

    language = models.CharField(max_length=10, blank=True)

    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #unique_together = ("whitepaper", "email")
        indexes = [
           models.Index(fields=["whitepaper", "email"]),
           models.Index(fields=["submitted_at"]),
           models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.email} - {self.whitepaper.title}"


class LeadFieldValue(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="values"
    )
    field_name = models.CharField(max_length=255, blank=True, help_text="Slug of the field from the template block")
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("lead", "field_name")

    def __str__(self):
        return f"{self.lead.email} - {self.field_name}"


class DownloadToken(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)

    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
        ]

    def is_valid(self):
        from django.utils import timezone
        return (
            self.is_active and
            not self.used and
            self.expires_at > timezone.now()
        )

    def __str__(self):
        return f"Token for {self.lead.email}"


class DownloadEvent(models.Model):
    token = models.ForeignKey(DownloadToken, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
