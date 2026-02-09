# Feature 1.2: CTA Customization System

**Feature Name:** CTA Button Customization  
**Status:** ⏳ Not Started  
**Priority:** Critical  
**Estimated Time:** 0.5 days  
**Assigned To:** GitHub Copilot

---

## 📝 Description

Allow non-technical users to customize the Call-To-Action (CTA) button on each whitepaper without touching code. Users can change:
- Button text
- Button color
- Button style
- Button position
- Target URL

---

## ✅ Acceptance Criteria

- [ ] Admin interface allows customizing CTA per whitepaper
- [ ] CTA changes appear immediately on preview
- [ ] CTA renders correctly in all 3 themes
- [ ] Invalid color codes are handled gracefully
- [ ] CTA position options include: Below Form, Sticky Footer, Right Sidebar
- [ ] Default CTA values are sensible
- [ ] CTA styling respects theme colors

---

## 🎯 CTA Customization Fields

### Model Fields to Add to WhitepaperPage

```python
# CTA Configuration
cta_button_text = CharField(
    max_length=50,
    default="Download Whitepaper",
    help_text="Text to display on the CTA button"
)

cta_button_color = CharField(
    max_length=20,
    default="#0066cc",
    help_text="Hex color code for button background"
)

cta_button_style = ChoiceField(
    choices=[
        ('solid', 'Solid'),
        ('outline', 'Outline'),
        ('gradient', 'Gradient'),
    ],
    default='solid'
)

cta_button_position = ChoiceField(
    choices=[
        ('below_form', 'Below Form'),
        ('sticky_footer', 'Sticky Footer'),
        ('right_sidebar', 'Right Sidebar'),
    ],
    default='below_form'
)

cta_button_url = URLField(
    blank=True,
    help_text="Override default PDF download URL (optional)"
)
```

---

## 📐 CTA Button Variations

### Style 1: Solid
```html
<button class="bg-[var(--cta-color)] hover:opacity-90 text-white font-bold py-3 px-8 rounded-lg transition-all">
    {{ page.cta_button_text }}
</button>
```

### Style 2: Outline
```html
<button class="border-2 border-[var(--cta-color)] text-[var(--cta-color)] font-bold py-3 px-8 rounded-lg hover:bg-[var(--cta-color)] hover:text-white transition-all">
    {{ page.cta_button_text }}
</button>
```

### Style 3: Gradient
```html
<button class="bg-gradient-to-r from-[var(--cta-color)] to-[var(--cta-color-light)] hover:shadow-lg text-white font-bold py-3 px-8 rounded-lg transition-all">
    {{ page.cta_button_text }}
</button>
```

---

## 🏗️ Implementation Plan

### Step 1: Update WhitepaperPage Model
- Add 5 new fields as specified above
- Add panels to content_panels in admin
- Add default values

### Step 2: Update Templates
- Pass CTA variables to context
- Update all 3 theme templates to use CTA customization
- Add CSS variables for dynamic coloring

### Step 3: Add Admin UI
- Create preview of CTA in admin
- Add color picker for easy selection
- Add form to test CTA text

### Step 4: Test
- Test CTA customization in all themes
- Test color validation
- Test form submission with custom CTA

---

## 🔧 Files to Create/Modify

**Modify:**
- `enrichdigiworld/whitepapers/models.py` - Add CTA fields
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/default/whitepaper_page.html`
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/modern/whitepaper_page.html`
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/classic/whitepaper_page.html`

**Create:**
- `enrichdigiworld/whitepapers/templates/whitepapers/components/cta_button.html` (optional reusable component)

---

## 🧪 Testing Scenarios

1. **Default CTA**
   - [ ] Create whitepaper without customizing CTA
   - [ ] Verify default text and color appear

2. **Custom Text**
   - [ ] Change button text to "Get Your Copy"
   - [ ] Verify text appears on all themes

3. **Custom Color**
   - [ ] Change color to #ff0000 (red)
   - [ ] Verify color displays correctly
   - [ ] Verify color is accessible (contrast ratio)

4. **Different Styles**
   - [ ] Test solid style
   - [ ] Test outline style
   - [ ] Test gradient style

5. **Different Positions**
   - [ ] Test below form position
   - [ ] Test sticky footer position
   - [ ] Test right sidebar position

6. **Custom URL**
   - [ ] Set custom download URL
   - [ ] Verify click goes to custom URL

---

## 📋 Implementation Checklist

- [ ] Add model fields to WhitepaperPage
- [ ] Run migrations
- [ ] Update Default theme template
- [ ] Update Modern theme template
- [ ] Update Classic theme template
- [ ] Add panel to admin interface
- [ ] Test CTA customization
- [ ] Verify all colors are accessible
- [ ] Document new fields in admin help text

---

## 🎨 CSS Variables Implementation

Add to theme templates:
```html
<style>
    :root {
        --cta-color: {{ page.cta_button_color }};
        --cta-color-light: {{ page.cta_button_color|lighter }};
        --cta-text-color: {{ page.get_cta_text_color }};
    }
</style>
```

---

## 💡 UX Considerations

1. **Admin Preview**
   - Show live preview of CTA button in admin
   - Update preview as user types

2. **Color Selection**
   - Provide color picker for easy selection
   - Show color preview before saving
   - Warn if contrast ratio is too low

3. **Default Values**
   - Smart defaults from site branding settings
   - Option to reset to defaults

4. **Validation**
   - Validate hex color codes
   - Warn on very long button text
   - Ensure URL format is valid

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Add model fields | ⏳ Not Started | - |
| Update templates | ⏳ Not Started | - |
| Add admin panels | ⏳ Not Started | - |
| Test all scenarios | ⏳ Not Started | - |

---

## 🚀 Expected Outcome

After completion, users should be able to:
1. Open any whitepaper in Wagtail admin
2. Scroll to CTA section
3. Change button text without touching code
4. Pick a color with color picker
5. Choose button style
6. Choose button position
7. See changes reflected on the live site

---

## 📚 Related Documentation

- [Whitepaper Themes](01_WHITEPAPER_THEMES.md)
- [Theme Customization (Phase 2)](../PHASE_2/01_PER_WHITEPAPER_BRANDING.md)

---

**Last Updated:** January 27, 2026  
**Next Feature:** [03_THANK_YOU_PAGES.md](03_THANK_YOU_PAGES.md)
