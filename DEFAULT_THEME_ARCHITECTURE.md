# DEFAULT THEME - ARCHITECTURE DIAGRAM

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENRICHDIGIWORLD WHITEPAPER                          │
│                          DEFAULT THEME SYSTEM                               │
└─────────────────────────────────────────────────────────────────────────────┘

                            ┌──────────────────┐
                            │  USER BROWSER    │
                            └────────┬─────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ↓                                 ↓
          ┌──────────────────┐           ┌──────────────────┐
          │   GET Request    │           │  POST Request    │
          │  /whitepaper/    │           │  Form Submit     │
          └────────┬─────────┘           └────────┬─────────┘
                   │                              │
                   └──────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Django Wagtail Server     │
                    │  whitepapers/models.py     │
                    │  WhitepaperPage.serve()    │
                    └─────────────┬──────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ↓                         ↓                         ↓
   ┌─────────────┐         ┌─────────────┐         ┌──────────────┐
   │   Step 1    │         │   Step 2    │         │   Step 3     │
   │   Email     │         │  Full Form  │         │ Thank You    │
   │Verification │         │  Submission │         │   Page       │
   └──────┬──────┘         └──────┬──────┘         └───────┬──────┘
          │                       │                        │
          ↓                       ↓                        ↓
   ┌────────────────┐     ┌────────────────┐     ┌──────────────┐
   │  Session Set   │     │  Validation    │     │  Redirect    │
   │  verified_    │     │  All Fields    │     │  to Thank    │
   │  email        │     │  Save to DB    │     │  You Page    │
   └────────────────┘     └────────────────┘     └──────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEMPLATE RENDERING                                  │
└─────────────────────────────────────────────────────────────────────────────┘

FILE: whitepapers/templates/whitepapers/themes/default/whitepaper_page.html
      (432 lines, responsive Bootstrap grid)

                        Container (py-5)
                              │
                ┌─────────────┴──────────────┐
                │                            │
        ┌───────▼────────┐          ┌───────▼───────┐
        │  LEFT SECTION  │          │  RIGHT SECTION│
        │  col-md-7      │          │  col-md-5     │
        │  (58% width)   │          │  (42% width)  │
        └───────┬────────┘          └───────┬───────┘
                │                           │
        ┌───────┴────────────┐      ┌────────┴───────┐
        │                    │      │                │
        ▼                    ▼      ▼                ▼
    ┌─────────────┐  ┌──────────┐ ┌──────────┐  ┌─────────────┐
    │ Whitepaper  │  │ THREE    │ │ Cover    │  │ Document    │
    │ Title       │  │ FORM     │ │ Image    │  │ Details     │
    │ Author      │  │ STATES   │ │ (or      │  │ Date        │
    │ Summary     │  │          │ │ placeholder)  │ Language    │
    └─────────────┘  └──────────┘ │          │  │ Type        │
                                   └──────────┘  │ File Size   │
                                                 └─────────────┘

    FORM STATES:
    │
    ├─ STATE 1 (email_verification=True, verified_email=None)
    │  └─ Email field only + "Verify Email" button
    │
    ├─ STATE 2 (email_verification=False, verified_email={email})
    │  └─ All fields (email pre-filled + rest) + "Download" button
    │
    └─ STATE 3 (form_submitted=True)
       └─ "Thank you!" + auto-redirect


┌─────────────────────────────────────────────────────────────────────────────┐
│                      SESSION STATE MACHINE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    [INITIAL STATE]
                          │
                          ▼
              email_verification: True
              verified_email: None
              form_submitted: False
                          │
                          │ User enters email + clicks "Verify Email"
                          │ [POST request]
                          ▼
              ┌──────────────────────────┐
              │ Backend validates email  │
              │ Sets: verified_email     │
              │ Sets: email_verification │
              │       to False           │
              └──────────────┬───────────┘
                             │
                             ▼
              email_verification: False
              verified_email: user@company.com
              form_submitted: False
                             │
                             │ Template reloads with new context
                             │ User sees full form with pre-filled email
                             │
                             │ User fills fields + clicks "Download"
                             │ [POST request]
                             ▼
              ┌──────────────────────────┐
              │ Backend validates form   │
              │ Saves to database        │
              │ Clears session vars      │
              │ Sets: form_submitted=True│
              └──────────────┬───────────┘
                             │
                             ▼
              form_submitted: True
                             │
                             │ Template shows thank you
                             │ JavaScript auto-redirects
                             │ to thank you page
                             ▼
                        [COMPLETE]


┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATABASE STORAGE                                       │
└─────────────────────────────────────────────────────────────────────────────┘

WhitepaperPage Model
├─ design_template: 'default' / 'modern' / 'classic'
├─ date: DateField
├─ summary: TextField
├─ cover_image: ImageField
├─ whitepaper_pdf: DocumentField
├─ author: ForeignKey(WhitepaperAuthor)
├─ categories: ManyToManyField(WhitepaperCategory)
├─ thank_you_text: RichTextField
└─ Form Configuration:
   ├─ to_address: CharField
   ├─ from_address: CharField
   ├─ subject: CharField
   └─ form_fields: InlinePanel
      ├─ label: CharField
      ├─ field_type: CharField
      ├─ required: BooleanField
      ├─ help_text: TextField
      └─ sort_order: IntegerField

WhitepaperFormSubmission
├─ page: ForeignKey(WhitepaperPage)
├─ submit_time: DateTimeField
├─ form_data: JSONField
└─ ... (inherited from AbstractFormSubmission)


┌─────────────────────────────────────────────────────────────────────────────┐
│                    FORM FIELD TYPES & RENDERING                             │
└─────────────────────────────────────────────────────────────────────────────┘

Field Type          HTML Rendering              CSS Classes
─────────────────────────────────────────────────────────────────────────────
Text                <input type="text">         form-control
Email               <input type="email">        form-control
Textarea            <textarea></textarea>       form-control
Select              <select></select>           form-control
Radio Button        <input type="radio">        form-check-input
Checkbox            <input type="checkbox">     form-check-input

All fields support:
├─ Required/optional marking
├─ Help text display
├─ Error messages
└─ Bootstrap styling


┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER FLOW DIAGRAM                                    │
└─────────────────────────────────────────────────────────────────────────────┘

START: User visits whitepaper URL
  │
  ├─ Browser makes GET request
  │
  └─▶ Django: WhitepaperPage.serve() called
       │
       ├─ Check session state
       │
       ├─ IF email not verified:
       │  └─ Render template with STATE 1 (email only)
       │     User sees:
       │     ┌──────────────────────┐
       │     │ Verify Your Email    │
       │     │ [Email Input]        │
       │     │ [Verify Button]      │
       │     └──────────────────────┘
       │
       └─ Browser displays form
          │
          User fills email: john@company.com
          User clicks "Verify Email"
          │
          ├─ Browser makes POST request
          │
          └─▶ Django: Form POST handler
              │
              ├─ Validate email format
              ├─ Store in session
              ├─ Render same template with STATE 2
              │
              └─ Browser displays form
                 │
                 User sees:
                 ┌──────────────────────┐
                 │ Tell us about you    │
                 │ [Email - prefilled]  │
                 │ [First Name]         │
                 │ [Company]            │
                 │ [Job Title]          │
                 │ [Industry dropdown]  │
                 │ [Download Button]    │
                 └──────────────────────┘
                 │
                 User fills fields
                 User clicks "Download"
                 │
                 ├─ Browser makes POST request
                 │
                 └─▶ Django: Form POST handler
                     │
                     ├─ Validate all fields
                     ├─ Save to database
                     ├─ Clear session
                     ├─ Render STATE 3
                     │
                     └─ Browser displays:
                        ┌──────────────────────┐
                        │ ✓ Thank you!         │
                        │   Redirecting...     │
                        │                      │
                        │ (1.5 second delay)   │
                        └──────────────────────┘
                        │
                        └─▶ Auto-redirect to thank you page
                            │
                            User can download PDF
                            │
                            END

