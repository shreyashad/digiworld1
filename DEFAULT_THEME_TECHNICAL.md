# Default Theme - Form Flow Technical Details

## Template Structure

### Layout
```html
<div class="container py-5 whitepaper-page">
  <div class="row g-5 align-items-start">
    
    <!-- LEFT SECTION: col-md-7 (58% width) -->
    <div class="col-md-7">
      - Whitepaper Title
      - Published By (Author)
      - Summary
      - THREE FORM STATES (see below)
      - Related Categories
    </div>
    
    <!-- RIGHT SECTION: col-md-5 (42% width) -->
    <div class="col-md-5 text-center">
      - Cover Image
      - Document Details (date, language, type, file size)
    </div>
    
  </div>
  
  <!-- StreamField Content -->
  {% if page.body %}
    - Document Preview (headings, paragraphs, images)
  {% endif %}
</div>
```

---

## Three Form States

### STATE 1: Email Verification Only
**Condition:** `{% if not form_submitted and email_verification %}`

```html
<div style="background-color: rgb(0, 48, 87);" class="text-white p-4 rounded mt-4 shadow-sm">
  <h3 class="mb-3">Verify Your Work Email <i class="bi bi-envelope-check"></i></h3>

  <form method="POST" novalidate>
    {% csrf_token %}
    
    <!-- ONLY EMAIL FIELD IS SHOWN -->
    {% for field in form.visible_fields %}
      {% if field.name == 'email' %}
        <div class="mb-3">
          {{ field.label_tag }}
          {{ field|add_class:"form-control" }}
          {% for error in field.errors %}
            <small class="text-danger">{{ error }}</small>
          {% endfor %}
        </div>
      {% endif %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary mt-2">Verify Email</button>
  </form>

  <p class="mt-3 small text-white">
    Please use your company email. Public domains (e.g., Gmail, Yahoo) are not allowed.
  </p>
</div>
```

**What Happens:**
1. User sees ONLY email input field
2. User clicks "Verify Email"
3. Django form processes:
   - Backend validates email format
   - Stores email in session: `request.session['verified_email_{page_id}']`
   - Sets `email_verification_{page_id}` to False
4. Page reloads → **STATE 2 is now shown**

---

### STATE 2: Full Form After Email Verified
**Condition:** `{% elif not form_submitted %}`

```html
<div style="background-color: rgb(0, 48, 87);" class="text-white p-4 rounded mt-4 shadow-sm">
  <h3 class="mb-3">Tell us about yourself <i class="bi bi-download"></i></h3>

  <form method="POST">
    {% csrf_token %}
    
    <!-- ALL FORM FIELDS ARE RENDERED -->
    {% for field in form.visible_fields %}
    
      <!-- RADIO BUTTONS -->
      {% if field.field.widget.input_type == "radio" %}
        <div class="form-group mb-3">
          <label>{{ field.label }}</label>
          {% for subwidget in field %}
            <div class="form-check">
              {{ subwidget.tag }}
              <label class="form-check-label" for="{{ subwidget.id_for_label }}">
                {{ subwidget.choice_label }}
              </label>
            </div>
          {% endfor %}
          {% for error in field.errors %}
            <div class="text-danger">{{ error }}</div>
          {% endfor %}
        </div>

      <!-- CHECKBOXES -->
      {% elif field.field.widget.input_type == "checkbox" %}
        <div class="form-check mb-3">
          {{ field|add_class:"form-check-input me-2 mt-1" }}
          <label class="form-check-label" for="{{ field.id_for_label }}">
            {{ field.label|safe }}
          </label>
          {% for error in field.errors %}
            <div class="text-danger">{{ error }}</div>
          {% endfor %}
        </div>

      <!-- TEXT, EMAIL, TEXTAREA, SELECT, ETC -->
      {% else %}
        <div class="mb-3">
          {{ field.label_tag }}
          {{ field|add_class:"form-control" }}
          
          <!-- SPECIAL MESSAGE FOR EMAIL FIELD -->
          {% if field.name == email_field_name %}
            <small class="text-warning d-block mt-1">
              This email is already verified and cannot be changed.
            </small>
          {% endif %}
          
          {% for error in field.errors %}
            <small class="text-danger">{{ error }}</small>
          {% endfor %}
        </div>
      {% endif %}
    
    {% endfor %}

    <button type="submit" class="btn btn-primary mt-2">Download</button>
  </form>

  <!-- DISCLAIMER (if configured in admin) -->
  {% if page.disclaimer %}
    <div class="mt-4 small text-white">
      {{ page.disclaimer|richtext }}
    </div>
  {% endif %}

  <p class="small text-white mt-3">
    For questions, email <a href="mailto:info@enrichdigiworld.com" class="text-info">
      info@enrichdigiworld.com
    </a>
  </p>
</div>
```

