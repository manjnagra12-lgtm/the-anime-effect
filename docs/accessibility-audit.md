# Accessibility audit

**Audit date:** 2 November 2026
**Scope:** Current local Django build, rendered in Chromium at `http://127.0.0.1:8012`.
**Standard checked:** WCAG 2.1 Level A and AA rules available in axe-core.
**Status:** No automated axe violations were reported on the pages below. This is a limited audit, not a claim of full WCAG conformance.

## Method and coverage

The audit combined an automated axe-core scan with source/style inspection and focused keyboard, form-label, contrast, and responsive checks.

- Ran axe-core **4.10.3** using the `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa` tags.
- Scanned Discover, anime detail, About, Contact, Community, Log in, and Register pages. The local database contained catalog content for the Discover and detail checks.
- Inspected visible field labels and keyboard focus on Contact, Log in, and Register. Verified the first Tab stop reaches the skip link on Discover; the existing browser test asserts this behavior.
- Measured representative foreground/background color pairs from `static/css/site.css` using the WCAG relative-luminance contrast formula.
- The existing Chromium browser test checks Discover for horizontal overflow at 320, 390, 768, and 1,280 CSS pixels.

## Results

| Check | Result | Evidence / notes |
| --- | --- | --- |
| axe-core WCAG 2.0/2.1 A and AA scan | **Pass, with limits** | Zero violations on all seven scanned page types. axe marked some color-contrast nodes as incomplete where it could not calculate gradient backgrounds, decorative placeholder content, or a textarea partly outside the current viewport; those results are not counted as passes. |
| Keyboard skip link and focus indicator | **Pass for checked behavior** | The first Tab stop on Discover is “Skip to content”; the browser test confirms it targets `#main-content`. Focus styling uses a 3 px mint outline. |
| Form labels | **Pass for checked forms** | Contact, login, and registration inputs expose associated labels. axe reported no form-label violations on those pages. |
| Sampled text contrast | **Pass for sampled pairs** | Ratios below meet or exceed 4.5:1 for normal text. Values are listed below. |
| Responsive reflow | **Pass for measured page and widths** | Discover had no horizontal overflow at 320, 390, 768, and 1,280 CSS pixels. Other pages and text resizing were not measured at every width. |

### Sampled contrast ratios

Ratios were computed from the CSS color values using the WCAG relative-luminance formula. The 4.5:1 threshold applies to normal-sized text; these checks do not cover every state, image, or rendered pixel.

| Foreground | Background | Ratio |
| --- | --- | ---: |
| `#f4f3f8` primary text | `#11131b` page canvas | 16.79:1 |
| `#a7a5b4` muted text | `#191b26` panel | 7.08:1 |
| `#c4a4ff` links | `#11131b` page canvas | 8.92:1 |
| `#91e5cd` mint accent text | `#11131b` page canvas | 12.62:1 |
| `#898796` input placeholder | `#11131b` input | 5.27:1 |
| `#21172e` primary button text | `#c4a4ff` button | 8.23:1 |
| `#32131a` destructive button text | `#ff9aab` button | 8.41:1 |
| `#adabb9` hero supporting text | `#493764` brightest hero gradient stop | 4.62:1 |

The hero supporting-text color was adjusted during this audit. Before the adjustment, `#a7a5b4` measured 4.31:1 against the brightest gradient stop, below the normal-text threshold. The updated color clears that conservative stop-to-text comparison.

## Limitations and follow-up

- axe cannot fully evaluate text over CSS gradients. The hero text was checked against its brightest gradient stop, but this does not replace pixel-level checks of all gradient and overlay combinations.
- Authenticated tracker and community states, staff/admin screens, validation-error states, and all focus/hover combinations were not included in the axe page scan.
- No screen-reader testing, browser zoom/text-resize test, forced-colors/high-contrast test, or cross-browser audit was performed.
- The responsive browser assertion covers Discover only. Repeat the reflow check on detail, tracker, community, and form pages.
- Automated scans can miss usability and assistive-technology issues. Continue manual keyboard and screen-reader testing, especially through registration, tracker updates, post/comment forms, and validation errors.

To reproduce the automated scan, run the app locally and use axe DevTools or inject axe-core 4.10.3 into each page in Chromium. Re-run after changes to shared templates, colors, forms, or responsive styles, and record the scanner version and any incomplete results.
