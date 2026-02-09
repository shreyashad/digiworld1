# Feature 3.1: View & Download Tracking

**Feature Name:** View & Download Tracking System  
**Status:** ⏳ Not Started  
**Priority:** Critical  
**Estimated Time:** 1.5 days

---

## 📝 Description

Implement comprehensive tracking of:
- Page views per whitepaper
- Unique visitors
- Repeat visitors
- PDF downloads
- Time on page
- Device and browser information

---

## ✅ Acceptance Criteria

- [ ] Views are tracked when page loads
- [ ] Downloads are tracked when PDF downloaded
- [ ] Unique visitors identified correctly
- [ ] Device/browser info captured
- [ ] Referrer information captured
- [ ] Time on page calculated
- [ ] Data persists in database
- [ ] No performance impact (<100ms overhead)

---

## 🏗️ Model Design

### WhitepaperView Model
```python
class WhitepaperView(models.Model):
    whitepaper = ForeignKey(WhitepaperPage)
    visitor_ip = GenericIPAddressField()
    user_agent = TextField()
    device_type = CharField(choices=[...])  # mobile, desktop, tablet
    browser = CharField()
    operating_system = CharField()
    referrer = URLField(blank=True)
    session_id = CharField()
    timestamp = DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            Index(fields=['whitepaper', 'timestamp']),
        ]
```

### WhitepaperDownload Model
```python
class WhitepaperDownload(models.Model):
    whitepaper = ForeignKey(WhitepaperPage)
    visitor_ip = GenericIPAddressField()
    session_id = CharField()
    user_agent = TextField()
    timestamp = DateTimeField(auto_now_add=True)
    downloaded_by = ForeignKey(FormSubmission, null=True)
    
    class Meta:
        indexes = [
            Index(fields=['whitepaper', 'timestamp']),
        ]
```

---

## 🔧 Implementation Files

Create:
- `enrichdigiworld/analytics/models.py`
- `enrichdigiworld/analytics/utils.py` (device detection)
- Update `enrichdigiworld/whitepapers/models.py` (add tracking methods)

Modify:
- `enrichdigiworld/whitepapers/views.py` (add tracking on page load)

---

## 📊 Metrics to Calculate

- Total views
- Unique visitors
- Views per unique visitor
- Download rate (downloads/views)
- Popular referrers
- Most used devices/browsers
- Average time on page

---

**Last Updated:** January 27, 2026

See [Phase 3 README](README.md) for more features.
