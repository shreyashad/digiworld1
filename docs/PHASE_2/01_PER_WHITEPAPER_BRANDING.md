# Feature 2.1: Per-Whitepaper Branding Overrides

**Feature Name:** Per-Whitepaper Branding Customization  
**Status:** ⏳ Not Started  
**Priority:** High  
**Estimated Time:** 1 day

---

## 📝 Description

Allow each whitepaper to override site-wide branding without affecting others. Users can customize:
- Primary and secondary colors
- Font family
- Background images/patterns
- Header/footer visibility
- Custom CSS (for advanced users)

---

## ✅ Acceptance Criteria

- [ ] Color overrides work across all themes
- [ ] Font overrides work across all themes
- [ ] Background images display correctly
- [ ] Overrides don't affect site-wide settings
- [ ] Preview shows changes before publishing
- [ ] Reset to default option available
- [ ] Color contrast is validated
- [ ] Invalid colors handled gracefully

---

## 🏗️ Technical Approach

### Model Fields to Add

```python
class WhitepaperPage(AbstractEmailForm):
    # Branding Overrides
    override_theme_colors = models.BooleanField(
        default=False,
        help_text="Enable custom colors for this whitepaper"
    )
    
    override_primary_color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Hex color code (leave blank to use site default)"
    )
    
    override_secondary_color = models.CharField(
        max_length=20,
        blank=True
    )
    
    override_font_family = models.CharField(
        max_length=100,
        blank=True,
        choices=[...]
    )
    
    override_background_image = ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    custom_css = models.TextField(
        blank=True,
        help_text="Custom CSS for advanced users (optional)"
    )
```

---

## 🔧 Files to Modify

- `enrichdigiworld/whitepapers/models.py`
- All theme templates (to use override variables)
- Admin panels (to show customization options)

---

**Last Updated:** January 27, 2026

See [Phase 2 README](README.md) for more features.
