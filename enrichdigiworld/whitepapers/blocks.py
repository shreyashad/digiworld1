from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock, ChoiceBlock, BooleanBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class FormFieldBlock(StructBlock):
    label = CharBlock(required=True)
    name = CharBlock(required=True, help_text="Used as the field name in the database (e.g. 'first_name')")
    field_type = ChoiceBlock(choices=[
        ('text', 'Text'),
        ('email', 'Email'),
        ('select', 'Select'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
        ('heading', 'Heading'),
    ], default='text')
    required = BooleanBlock(default=True, required=False)
    placeholder = CharBlock(required=False)
    choices = ListBlock(StructBlock([
        ('label', CharBlock()),
        ('value', CharBlock()),
    ]), required=False, help_text="Only used for Select and Radio fields")

    class Meta:
        icon = "form"
        label = "Form Field"



class DefaultTemplateBlock(StructBlock):
    # Hero Section
    title = CharBlock(required=True, help_text="The main heading for the page")
    intro_text = RichTextBlock(required=False, help_text="Introductory text shown in the hero section")
    background_image = ImageChooserBlock(required=False, help_text="Background image for the hero section")
    
    # Main Content
    body_content = RichTextBlock(required=False, help_text="Main body content of the whitepaper page")
    cover_image = ImageChooserBlock(required=False, help_text="Thumbnail/Cover image of the whitepaper")
    
    # Metadata
    language = CharBlock(default="ENG", help_text="e.g. ENG, GER")
    whitepaper_type = CharBlock(default="Whitepaper", help_text="e.g. Whitepaper, eBook, Case Study")
    length = CharBlock(required=False, help_text="e.g. 913.4 KB (approx)")
    
    # Form Configuration
    form_title = CharBlock(default="Download Now")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    
    # Legal & Consent
    marketing_consent = RichTextBlock(required=False, help_text="Text for the marketing agreement checkbox")
    privacy_disclaimer = RichTextBlock(required=False, help_text="Text for the privacy disclaimer shown below the form")
    form_bottom_disclaimer = RichTextBlock(required=False, help_text="Text for the disclaimer shown at the bottom of Step 2 form")
    
    # Files & Thank You
    pdf_file = DocumentChooserBlock(required=True)
    thank_you_title = CharBlock(default="Thank You!")
    thank_you_text = RichTextBlock(required=False)
    
    cta_text = CharBlock(default="Download the Whitepaper")

    class Meta:
        label = "Default Theme"
        icon = "doc-full"


class AWSTemplateBlock(StructBlock):
    # Header & Hero (Slide 1)
    logo = ImageChooserBlock(required=False)
    hero_title = CharBlock(required=True, help_text="Appears in the blue bar")
    intro_text = RichTextBlock(required=False)
    cover_image = ImageChooserBlock(required=True)
    
    # Landing Page Additionals (Slide 2)
    landing_description = RichTextBlock(required=False)
    
    # Form Configuration
    form_title = CharBlock(default="Download the eBook")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    
    # Footer / Legal
    interest_question = CharBlock(required=False, help_text="e.g. 'I am completing this form in connection with my:'")
    interest_options = ListBlock(StructBlock([
        ('label', CharBlock()),
        ('value', CharBlock()),
    ]), required=False)
    
    consent_text = RichTextBlock(required=False)
    privacy_notice = RichTextBlock(required=False)
    
    # Files & Thank You
    pdf_file = DocumentChooserBlock(required=True)
    thank_you_title = CharBlock(default="Thank You!")
    thank_you_text = RichTextBlock(required=False)
    
    cta_text = CharBlock(default="Download the eBook")

    class Meta:
        label = "AWS Theme"
        icon = "doc-full"




class LenovoTemplateBlock(StructBlock):
    logo_left = ImageChooserBlock(required=False)
    logo_right = ImageChooserBlock(required=False)
    title = CharBlock(required=True)
    preview_banner = ImageChooserBlock(required=False)
    description_paragraph = RichTextBlock(
        required=False,
        help_text="Additional description paragraph"
    )
    intro_text = RichTextBlock()
    highlights = ListBlock(CharBlock(), required=False)
    landing_image = ImageChooserBlock(
        required=False,
        help_text="Image shown on landing page (left column)"
    )

    landing_description = RichTextBlock(
        required=False,
        help_text="Text shown above the landing page image"
    )
    # Form Configuration
    form_title = CharBlock(default="Download Now")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    consent_text = RichTextBlock(
        required=False,
        help_text="Marketing consent text"
    )

    privacy_notice = RichTextBlock(
        required=False,
        help_text="Privacy disclaimer text"
    )
    # Files & Thank You
    pdf_file = DocumentChooserBlock(required=True)
    thank_you_title = CharBlock(default="Thank You!")
    thank_you_text = RichTextBlock(required=False)
    
    cta_text = CharBlock(default="Download Now")

    class Meta:
        label = "Lenovo Theme"
        icon = "doc-full"




class LenovoTemplateBaseBlock(StructBlock):
    title = CharBlock(required=True)
    preview_banner = ImageChooserBlock(required=False)
    description_paragraph = RichTextBlock(
        required=False,
        help_text="Additional description paragraph"
    )
    intro_text = RichTextBlock(required=False)
    highlights = ListBlock(CharBlock(), required=False)
    landing_image = ImageChooserBlock(
        required=False,
        help_text="Image shown on landing page (left column)"
    )
    landing_description = RichTextBlock(
        required=False,
        help_text="Text shown above the landing page image"
    )
    form_title = CharBlock(default="Download Now")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    consent_text = RichTextBlock(
        required=False,
        help_text="Marketing consent text"
    )
    privacy_notice = RichTextBlock(
        required=False,
        help_text="Privacy disclaimer text"
    )
    pdf_file = DocumentChooserBlock(required=True)
    thank_you_title = CharBlock(default="Thank You!")
    thank_you_text = RichTextBlock(required=False)
    cta_text = CharBlock(default="Download Now")



class LenovoTemplate1Block(LenovoTemplateBaseBlock):
    logo_left = ImageChooserBlock(required=False)
    logo_right = ImageChooserBlock(required=False)

    class Meta:
        label = "Lenovo Template 1"
        icon = "doc-full"


class LenovoTemplate2Block(LenovoTemplateBaseBlock):
    logo_left = ImageChooserBlock(required=False)
    logo_right = ImageChooserBlock(required=False)
    
    class Meta:
        label = "Lenovo Template 2"
        icon = "doc-full"


class LenovoTemplate3Block(LenovoTemplateBaseBlock):
    logo_left = ImageChooserBlock(required=False)
    
    class Meta:
        label = "Lenovo Template 3"
        icon = "doc-full"


