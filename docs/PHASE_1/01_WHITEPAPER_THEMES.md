# Feature 1.1: Whitepaper Theme Templates

**Feature Name:** Implement 3 Whitepaper Theme Templates  
**Status:** ⏳ Not Started  
**Priority:** Critical  
**Estimated Time:** 1.5 days  
**Assigned To:** GitHub Copilot

---

## 📝 Description

Create three complete, responsive HTML templates for displaying whitepapers. Each theme will have a distinct visual style while maintaining brand consistency and functionality.

---

## ✅ Acceptance Criteria

- [ ] Default theme renders correctly on desktop, tablet, and mobile
- [ ] Modern theme renders correctly on all devices
- [ ] Classic theme renders correctly on all devices
- [ ] All themes display: header, hero section, content blocks, form, footer
- [ ] Responsive images with proper aspect ratios
- [ ] Forms are properly integrated and styled
- [ ] All themes use Tailwind CSS classes
- [ ] No layout shifts or visual bugs
- [ ] Page loading performance is acceptable (<3s)

---

## 🎯 Theme Specifications

### Theme 1: Default Theme
**Style:** Clean, minimal, modern  
**Color Palette:** Neutral (grays) with accent colors  
**Typography:** Sans-serif, clear hierarchy  
**Layout:** Single column with sidebar option

**Key Sections:**
- Hero with background image and overlay
- Introduction text
- Content body with sections
- Gated form (if gated)
- CTA button
- Related whitepapers (if available)
- Footer

**File Location:** `enrichdigiworld/whitepapers/templates/whitepapers/themes/default/whitepaper_page.html`

---

### Theme 2: Modern Theme
**Style:** Contemporary, bold, gradient-forward  
**Color Palette:** Vibrant gradients, high contrast  
**Typography:** Mix of serif and sans-serif  
**Layout:** Multi-column with cards

**Key Sections:**
- Gradient hero background
- Cover image as focal point
- Card-based content layout
- Form in highlighted box
- Social proof/stats
- CTA with animation
- Footer with links

**File Location:** `enrichdigiworld/whitepapers/templates/whitepapers/themes/modern/whitepaper_page.html`

---

### Theme 3: Classic Theme
**Style:** Professional, EnrichDigiWorld brand  
**Color Palette:** Company brand colors (primary/secondary)
**Typography:** Traditional, professional  
**Layout:** Multi-column with sidebar

**Key Sections:**
- Company logo in header
- Professional hero with company colors
- Traditional layout with sidebar
- Branded form styling
- Company footer with all links
- Professional typography
- Author byline prominent

**File Location:** `enrichdigiworld/whitepapers/templates/whitepapers/themes/classic/whitepaper_page.html`

---

## 📐 Layout Components (All Themes Must Include)

### 1. Header Section
- Page title
- Breadcrumb navigation
- Author and date information

### 2. Hero Section
- Background image or color
- Page title/hero text
- Subtitle/summary

### 3. Content Area
- Main content body (from StreamField)
- Support for images, text, documents
- Proper spacing and readability

### 4. Form Section (Gated Content)
- Form fields displayed clearly
- Proper validation feedback
- Submit button

### 5. Footer Section
- Copyright information
- Links to other resources
- Social media links (from site settings)

---

## 🏗️ Technical Approach

### Model Context
```
WhitepaperPage instance provides:
- title
- cover_image
- summary
- body (StreamField with blocks)
- author (WhitepaperAuthor)
- date
- is_gated
- design_template
- form_fields (if gated)
- whitepaper_pdf (link to download after form)
- thank_you_text
```

### Template Structure
Each template will:
1. Extend `base.html` for consistent header/footer
2. Use Tailwind CSS for styling
3. Include proper semantic HTML
4. Have responsive grid systems
5. Support dark mode (optional but nice)
6. Handle both gated and public content

### Data Context
Templates receive from `WhitepaperPage.get_context()`:
- `page` - the WhitepaperPage object
- `form` - the gated form (if applicable)
- `has_access` - boolean for access control
- All other page context variables

---

## 📋 Implementation Checklist

### Default Theme Template
- [ ] Create HTML structure
- [ ] Add Tailwind CSS classes
- [ ] Responsive design (mobile-first)
- [ ] Form integration
- [ ] Test on multiple devices
- [ ] Performance optimization

### Modern Theme Template
- [ ] Create HTML structure with gradient hero
- [ ] Add Tailwind CSS classes
- [ ] Card-based layout
- [ ] Interactive elements
- [ ] Mobile responsiveness
- [ ] Test animations don't break on mobile

### Classic Theme Template
- [ ] Create HTML structure
- [ ] Integrate brand colors from settings
- [ ] Professional styling
- [ ] Sidebar layout
- [ ] Company footer
- [ ] Responsive behavior

### All Themes
- [ ] Add proper image alt text
- [ ] Ensure accessibility (color contrast, focus states)
- [ ] Add meta tags support
- [ ] Handle missing images gracefully
- [ ] Test form submission
- [ ] Verify all content blocks display

---

## 🔧 Files to Create/Modify

**Create:**
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/default/whitepaper_page.html`
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/modern/whitepaper_page.html`
- `enrichdigiworld/whitepapers/templates/whitepapers/themes/classic/whitepaper_page.html`

**Modify:**
- None (existing templates remain unchanged)

---

## 🧪 Testing Plan

### Manual Testing
1. Create 3 test whitepapers (one per theme)
2. Test gated content flow
3. Test form submission
4. Test on mobile devices
5. Test image loading and display
6. Test PDF download (if available)

### Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## 📸 Visual References

### Default Theme Visual Hierarchy
1. Hero section (30% of viewport)
2. Content area (50%)
3. Form/CTA (15%)
4. Footer (5%)

### Modern Theme Visual Hierarchy
1. Large hero with gradient (40%)
2. Featured image (20%)
3. Content cards (25%)
4. Form (10%)
5. Footer (5%)

### Classic Theme Visual Hierarchy
1. Branded header (5%)
2. Professional hero (25%)
3. Main content + sidebar (60%)
4. Footer (10%)

---

## 💡 Design Principles

1. **Clarity** - Content should be easy to scan
2. **Hierarchy** - Important elements should stand out
3. **Consistency** - All themes follow similar structure
4. **Responsiveness** - Works on all device sizes
5. **Accessibility** - WCAG AA compliant
6. **Performance** - Fast loading, no unnecessary bloat

---

## 🚀 Implementation Progress

### Step 1: Default Theme
**Status:** ⏳ Not Started
**Time:** 0.5 days

### Step 2: Modern Theme
**Status:** ⏳ Not Started
**Time:** 0.5 days

### Step 3: Classic Theme
**Status:** ⏳ Not Started
**Time:** 0.5 days

---

## 📚 Related Documentation

- [CTA Customization](02_CTA_CUSTOMIZATION.md)
- [Thank You Pages](03_THANK_YOU_PAGES.md)
- [Form UI Polish](04_FORM_UI_POLISH.md)

---

## 🔍 Quality Checklist

Before moving to next feature:
- [ ] All templates validate as proper HTML5
- [ ] No console errors in browser DevTools
- [ ] All images load correctly
- [ ] Forms are functional
- [ ] Text is readable (contrast ratios OK)
- [ ] No horizontal scrolling on mobile
- [ ] Page loads in under 3 seconds
- [ ] All links work correctly

---

**Last Updated:** January 27, 2026  
**Next Feature:** [02_CTA_CUSTOMIZATION.md](02_CTA_CUSTOMIZATION.md)
