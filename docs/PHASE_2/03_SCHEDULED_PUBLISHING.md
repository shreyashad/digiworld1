# Feature 2.3: Scheduled Publishing

**Feature Name:** Scheduled Publishing  
**Status:** ⏳ Not Started  
**Priority:** Medium  
**Estimated Time:** 0.75 days

---

## 📝 Description

Allow users to schedule when whitepapers become available or are unpublished. Features:
- Schedule publish date
- Schedule unpublish/expiry date
- Automatic publishing at scheduled time
- Visibility indicators in admin

---

## ✅ Acceptance Criteria

- [ ] Whitepapers can be scheduled for future publishing
- [ ] Scheduled whitepapers don't appear before publish date
- [ ] Whitepapers automatically publish at scheduled time
- [ ] Expiry date works (whitepaper becomes unavailable)
- [ ] Admin shows clear scheduling status
- [ ] Scheduled publications are reliable

---

## 🏗️ Technical Approach

Update WhitepaperPage model:
```python
scheduled_go_live_at = models.DateTimeField(null=True, blank=True)
scheduled_expire_at = models.DateTimeField(null=True, blank=True)
```

Add Celery task to publish scheduled whitepapers.

---

## 🔧 Files to Modify

- `enrichdigiworld/whitepapers/models.py`
- Create `enrichdigiworld/celery_tasks.py` (if using Celery)
- Update queryset filtering to respect scheduled dates

---

**Last Updated:** January 27, 2026

See [Phase 2 README](README.md) for more features.
