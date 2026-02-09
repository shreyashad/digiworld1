# Feature 2.2: Custom Form Field Builder

**Feature Name:** Custom Form Field Builder  
**Status:** ⏳ Not Started  
**Priority:** High  
**Estimated Time:** 1.5 days

---

## 📝 Description

Enable non-technical users to create and customize lead capture forms. Features include:
- Add/remove/reorder form fields
- Conditional field visibility
- Save form templates for reuse
- Pre-built form templates (Contact, Lead, Newsletter, etc.)

---

## ✅ Acceptance Criteria

- [ ] Fields can be added via admin interface
- [ ] Fields can be drag-dropped to reorder
- [ ] Fields can be hidden based on conditions
- [ ] Form templates can be saved and reused
- [ ] Multiple form field types supported
- [ ] Form validation works
- [ ] Submissions stored in database
- [ ] CSV export of form submissions

---

## 📋 Field Types Supported

- Text Input
- Email Input
- Phone Input
- Text Area
- Select Dropdown
- Checkbox
- Radio Buttons
- Date Picker
- File Upload (optional)

---

## 🏗️ Technical Approach

Update WhitepaperFormField model to add:
- field_type choices
- conditional_visibility settings
- field ordering
- custom validation rules

---

## 🔧 Files to Modify

- `enrichdigiworld/whitepapers/models.py`
- `enrichdigiworld/whitepapers/admin.py`
- Create `enrichdigiworld/whitepapers/templates/whitepapers/components/form_builder.html`

---

**Last Updated:** January 27, 2026

See [Phase 2 README](README.md) for more features.
