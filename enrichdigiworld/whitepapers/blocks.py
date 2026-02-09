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
    
    # Metadata
    language = CharBlock(default="ENG", help_text="e.g. ENG, GER")
    whitepaper_type = CharBlock(default="Whitepaper", help_text="e.g. Whitepaper, eBook, Case Study")
    
    # Form Configuration
    form_title = CharBlock(default="Verify Your Work Email")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    
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
    heading = CharBlock()
    subheading = CharBlock(required=False)
    background_image = ImageChooserBlock()
    intro_text = RichTextBlock()
    highlights = ListBlock(CharBlock(), required=False)
    
    # Form Configuration
    form_title = CharBlock(default="Download Now")
    form_fields = ListBlock(FormFieldBlock(), required=False)
    
    # Files & Thank You
    pdf_file = DocumentChooserBlock(required=True)
    thank_you_title = CharBlock(default="Thank You!")
    thank_you_text = RichTextBlock(required=False)
    
    cta_text = CharBlock(default="Download Now")

    class Meta:
        label = "Lenovo Theme"
        icon = "doc-full"

