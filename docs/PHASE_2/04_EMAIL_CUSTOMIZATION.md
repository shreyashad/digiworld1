# Feature 2.4: Email Template Customization

**Feature Name:** Email Template Customization  
**Status:** ⏳ Not Started  
**Priority:** Medium  
**Estimated Time:** 0.75 days

---

## 📝 Description

Allow customization of confirmation and notification emails sent after form submission. Users can customize:
- Email subject line
- Email body content
- From address and name
- Reply-to address

---

## ✅ Acceptance Criteria

- [ ] Confirmation emails send to users
- [ ] Admin emails send to team
- [ ] Email template can be customized
- [ ] Template variables work ({{name}}, {{company}})
- [ ] Rich text editor for email body
- [ ] Email preview available
- [ ] Test email can be sent
- [ ] Email validation works

---

## 📋 Email Types

1. **User Confirmation Email**
   - Sent to form submitter
   - Confirms receipt of their info
   - Provides PDF download link
   - Customizable message

2. **Admin Notification Email**
   - Sent to team email address
   - Lists form submission data
   - Link to view in admin
   - Configurable recipients

---

## 🏗️ Technical Approach

Update WhitepaperPage model with email fields:
```python
confirmation_email_subject = CharField()
confirmation_email_body = RichTextField()
admin_notification_email = CharField()
```

Create email template system using Django templates.

---

## 🔧 Files to Modify

- `enrichdigiworld/whitepapers/models.py`
- Create `enrichdigiworld/whitepapers/emails.py`
- Create email templates in `enrichdigiworld/whitepapers/templates/email/`

---

**Last Updated:** January 27, 2026

See [Phase 2 README](README.md) for more features.