**What's Different from Step 1:**
1. Email field is **PRE-FILLED** from previous step
2. Email field has warning: "This email is already verified and cannot be changed"
3. **ALL OTHER FIELDS** are now visible (name, company, job_title, etc.)
4. Button text is "Download" (not "Verify Email")

**Field Types Rendered:**
| Type | Rendering | Example |
|------|-----------|---------|
| Text | `<input type="text" class="form-control">` | Name, Company |
| Email | `<input type="email" class="form-control">` | Email |
| Textarea | `<textarea class="form-control">` | Message |
| Radio | `.form-check` with radio buttons | Industry type |
| Checkbox | `.form-check` with checkboxes | Newsletter opt-in |
| Select | `<select class="form-control">` | Job title, Company size |

**What Happens When User Submits:**
1. User fills remaining fields
2. Clicks "Download"
3. Django form validates ALL fields
4. If valid:
   - Form data saved to database
   - Session access granted: `request.session['whitepaper_access_{page_id}'] = True`
   - Session cleared: `email_verification_{page_id}` and `verified_email_{page_id}` deleted
   - Form marked as submitted → **STATE 3 is now shown**

---

### STATE 3: Thank You & Redirect
**Condition:** `{% else %}`

```html
<div class="alert alert-success mt-4">
  Thank you! We are redirecting you shortly...
</div>

<script>
  setTimeout(function () {
    const thankYouUrl = "{{ page.thank_you_page.url }}?id={{ page.id }}";
    window.location.href = thankYouUrl;
  }, 1500);  // 1.5 seconds delay
</script>
```

**What Happens:**
1. Success message displays
2. After 1.5 seconds, automatically redirects to thank you page
3. Thank you page URL is from `page.thank_you_page` (must be configured in admin)

---

## Session Variables Used

### Storage Location
All session data is stored in user's browser session (or server-side session store)

### Variables
```python
request.session[f'email_verification_{page_id}']  
  # Type: Boolean
  # True = Show step 1 (email only)
  # False = Show step 2 (full form)
  # Default: True (first time visitor)

request.session[f'verified_email_{page_id}']
  # Type: String or None
  # Value: User's verified email address
  # Default: None (not yet verified)

request.session[f'whitepaper_access_{page_id}']
  # Type: Boolean
  # True = User has completed form, can access PDF
  # False = User hasn't submitted form yet
  # Default: False (new visitor)
```

### Cleanup
After successful form submission, session variables are deleted:
```python
del request.session[f'verified_email_{page_id}']
del request.session[f'email_verification_{page_id}']
```

---

## Admin Configuration

### Form Fields Panel
In Wagtail admin, users can:

1. **Add Fields** - Click "Add form field"
2. **Configure Each Field:**
   - Field label (shown to user)
   - Field type (text, email, checkbox, radio, select, etc.)
   - Help text
   - Required? (checkbox)
3. **Reorder Fields** - Drag-and-drop in admin
4. **Delete Fields** - Click remove button

