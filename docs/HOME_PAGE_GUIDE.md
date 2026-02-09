# HomePage Model & StreamField Implementation Guide

## Overview
The HomePage model provides a flexible, admin-customizable home page with 8 different content blocks that can be arranged in any order.

## Model Structure

### HomePage Model
- **introduction**: TextField for brief homepage intro
- **body**: StreamField with 8 different block types
- **Template**: `home/home_page.html`

### Supported Blocks in StreamField

#### 1. **HeroBlock**
Complete hero section with:
- Title (required)
- Subtitle (optional)
- Background image
- Overlay opacity (0-100)
- Multiple CTA buttons with styles (primary, secondary, outline, white)

**Admin Fields:**
- title
- subtitle
- background_image
- overlay_opacity
- cta_buttons (ListBlock of CTAButtonBlock)

**Features:**
- Responsive full-viewport hero
- Animated scroll indicator
- Smooth button hover effects
- Mobile-optimized layout

---

#### 2. **LogoCloudBlock**
Client/company logos section
- Title (required)
- Subtitle (optional)
- Automatically pulls all WhitepaperClient logos

**Admin Fields:**
- title
- subtitle
- section_title

**Features:**
- Responsive grid layout (6 columns on desktop, 2 on mobile)
- Hover elevation effects
- Auto-populates from WhitepaperClient model

---

#### 3. **StatsBlock**
Statistics/metrics section with animated counters
- Title (required)
- Subtitle (optional)
- Description (optional RichText)
- Customizable background color (hex code)
- Auto-populates from StatsCounter snippets

**Admin Fields:**
- title
- subtitle
- description
- background_color

**Features:**
- Counter animation on scroll
- Grid icons
- 4 columns on desktop, 1 on mobile
- Custom background color support

**Data Source:** StatsCounter snippet model

---

#### 4. **ServiceGridBlock**
"We Provide These Services" section
- Title (required)
- Subtitle (optional)
- Description (optional RichText)
- Auto-populates from Service snippets

**Admin Fields:**
- title
- subtitle
- description

**Features:**
- 3-column grid on desktop
- Colored left border on hover
- Gradient icon backgrounds
- Auto-fetched from Service model

**Data Source:** Service snippet model

---

#### 5. **WhitepaperCarouselBlock**
Latest whitepapers showcase
- Title (required, default: "Latest Whitepapers")
- Subtitle (optional)
- Limit (number of whitepapers to show, default: 6)
- Show filters toggle (show category filters)

**Admin Fields:**
- title
- subtitle
- limit
- show_filters

**Features:**
- 3-column responsive grid
- Category filter buttons
- Auto-fetch latest published whitepapers
- Client badges on cards
- Hover image zoom effect

**Data Source:** WhitepaperPage (live, ordered by -published_date)

---

#### 6. **TestimonialCarouselBlock**
Customer testimonials section
- Title (required, default: "What Our Clients Say")
- Subtitle (optional)
- Auto-populates from Testimonial snippets

**Admin Fields:**
- title
- subtitle

**Features:**
- 2-column layout on desktop, 1 on mobile
- Author images, titles, and companies
- Glassmorphism design
- Gradient background
- Auto-fetched from Testimonial model

**Data Source:** Testimonial snippet model

---

#### 7. **NetworkBlock**
Social media / Network links section
- Title (required, default: "Connect With Us")
- Subtitle (optional)
- Auto-populates from NetworkLink snippets

**Admin Fields:**
- title
- subtitle

**Features:**
- Icon-based link grid
- Supports Font Awesome icons
- Hover lift effect
- Responsive sizing

**Data Source:** NetworkLink snippet model

---

#### 8. **NewsletterBlock**
Newsletter signup section
- Title (required, default: "Subscribe to Our Newsletter")
- Subtitle (optional)
- Description (optional RichText)
- Placeholder text (email input placeholder)
- Button text (submit button label)
- Optional background image

**Admin Fields:**
- title
- subtitle
- description
- placeholder
- button_text
- background_image

**Features:**
- Dark blue overlay
- Email input with submit button
- Responsive form layout
- Customizable button text
- Privacy notice

---

## Snippet Models (Reusable Content)

### StatsCounter
Manage statistics shown in the stats section.
- **label**: Stat name (e.g., "Downloads")
- **value**: Stat number (e.g., "10000")
- **icon**: Icon image
- **order**: Display order

**Admin Path:** Snippets → Stats Counters

### Service
Manage services shown in the services section.
- **title**: Service name
- **description**: RichText description
- **icon**: Icon image
- **order**: Display order

**Admin Path:** Snippets → Services

### Testimonial
Manage customer testimonials.
- **text**: RichText testimonial quote
- **author_name**: Customer name
- **author_title**: Job title (optional)
- **author_company**: Company name (optional)
- **author_image**: Profile photo
- **order**: Display order

**Admin Path:** Snippets → Testimonials

### NetworkLink
Manage social media and network links.
- **name**: Link label
- **url**: Target URL
- **icon_class**: Font Awesome class (e.g., "fab fa-linkedin")
- **order**: Display order

**Admin Path:** Snippets → Network Links

---

## Template Files Structure

