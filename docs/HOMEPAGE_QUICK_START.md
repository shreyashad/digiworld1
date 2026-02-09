# HomePage Implementation - Quick Setup Guide

## What Was Created

### 1. **HomePage Model** (`home/models.py`)
A powerful, flexible home page model with:
- **TextField**: introduction (optional)
- **StreamField**: body with 8 different block types
- All fields are admin-customizable via Wagtail CMS

### 2. **Snippet Models** (Reusable Content)
Four snippet models for managing content:
- **StatsCounter** - Statistics metrics
- **Service** - Services/features
- **Testimonial** - Customer testimonials
- **NetworkLink** - Social/network links

Each snippet has:
- Core content fields
- Optional icon/image fields
- Order field for sorting
- Admin panels for easy management

### 3. **StreamField Blocks** (8 Types)

| Block | Purpose | Auto-Data | Admin Fields |
|-------|---------|-----------|--------------|
| **HeroBlock** | Hero section with CTAs | None | title, subtitle, image, buttons |
| **LogoCloudBlock** | Client logos | WhitepaperClient | title, subtitle |
| **StatsBlock** | Animated stats | StatsCounter | title, subtitle, color |
| **ServiceGridBlock** | Services listing | Service | title, subtitle |
| **WhitepaperCarouselBlock** | Latest whitepapers | WhitepaperPage | title, limit, filters |
| **TestimonialCarouselBlock** | Testimonials | Testimonial | title, subtitle |
| **NetworkBlock** | Social links | NetworkLink | title, subtitle |
| **NewsletterBlock** | Newsletter signup | None | title, placeholder, button text |

### 4. **Templates** (8 Block Templates + Main)
```
home/templates/home/
├── home_page.html (main - renders blocks)
└── blocks/
    ├── hero_block.html
    ├── logo_cloud_block.html
    ├── stats_block.html
    ├── services_block.html
    ├── whitepapers_block.html
    ├── testimonials_block.html
    ├── networks_block.html
    └── newsletter_block.html
```

### 5. **Template Tags** (Custom Tags)
Created custom template tags in:
- `home/templatetags/home_tags.py`
- `whitepapers/templatetags/wagtail_whitepapers.py`

Available tags:
```django
{% get_stats_counters %}
{% get_services %}
{% get_testimonials %}
{% get_network_links %}
{% get_latest_whitepapers limit=6 %}
{% get_whitepaper_categories %}
{% get_clients %}
{% mul value arg %} (filter)
```

---

## How to Use

### Step 1: Create Content Snippets

Go to Wagtail Admin → Snippets and create:

#### Stats Counters
1. **Snippets** → **Stats Counters** → **Add**
2. Fill in:
   - Label: "Downloads"
   - Value: "10,000"
   - Icon: (upload or select image)
   - Order: 0
3. Repeat for more stats

#### Services
1. **Snippets** → **Services** → **Add**
2. Fill in:
   - Title: "Service Name"
   - Description: (RichText)
   - Icon: (image)
   - Order: 0
3. Repeat for more services

#### Testimonials
1. **Snippets** → **Testimonials** → **Add**
2. Fill in:
   - Text: Quote
   - Author Name: "John Doe"
   - Author Title: "CEO"
   - Author Company: "Company Name"
   - Author Image: Profile photo
   - Order: 0

#### Network Links
1. **Snippets** → **Network Links** → **Add**
2. Fill in:
   - Name: "LinkedIn"
   - URL: "https://linkedin.com/company/..."
   - Icon Class: "fab fa-linkedin"
   - Order: 0

**Common Icon Classes:**
- `fab fa-linkedin` - LinkedIn
- `fab fa-twitter` - Twitter
- `fab fa-facebook` - Facebook
- `fab fa-instagram` - Instagram
- `fab fa-github` - GitHub
- `fab fa-youtube` - YouTube

### Step 2: Create HomePage

1. **Pages** → (right-click site root) → **Add child page**
2. Select **Home Page** as page type
3. Fill in:
   - **Title**: "Home"
   - **Slug**: "home" (or blank for root)
   - **Introduction**: (optional)
4. Click **Save**

### Step 3: Build Your Page with Blocks

In the **Body** field:

