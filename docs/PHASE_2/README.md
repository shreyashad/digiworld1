# Phase 2: Customization & Branding

**Phase Name:** Customization & Branding System  
**Duration:** 3-4 days  
**Priority:** High  
**Status:** ⏳ Not Started

---

## 📋 Phase Overview

This phase enables non-technical users to customize whitepapers beyond templates. Users will be able to override branding, customize forms, schedule publishing, and configure email templates.

### What We're Building

1. **Per-Whitepaper Branding Overrides**
   - Custom colors, fonts, backgrounds per whitepaper
   - Override site-wide settings

2. **Custom Form Field Builder**
   - Drag-and-drop form field management
   - Reusable form templates
   - Conditional field visibility

3. **Scheduled Publishing**
   - Schedule publish/unpublish dates
   - Auto-publish at scheduled times
   - Visibility indicators

4. **Email Template Customization**
   - Customize confirmation emails
   - Custom signatures and footer

---

## 📑 Feature List

### Feature 1: Per-Whitepaper Branding Overrides
**Status:** ⏳ Not Started  
**Priority:** High  
**Estimated Time:** 1 day

See [01_PER_WHITEPAPER_BRANDING.md](01_PER_WHITEPAPER_BRANDING.md)

---

### Feature 2: Custom Form Field Builder
**Status:** ⏳ Not Started  
**Priority:** High  
**Estimated Time:** 1.5 days

See [02_CUSTOM_FORM_FIELDS.md](02_CUSTOM_FORM_FIELDS.md)

---

### Feature 3: Scheduled Publishing
**Status:** ⏳ Not Started  
**Priority:** Medium  
**Estimated Time:** 0.75 days

See [03_SCHEDULED_PUBLISHING.md](03_SCHEDULED_PUBLISHING.md)

---

### Feature 4: Email Template Customization
**Status:** ⏳ Not Started  
**Priority:** Medium  
**Estimated Time:** 0.75 days

See [04_EMAIL_CUSTOMIZATION.md](04_EMAIL_CUSTOMIZATION.md)

---

## 🎯 Phase Acceptance Criteria

- [ ] Users can override site colors per whitepaper
- [ ] Users can customize form fields without code
- [ ] Form fields can be drag-and-dropped to reorder
- [ ] Form templates can be created and reused
- [ ] Whitepapers can be scheduled for publishing
- [ ] Email templates can be customized
- [ ] All customizations work in all themes
- [ ] No technical knowledge required

---

## 🔗 File Structure After Phase 2

```
enrichdigiworld/
├── whitepapers/
│   ├── models.py (add customization fields)
│   ├── forms.py (add form builder)
│   └── templates/
│       └── whitepapers/
│           └── components/
│               ├── form_builder.html
│               └── email_template.html
│
├── static/
│   └── js/
│       ├── form-builder.js (drag-and-drop)
│       └── color-picker.js
│
└── enrichdigiworld/
    └── static/
        └── css/
            └── form-builder.css
```

---

## 🔄 Dependencies

**Depends on:**
- Phase 1: Templates must be complete
- All 3 themes must be implemented

**Blocks:**
- Phase 3: Analytics depends on complete customization
- Phase 4: Advanced features depend on this

---

## 🚀 How to Get Started

1. Start with [01_PER_WHITEPAPER_BRANDING.md](01_PER_WHITEPAPER_BRANDING.md)
2. Implement per-whitepaper color/font overrides
3. Move to [02_CUSTOM_FORM_FIELDS.md](02_CUSTOM_FORM_FIELDS.md)
4. Build form field builder UI
5. Complete remaining features in order

---

## 📊 Progress Tracking

| Feature | Status | Progress | Notes |
|---------|--------|----------|-------|
| Per-Whitepaper Branding | ⏳ Not Started | 0% | - |
| Custom Form Fields | ⏳ Not Started | 0% | - |
| Scheduled Publishing | ⏳ Not Started | 0% | - |
| Email Customization | ⏳ Not Started | 0% | - |

---

## 💡 Key Principles

1. **No Code Required** - Everything should be doable in admin UI
2. **Consistency** - Respect brand guidelines where possible
3. **Simplicity** - Don't overwhelm with options
4. **Flexibility** - Advanced users can customize deeply
5. **Feedback** - Show changes in real-time preview

---

## 🧪 Testing Strategy

- Test all customizations in all 3 themes
- Test on mobile and desktop
- Test with extreme values (very long text, unusual colors)
- Test persistence (data saves correctly)
- Test reset to defaults functionality

---

**Last Updated:** January 27, 2026  
**Next Step:** Open [01_PER_WHITEPAPER_BRANDING.md](01_PER_WHITEPAPER_BRANDING.md)
