from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

def serve(self, request):
    """
    Two-step gated download flow:
    Step 1: Email verification
    Step 2: Full form submission
    """

    # ---- 0. Ungated whitepaper ----
    if not self.is_gated:
        context = self.get_context(request)
        context["download_url"] = self.whitepaper_pdf.url if self.whitepaper_pdf else None
        return render(request, self.get_template(request), context)

    # ---- 1. Session state ----
    email_verify_key = f"{EMAIL_VERIFY_KEY}_{self.id}"
    verified_email_key = f"{VERIFIED_EMAIL_KEY}_{self.id}"

    verified_email = request.session.get(verified_email_key)
    email_verification = not bool(verified_email)

    context = self.get_context(request)
    form = None

    # ---- 2. POST request ----
    if request.method == "POST":
        form = self.get_form(request.POST, page=self, user=request.user)

        # ===== STEP 1: Email verification =====
        if email_verification:
            if form.is_valid():
                email = form.cleaned_data.get("email")

                if not email:
                    form.add_error("email", "Email is required.")
                else:
                    request.session[verified_email_key] = email
                    request.session.modified = True

                    # Move to step 2 with pre-filled email
                    form = self.get_form(
                        page=self,
                        user=request.user,
                        initial={"email": email},
                    )
                    context.update({
                        "form": form,
                        "email_verification": False,
                        "form_submitted": False,
                    })
                    return render(request, self.get_template(request), context)

        # ===== STEP 2: Full form submission =====
        else:
            if form.is_valid():
                self.process_form_submission(form)

                # Clear session
                request.session.pop(verified_email_key, None)
                request.session.modified = True

                # Redirect to thank-you page if configured
                if self.thank_you_page:
                    return redirect(self.thank_you_page.url)

                context.update({
                    "form": form,
                    "email_verification": False,
                    "form_submitted": True,
                    "download_url": self.whitepaper_pdf.url if self.whitepaper_pdf else None,
                })
                return render(request, self.get_template(request), context)

    # ---- 3. GET request ----
    if verified_email:
        form = self.get_form(
            page=self,
            user=request.user,
            initial={"email": verified_email},
        )
        email_verification = False
    else:
        form = self.get_form(page=self, user=request.user)

    # ---- 4. Final render ----
    context.update({
        "form": form,
        "email_verification": email_verification,
        "form_submitted": False,
    })

    return render(request, self.get_template(request), context)
-----------
def serve(self, request):
        """
        Handle two-step email verification form flow:
        Step 1: Email verification only
        Step 2: Full form after email verified
        Step 3: Thank you page after submission
        """
        from django.shortcuts import render
        
        # Session keys for state management
        email_verify_key = f'email_verification_{self.id}'
        verified_email_key = f'verified_email_{self.id}'
        
        # Initialize context
        context = self.get_context(request)
        
        # Determine current form state
        email_verification = request.session.get(email_verify_key, True)
        verified_email = request.session.get(verified_email_key, None)
        form_submitted = False
        
        if request.method == 'POST':
            # Get form from POST data
            form = self.get_form(request.POST, page=self, user=request.user)
            
            # ===== STEP 1: Email Verification =====
            if email_verification and not verified_email:
                # In step 1, we only validate the email field
                try:
                    if form.is_valid():
                        # Extract email from form
                        email = form.cleaned_data.get('email')
                        
                        if email:
                            # Store verified email in session
                            request.session[verified_email_key] = email
                            request.session[email_verify_key] = False
                            request.session.modified = True
                            
                            # Create fresh form for step 2 with pre-filled email
                            form = self.get_form(
                                page=self, 
                                user=request.user, 
                                initial={'email': email}
                            )
                            
                            context['form'] = form
                            context['email_verification'] = False
                            context['form_submitted'] = False
                            return render(request, self.get_template(request), context)
                except Exception as e:
                    # If validation fails, show errors and stay on step 1
                    context['form'] = form
                    context['email_verification'] = True
                    context['form_submitted'] = False
                    return render(request, self.get_template(request), context)
            
            # ===== STEP 2: Full Form Submission =====
            elif not email_verification and verified_email:
                if form.is_valid():
                    try:
                        # Process form submission and send email
                        self.process_form_submission(form)
                        
                        # Clear session after successful submission
                        if verified_email_key in request.session:
                            del request.session[verified_email_key]
                        if email_verify_key in request.session:
                            del request.session[email_verify_key]
                        request.session.modified = True
                        
                        # Show thank you and prepare redirect
                        form_submitted = True
                        context['form'] = form
                        context['form_submitted'] = True
                        context['email_verification'] = False
                        context['download_url'] = self.whitepaper_pdf.url if self.whitepaper_pdf else None
                        return render(request, self.get_template(request), context)
                    
                    except Exception as e:
                        # If submission fails, show error but keep form data
                        context['form'] = form
                        context['form_submitted'] = False
                        context['email_verification'] = False
                        return render(request, self.get_template(request), context)
                else:
                    # Form validation failed, show errors
                    context['form'] = form
                    context['form_submitted'] = False
                    context['email_verification'] = False
                    return render(request, self.get_template(request), context)
        
        else:
            # ===== GET REQUEST =====
            # Determine which step to show based on session state
            if verified_email:
                # User already verified email, show step 2 form with pre-filled email
                form = self.get_form(
                    page=self, 
                    user=request.user, 
                    initial={'email': verified_email}
                )
                email_verification = False
            else:
                # Show step 1 - email only
                form = self.get_form(page=self, user=request.user)
                email_verification = True
        
        # ===== PREPARE CONTEXT FOR RENDERING =====
        context['form'] = form
        context['email_verification'] = email_verification
        context['form_submitted'] = form_submitted
        return render(request, self.get_template(request), context)
