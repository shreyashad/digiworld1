class LeadFieldValue(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="values"
    )
    # Keeping 'field' for legacy, making it null. Adding 'field_name' for blocks.
    field = models.ForeignKey(FormField, on_delete=models.CASCADE, null=True, blank=True)
    field_name = models.CharField(max_length=255, blank=True, help_text="Slug of the field from the template block")
    
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("lead", "field", "field_name")

    def __str__(self):
        return f"{self.lead.email} - {self.field_name or self.field.label}"



class DownloadToken(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)

    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
        ]

    def is_valid(self):
        from django.utils import timezone
        return (
            self.is_active and
            not self.used and
            self.expires_at > timezone.now()
        )

    def __str__(self):
        return f"Token for {self.lead.email}"








class WhitepaperView(models.Model):
    whitepaper = models.ForeignKey("WhitepaperPage", on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)


class DownloadEvent(models.Model):
    token = models.ForeignKey(DownloadToken, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)




class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("exported", "Exported"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
    ]

    whitepaper = models.ForeignKey(
        "WhitepaperPage",
        on_delete=models.CASCADE,
        related_name="leads"
    )

    email = models.EmailField()
    full_name = models.CharField(max_length=255, blank=True)

    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField()

    utm_source = models.CharField(max_length=255, blank=True)
    utm_campaign = models.CharField(max_length=255, blank=True)
    referer = models.URLField(blank=True)

    language = models.CharField(max_length=10, blank=True)

    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("whitepaper", "email")

    def __str__(self):
        return f"{self.email} - {self.whitepaper.title}"