### Example Configuration
```
Email                [Required] [Help text...]
First Name           [Required] [Help text...]
Last Name            [Required] [Help text...]
Company              [Required] [Help text...]
Job Title            [Required] [Help text...]
Industry (Dropdown)  [Required] [Help text...]
Company Size         [Optional] [Help text...]
Newsletter?          [Optional] [Help text...]
```

### What Gets Saved
When form is submitted, all field values are saved to:
- **WhitepaperFormSubmission** model
- Contains: timestamp, IP address, form data, page reference

---

## Error Handling

### Field Validation
Each field is validated according to its type:
- **Required fields:** Must not be empty
- **Email fields:** Must be valid email format
- **Specific types:** Custom validation if defined

### Error Display
```html
{% if field.errors %}
  <small class="text-danger">{{ field.errors.0 }}</small>
{% endif %}
```

Errors appear:
- Below each field
- In red text (Bootstrap `.text-danger`)
- Only the first error shown (`.0` index)

### Form Rejection
If form validation fails:
- Page reloads with same form state
- Error messages display
- User stays in Step 2 (doesn't go back to Step 1)

---

## Styling Classes

### Colors (Bootstrap)
```css
.text-white        /* White text */
.text-primary      /* Primary brand color (blue) */
.text-danger       /* Error text (red) */
.text-warning      /* Warning text (orange) */
.text-muted        /* Muted/secondary text (gray) */
.text-info         /* Info text (cyan) - links */
```

### Spacing (Bootstrap)
```css
.py-5              /* Padding vertical (large) */
.px-4              /* Padding horizontal (medium) */
.mb-3              /* Margin bottom (medium) */
.mt-4              /* Margin top (medium) */
.mt-2              /* Margin top (small) */
.g-5               /* Gap between columns (large) */
```

### Form Elements (Bootstrap)
```css
.form-control      /* Text input, select, textarea styling */
.form-check        /* Checkbox/radio container */
.form-check-input  /* Checkbox/radio input styling */
.form-check-label  /* Checkbox/radio label styling */
.form-group        /* Form group container */
```

### Alerts & Colors
```css
.alert             /* Alert container */
.alert-success     /* Green background (success) */
.btn               /* Button styling */
.btn-primary       /* Primary button color */
```

---

## Response Flow Diagram

```
GET /whitepaper/page/
  ↓
Template receives context:
  - email_verification: True/False
  - verified_email: None/'user@email.com'
  - form_submitted: False/True
  - form: Django form object
  ↓
Template checks conditions:
  
  if not form_submitted and email_verification:
    → SHOW STATE 1 (Email only)
  
  elif not form_submitted:
    → SHOW STATE 2 (Full form)
  
  else:
    → SHOW STATE 3 (Thank you)


POST /whitepaper/page/
  ↓
Backend processes:
  1. Get request.POST data
  2. Check session state
  3. Validate form based on state
  4. Update session
  5. Render same template with updated context
```

---

## Mobile Responsiveness

### Breakpoints
```css
col-md-7          /* 58% width on medium+ screens */
col-md-5          /* 42% width on medium+ screens */

/* On mobile (< 768px):   */
  col-md-7 → 100% width (full width)
  col-md-5 → 100% width (full width, below col-md-7)
```

### Form Elements on Mobile
- Input fields: 100% width
- Buttons: 100% width (full width form submission)
- Labels: Display above inputs (stacked)
- Spacing: Adjusted with Bootstrap utilities

---

## Security Features

1. **CSRF Protection**
   - `{% csrf_token %}` in every form
   - Django validates on submission

2. **Email Validation**
   - Format check (contains @ and .)
   - Can be extended with custom validators

3. **Session Security**
   - Session data stored securely (server or encrypted cookies)
   - Cleared after submission

4. **No Client-Side Bypass**
   - Step 2 validation still happens on backend
   - Email field display is just UX, validation enforced on server