-----------
from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from wagtail.models import Page, TranslatableMixin
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from modelcluster.fields import ParentalKey, ParentalManyToManyField
# Create your models here.


# =====================================================
# CONSTANTS
# =====================================================
BLOCKED_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "aol.com",
    "outlook.com", "protonmail.com", "icloud.com",
    "mail.com", "gmx.com", "yandex.com", "zoho.com", "msn.com",
]

LAYOUT_CHOICES = [
    ("standard", "Standard Layout (Multi-step form)"),
    ("simple", "AWS Simple Layout (Single-step form)"),
]




# =====================================================
# SNIPPETS
# =====================================================
@register_snippet
class Client(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def _str_(self):
        return self.name




@register_snippet
class WhitepaperCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Whitepaper Categories"

    def _str_(self):
        return self.name



# =====================================================
# CUSTOM FORM FIELD
# =====================================================
class CustomWhitepaperFormField(TranslatableMixin, AbstractFormField):
    page = ParentalKey(
        "whitepapers.WhitepaperPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )

    placeholder = models.CharField(max_length=255, blank=True)
    display_label = models.BooleanField(default=True)
    floating_label = models.BooleanField(default=False)
    custom_css_class = models.CharField(max_length=255, blank=True)
    form_step = models.PositiveIntegerField(default=1)

    panels = AbstractFormField.panels + [
        FieldPanel("placeholder"),
        FieldPanel("display_label"),
        FieldPanel("floating_label"),
        FieldPanel("custom_css_class"),
        FieldPanel("form_step"),
    ]



# =====================================================
# INDEX PAGE
# =====================================================
class WhitepaperIndexPage(Page):
    subpage_types = ["whitepapers.WhitepaperPage"]

    def get_context(self, request):
        context = super().get_context(request)

        whitepapers = (
            WhitepaperPage.objects
            .live()
            .descendant_of(self)
            .select_related("client", "preview_image")
            .prefetch_related("categories")
        )

        category_slug = request.GET.get("category")
        if category_slug:
            whitepapers = whitepapers.filter(categories__slug=category_slug)

        search_query = request.GET.get("q")
        if search_query:
            whitepapers = whitepapers.search(search_query)

        context["whitepapers"] = whitepapers
        context["categories"] = WhitepaperCategory.objects.all()
        return context


# =====================================================
# WHITEPAPER PAGE
# =====================================================
class WhitepaperPage(AbstractEmailForm):
    parent_page_types = ["whitepapers.WhitepaperIndexPage"]
    template = "whitepapers/whitepaper_page.html"

    template_choice = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default="standard",
    )

    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="whitepapers",
    )

    description = RichTextField(blank=True)

    categories = ParentalManyToManyField(
        WhitepaperCategory,
        blank=True,
        related_name="+",
    )

    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    downloadable_file = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    thank_you_page = models.ForeignKey(
        "whitepapers.WhitepaperThankYouPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    disclaimer = RichTextField(blank=True)
    published_date = models.DateField(default=timezone.now)

    form_heading = models.CharField(
        max_length=255,
        default="Download the Whitepaper",
    )

    form_button_label = models.CharField(
        max_length=100,
        default="Download",
    )

    search_fields = Page.search_fields + [
        index.SearchField("title", partial_match=True),
        index.SearchField("description", partial_match=True),
    ]

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("template_choice"),
        FieldPanel("client"),
        FieldPanel("description"),
        FieldPanel("preview_image"),
        FieldPanel("categories"),
        FieldPanel("downloadable_file"),
        FieldPanel("published_date"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("form_heading"),
        FieldPanel("form_button_label"),
        FieldPanel("disclaimer"),
        FieldPanel("thank_you_page"),
    ]

    # -------------------------------------------------
    # FORM HELPERS
    # -------------------------------------------------
    
    def get_form_fields(self):
        return self.form_fields.all().order_by('sort_order')


    def get_template(self, request, *args, **kwargs):
        print(f"Using template: {self.template_choice}")
        if self.template_choice == 'simple':
            return 'whitepapers/whitepaper_simple.html'
        return 'whitepapers/whitepaper_page.html'

    
    def get_form_class(self):
        form_class = super().get_form_class()

        for name, field in form_class.base_fields.items():
            try:
                form_field = self.form_fields.get(clean_name=name)
            except CustomWhitepaperFormField.DoesNotExist:
                continue

            # Add placeholder if provided
            if form_field.placeholder:
                field.widget.attrs['placeholder'] = form_field.placeholder

            # Add custom CSS class if needed
            css_classes = field.widget.attrs.get('class', '')
            if form_field.custom_css_class:
                css_classes += f" {form_field.custom_css_class}"
            field.widget.attrs['class'] = css_classes.strip()

            # Add '*' to label if required
            if field.required and form_field.display_label:
                field.label = f"{field.label} *"

            # Handle label visibility
            if not form_field.display_label:
                field.label = ''

            # Special handling for dropdowns
            if field.widget._class.name_ in ['Select', 'SelectMultiple']:
                if not form_field.placeholder:
                    # If no custom placeholder, use the label as placeholder
                    field.widget.choices = [('', f"Select {field.label or name}")] + list(field.widget.choices)
                else:
                    # If placeholder is defined, use that as first option
                    field.widget.choices = [('', form_field.placeholder)] + list(field.widget.choices)

        return form_class

    def get_client_ip(self, request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return forwarded and forwarded.split(',')[0] or request.META.get('REMOTE_ADDR')


    

    # -------------------------------------------------
    # SERVE OVERRIDE (SAFE)
    # -------------------------------------------------
    def serve(self, request):
        print(f"Serving WhitepaperPage: {self.title}")
        session = request.session
        verified_flag = f'whitepaper_email_verified_{self.pk}'
        submitted_flag = f'whitepaper_submitted_{self.pk}'

        # Find the email field name dynamically
        email_field_name = None
        for form_field in self.form_fields.all():
            if form_field.field_type == 'email':
                email_field_name = form_field.clean_name
                break

        if not email_field_name:
            raise ValueError("This form does not contain an email field.")

        # For 'simple' template: single-step form
        if self.template_choice == 'simple':
            if request.method == 'POST':
                form = self.get_form(request.POST, page=self)
                form.request = request
                if form.is_valid():
                    # Process form submission directly
                    self.process_form_submission(form, email_field_name)
                    session[submitted_flag] = True
                    # Redirect to thank-you page if set
                    if self.thank_you_page:
                        return redirect(f"{self.thank_you_page.url}?id={self.pk}")
                else:
                        return redirect(request.path)
            else:
                form = self.get_form(page=self)

            context = self.get_context(request)
            context.update({
                'form': form,
		        'form_submitted': session.get(submitted_flag, False),
                'email_field_name': email_field_name,
                'email_verification': False,  # no email step here
            })
            return TemplateResponse(request, self.get_template(request), context)

        # For other templates (e.g., 'standard'): multi-step form
        else:
            # Step 1: Email verification not done yet
            if not session.get(verified_flag):
                if request.method == 'POST':
                    form = self.get_form(request.POST, page=self)
                    form.request = request
                    # Only keep the email field visible
                    form.fields = {email_field_name: form.fields[email_field_name]}
                    email = form.data.get(email_field_name, '').lower()

                    # Block certain emails if needed
                    if any(email.endswith("@" + domain) for domain in BLOCKED_EMAIL_DOMAINS):
                        form.add_error(email_field_name, "Please use your work email address.")
                    elif form.is_valid():
                        session[verified_flag] = True
                        session['verified_email'] = email
                        return redirect(request.path)
                else:
                    form = self.get_form(page=self)
                    form.fields = {email_field_name: form.fields[email_field_name]}

                context = self.get_context(request)
                context.update({
                    'form': form,
                    'email_verification': True,
                    'form_submitted': False,
                    'email_field_name': email_field_name,
                })
                return TemplateResponse(request, self.get_template(request), context)

            # Step 2: Full form submission after email verified
            else:
                if request.method == 'POST' and not session.get(submitted_flag):
                    form = self.get_form(request.POST, page=self)
                    form.request = request
                    if form.is_valid():
                        self.process_form_submission(form, email_field_name)
                        session[submitted_flag] = True
                        if self.thank_you_page:
                            return redirect(f"{self.thank_you_page.url}?id={self.pk}")
                        return redirect(request.path)
                else:
                    form = self.get_form(page=self)
                    # Prefill email as readonly
                    form.initial[email_field_name] = session.get('verified_email', '')
                    form.fields[email_field_name].widget.attrs.update({
                        'readonly': True,
                        'class': 'form-control-plaintext'
                    })

                context = self.get_context(request)
                context.update({
                    'form': form,
                    'email_verification': False,
                    'form_submitted': session.get(submitted_flag, False),
                    'email_field_name': email_field_name,
                })
                return TemplateResponse(request, self.get_template(request), context)

    def get_download_url(self):
        return reverse("whitepaper_download", args=[self.pk])
    
    def process_form_submission(self, form, email_field_name):
        submission = super().process_form_submission(form)

        # Extract field values
        data = form.cleaned_data

        Lead.objects.create(
            whitepaper=self,
            client=self.client,
            name=data.get('name', 'Anonymous'),
            email=data.get(email_field_name),
            company=data.get('company', ''),
            phone=data.get('phone', ''),
            submission_data=data,
        )

        return submission

    def get_email_field_name(self):
        for form_field in self.form_fields.all():
            if form_field.field_type == 'email':
                return form_field.clean_name
        return None

# =====================================================
# LEAD MODEL (NOT A SNIPPET)
# =====================================================
class Lead(models.Model):
    whitepaper = models.ForeignKey(
        WhitepaperPage,
        on_delete=models.CASCADE,
        related_name="leads",
    )
    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    submission_data = models.JSONField(default=dict)
    submitted_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.name} ({self.email})"

# =====================================================
# THANK YOU PAGE
# =====================================================
class WhitepaperThankYouPage(Page):
    template = "whitepapers/whitepaper_thank_you_page.html"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        whitepaper_id = request.GET.get("id")
        context["whitepaper"] = WhitepaperPage.objects.filter(id=whitepaper_id).first()
        return context
    




class WhitepaperFormField(AbstractFormField):
    page = ParentalKey('WhitepaperPage', on_delete=models.CASCADE, related_name='form_fields')


class WhitepaperPage(AbstractEmailForm):
    TEMPLATE_CHOICES = [
        ('default', 'Default Theme'),
        ('modern', 'Modern Theme'),
        ('classic', 'Classic Theme'),
    ]
    
    design_template = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default='default',
        help_text="Select the design layout for this whitepaper"
    )

    date = models.DateField("Post date")
    summary = models.TextField(blank=True, help_text='Summary for listing pages')
    
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    whitepaper_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The gated PDF file"
    )

    is_gated = models.BooleanField(default=True, help_text="If checked, users must fill a form to access the PDF")

    categories = ParentalManyToManyField('whitepapers.WhitepaperCategory', blank=True)
    
    client = models.ForeignKey(
        'whitepapers.WhitepaperClient',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='whitepapers',
        help_text="Author or publisher of this whitepaper"
    )

    disclaimer = RichTextField(
        blank=True,
        help_text="Optional disclaimer text to display on the form"
    )

    thank_you_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Page to redirect to after form submission"
    )

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('body'),
    ]

    # Email fields for form submissions (inherited from AbstractEmailForm)
    to_address = models.CharField(
        verbose_name='to address', max_length=255, blank=True,
        help_text="Optional: email address to send form submissions to"
    )
    from_address = models.CharField(verbose_name='from address', max_length=255, blank=True)
    subject = models.CharField(verbose_name='subject', max_length=255, blank=True)
    
    thank_you_text = RichTextField(
        blank=True,
        default="Thank you for downloading our whitepaper!",
        help_text="Custom message to display on the thank you page"
    )

    content_panels = Page.content_panels + [
        FormSubmissionsPanel(),
        
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('client'),
        ], heading="Meta Information"),
        
        FieldPanel('design_template'),
        
        MultiFieldPanel([
            FieldPanel('preview_image'),
            FieldPanel('summary'),
            FieldPanel('body'),
        ], heading="Content"),

        MultiFieldPanel([
            FieldPanel('is_gated'),
            FieldPanel('whitepaper_pdf'),
        ], heading="Gated Asset"),
        
        MultiFieldPanel([
            InlinePanel('form_fields', label="Form fields"),
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
            FieldPanel('thank_you_text'),
            FieldPanel('disclaimer'),
            FieldPanel('thank_you_page'),
        ], heading="Lead Capture Form (for gated whitepapers)"),
    ]

    parent_page_types = ['WhitepaperIndexPage']

    def get_template(self, request, *args, **kwargs):
        # Dynamic template selection based on the design_template field
        template_name = f"whitepapers/themes/{self.design_template}/whitepaper_page.html"
        return template_name

   
    def serve(self, request):
        """
        Two-step gated download flow:
        Step 1: Email verification
        Step 2: Full form submission
        """

        # ---- 0. Ungated whitepaper ----
        if not self.is_gated:
            context = self.get_context(request)
            context["download_url"] = self.whitepaper_pdf.url if self.whitepaper_pdf else None
            return render(request, self.get_template(request), context)

        # ---- 1. Session state ----
        email_verify_key = f'email_verification_{self.id}'
        verified_email_key = f'verified_email_{self.id}'
       
        verified_email = request.session.get(verified_email_key)
        email_verification = not bool(verified_email)

        context = self.get_context(request)
        form = None

        # ---- 2. POST request ----
        if request.method == "POST":
            form = self.get_form(request.POST, page=self, user=request.user)

            # ===== STEP 1: Email verification =====
            if email_verification:
                if form.is_valid():
                    email = form.cleaned_data.get("email")

                    if not email:
                        form.add_error("email", "Email is required.")
                    else:
                        request.session[verified_email_key] = email
                        request.session.modified = True

                        # Move to step 2 with pre-filled email
                        form = self.get_form(
                            page=self,
                            user=request.user,
                            initial={"email": email},
                        )
                        context.update({
                            "form": form,
                            "email_verification": False,
                            "form_submitted": False,
                        })
                        return render(request, self.get_template(request), context)

            # ===== STEP 2: Full form submission =====
            else:
                if form.is_valid():
                    self.process_form_submission(form)

                    # Clear session
                    request.session.pop(verified_email_key, None)
                    request.session.modified = True

                    # Redirect to thank-you page if configured
                    if self.thank_you_page:
                        return redirect(self.thank_you_page.url)

                    context.update({
                        "form": form,
                        "email_verification": False,
                        "form_submitted": True,
                        "download_url": self.whitepaper_pdf.url if self.whitepaper_pdf else None,
                    })
                    return render(request, self.get_template(request), context)

        # ---- 3. GET request ----
        if verified_email:
            form = self.get_form(
                page=self,
                user=request.user,
                initial={"email": verified_email},
            )
            email_verification = False
        else:
            form = self.get_form(page=self, user=request.user)

        # ---- 4. Final render ----
        context.update({
            "form": form,
            "email_verification": email_verification,
            "form_submitted": False,
        })

        return render(request, self.get_template(request), context)
    

    def get_email_field_name(self):
        for form_field in self.form_fields.all():
            if form_field.field_type == 'email':
                return form_field.clean_name
        return None