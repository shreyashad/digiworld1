# Feature 4.1: PDF Versioning System

**Feature Name:** PDF Version Management  
**Status:** ⏳ Not Started  
**Priority:** Medium  
**Estimated Time:** 1.5 days

---

## 📝 Description

Allow storing multiple PDF versions per whitepaper with:
- Version history and changelog
- Auto-archive old versions
- Download specific versions
- Version comparison
- Deprecation notices

---

## ✅ Acceptance Criteria

- [ ] Multiple PDFs can be stored per whitepaper
- [ ] Current version is clearly marked
- [ ] Version history visible in admin
- [ ] Users can download previous versions
- [ ] Changelog is displayed to users
- [ ] Version archive works (old versions archived after 12 months)
- [ ] No data loss when uploading new version

---

## 🏗️ Model Design

### WhitepaperPDFVersion Model
```python
class WhitepaperPDFVersion(models.Model):
    whitepaper = ForeignKey(WhitepaperPage)
    pdf_file = ForeignKey('wagtaildocs.Document')
    version_number = CharField()  # 1.0, 1.1, 2.0, etc.
    changelog = TextField()
    is_current = BooleanField(default=False)
    uploaded_at = DateTimeField(auto_now_add=True)
    deprecated_at = DateTimeField(null=True)  # auto-set after 12 months
    download_count = IntegerField(default=0)
```

---

## 🔧 Files to Modify

- `enrichdigiworld/whitepapers/models.py` (add versioning)
- Templates (show version selector)
- Admin interface (manage versions)

---

**Last Updated:** January 27, 2026

See [Phase 4 README](README.md) for more features.