1. Click **"Add block"**
2. Choose a block type (Hero, LogoCloud, Stats, etc.)
3. Configure the block:
   - **HeroBlock**: Add title, subtitle, image, CTA buttons
   - **LogoCloudBlock**: Add title (logos auto-populate)
   - **StatsBlock**: Add title, description, color (stats auto-populate)
   - **ServiceGridBlock**: Add title (services auto-populate)
   - **WhitepaperCarouselBlock**: Set limit and show filters
   - **TestimonialCarouselBlock**: Add title (testimonials auto-populate)
   - **NetworkBlock**: Add title (networks auto-populate)
   - **NewsletterBlock**: Add title, button text, placeholder
4. Reorder blocks by dragging
5. Publish page

---

## Features

### ✅ Responsive Design
- Desktop: Full-featured layouts
- Tablet: Optimized columns and spacing
- Mobile: Single column, touch-friendly

### ✅ Animations
- AOS (Animate On Scroll)
- Counter animations on scroll
- Hover effects on all cards
- Smooth transitions

### ✅ Admin Features
- Drag-and-drop block reordering
- Rich text editor for content
- Image picker for icons/images
- Color picker for backgrounds
- Easy snippet management

### ✅ Auto-Population
- Whitepapers auto-fetch latest published
- Snippets auto-populate from database
- Clients auto-populate from WhitepaperClient

### ✅ SEO-Ready
- Proper heading hierarchy
- Alt text on images
- Semantic HTML
- Search fields

---

## Customization

### Change Colors
Edit the color values in each block template:
- Primary: `#003057` (blue)
- Gradient: `#667eea to #764ba2`
- Light: `#f8f9fa`

### Change Animations
In templates, modify AOS attributes:
```html
data-aos="fade-up"
data-aos-delay="200"
data-aos-duration="1000"
```

### Add New Block Types
1. Create new StructBlock in `models.py`
2. Add to HomePage StreamField
3. Create template in `blocks/`
4. Add include in `home_page.html`
5. Run migrations

### Customize Styling
Each block template has inline `<style>` tags. Customize:
- Colors
- Typography
- Spacing
- Hover effects
- Responsive breakpoints

---

## Database

### Models Created
- `home.HomePage` - Main page model
- `home.StatsCounter` - Statistics snippets
- `home.Service` - Services snippets
- `home.Testimonial` - Testimonials snippets
- `home.NetworkLink` - Network links snippets

### Migration
- Migration file: `home/migrations/0003_...py`
- Status: ✅ Applied

---

## File Locations

```
enrichdigiworld/
├── home/
│   ├── models.py (HomePage + Snippets)
│   ├── templates/
│   │   └── home/
│   │       ├── home_page.html
│   │       └── blocks/ (8 templates)
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── home_tags.py
│   └── migrations/
│       └── 0003_*.py
├── whitepapers/
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── wagtail_whitepapers.py
│   └── models.py (existing)
└── HOME_PAGE_GUIDE.md (comprehensive guide)
```

---

## Next Steps

1. ✅ **Models Created** - HomePage with 8 block types
2. ✅ **Templates Created** - Responsive templates for each block
3. ✅ **Migrations Applied** - Database ready
4. 📝 **Create Snippets** - Add Stats, Services, Testimonials, Networks
5. 📝 **Create HomePage** - Build with StreamField blocks
6. 📝 **Test Responsiveness** - Check mobile/tablet views
7. 📝 **Publish** - Make page live
8. 📝 **Configure URL** - Set as home page in site settings

---

## Support

For detailed documentation, see: `HOME_PAGE_GUIDE.md`

For template customization, check inline comments in:
- `home/templates/home/blocks/*.html`

For snippet usage, see admin interface:
- Wagtail Admin → Snippets

---

## Troubleshooting

**Q: Blocks not showing in admin?**
A: Run `python manage.py migrate home` to apply migrations

**Q: Snippets not appearing on page?**
A: Verify snippets are created and template tags are loaded with `{% load home_tags %}`

**Q: Images not displaying?**
A: Check image is uploaded in Wagtail media and ForeignKey is set correctly

**Q: Styling looks off?**
A: Clear browser cache (Ctrl+Shift+Delete) and hard reload (Ctrl+Shift+R)

---

Created: 2026-01-27
Status: Ready for use