```
home/
├── templates/
│   └── home/
│       ├── home_page.html (main template)
│       └── blocks/
│           ├── hero_block.html
│           ├── logo_cloud_block.html
│           ├── stats_block.html
│           ├── services_block.html
│           ├── whitepapers_block.html
│           ├── testimonials_block.html
│           ├── networks_block.html
│           └── newsletter_block.html
├── templatetags/
│   └── home_tags.py (custom template tags)
└── models.py (HomePage model)
```

---

## Template Tags (home_tags.py)

Custom template tags available in `home/blocks/` templates:

```django
{% load home_tags %}

{# Get all statistics #}
{% get_stats_counters as stats %}

{# Get all services #}
{% get_services as services %}

{# Get all testimonials #}
{% get_testimonials as testimonials %}

{# Get all network links #}
{% get_network_links as networks %}

{# Get latest whitepapers #}
{% get_latest_whitepapers limit=6 as whitepapers %}

{# Get whitepaper categories #}
{% get_whitepaper_categories as categories %}

{# Get all clients #}
{% get_clients as clients %}

{# Multiply filter for delays #}
{% forloop.counter|mul:100 %}
```

---

## Admin Panel Customization

### Creating a HomePage

1. Go to **Pages** in Wagtail admin
2. Click **Add child page** under your site root
3. Select **Home Page** as the page type
4. Fill in:
   - **Title**: "Home" (or your preferred name)
   - **Slug**: "home" or "" (for root)
   - **Introduction**: Brief intro text (optional)
5. Build your page using StreamField blocks:
   - Click **"Add block"** in the body field
   - Choose a block type
   - Configure block options
   - Reorder blocks by dragging

### Managing Snippets (Content Data)

#### Stats Counters
1. Go to **Snippets** → **Stats Counters**
2. Click **Add Stats Counter**
3. Enter label, value, icon, and order
4. These will auto-appear in any StatsBlock you add

#### Services
1. Go to **Snippets** → **Services**
2. Click **Add Service**
3. Configure title, description, icon, order
4. Auto-appears in ServiceGridBlock

#### Testimonials
1. Go to **Snippets** → **Testimonials**
2. Click **Add Testimonial**
3. Add quote, author details, image
4. Auto-appears in TestimonialCarouselBlock

#### Network Links
1. Go to **Snippets** → **Network Links**
2. Click **Add Network Link**
3. Configure name, URL, Font Awesome icon class
4. Example icon classes:
   - `fab fa-linkedin` (LinkedIn)
   - `fab fa-twitter` (Twitter)
   - `fab fa-facebook` (Facebook)
   - `fab fa-instagram` (Instagram)
   - `fab fa-github` (GitHub)

---

## Responsive Behavior

All blocks are fully responsive:

### Desktop (lg, ≥992px)
- Hero: Full viewport height, centered content
- Logo Cloud: 6 columns
- Stats: 4 columns
- Services: 3 columns
- Whitepapers: 3 columns
- Testimonials: 2 columns side-by-side
- Networks: Flexible wrap

### Tablet (md, 768px-991px)
- Adjusted spacing and typography
- Logo Cloud: 3 columns
- Stats: 2 columns
- Services: 2 columns
- Whitepapers: 2 columns
- Testimonials: Single column

### Mobile (sm, <768px)
- Single column layouts where applicable
- Increased padding for touch targets
- Optimized button sizing
- Full-width forms
- Smaller hero section (400px min-height)

---

## Styling & Customization

### Colors
- Primary Blue: `#003057`
- Gradient: `#667eea to #764ba2`
- Backgrounds: `#f8f9fa` (light), white, dark blue

### Animations
- AOS (Animate On Scroll) library support
- Hover effects on cards
- Counter animations on scroll
- Smooth transitions (0.3s)

### CSS Classes
All blocks include inline styles and can be customized via:
1. CSS file overrides
2. Inline style modifications in templates
3. Tailwind classes (if integrated)

---

## Database Queries Optimization

The implementation uses:
- `.select_related()` for foreign keys (images, clients)
- `.prefetch_related()` for many-to-many (categories)
- `.live()` for only published whitepapers
- `.order_by()` for consistent ordering

---

## SEO & Search

HomePage includes:
- Search fields for title and introduction
- Proper heading hierarchy (h1, h2, h3)
- Alt text on images
- Semantic HTML structure

---

## Future Enhancements

Possible additions:
1. **CarouselBlock** - Animated carousel with multiple images
2. **CTACardBlock** - Custom call-to-action cards
3. **VideoBlock** - Embedded video support
4. **PricingBlock** - Pricing table
5. **FAQBlock** - Frequently asked questions
6. **DownloadBlock** - Featured downloads
7. **EventBlock** - Upcoming events

---

## Troubleshooting

### Snippets not appearing?
- Verify snippets are created in Wagtail admin
- Check `order` field is set correctly
- Ensure template tags are loaded: `{% load home_tags %}`

### Images not loading?
- Verify images are uploaded in Wagtail
- Check image ForeignKey relations
- Ensure proper Wagtail image filter usage

### Blocks not displaying?
- Verify block template files exist
- Check block value variables match template
- Review browser console for JS errors

---

## Next Steps

1. **Create HomePage instance** in Wagtail admin
2. **Add content snippets** (Stats, Services, Testimonials, Networks)
3. **Build StreamField blocks** in desired order
4. **Test responsiveness** on mobile/tablet
5. **Publish** the page
6. **Configure DNS/URL routing** if needed
