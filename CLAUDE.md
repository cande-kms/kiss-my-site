# Kiss My Site — Snap Scroll Landing Page

## Goal
12-panel snap-on-scroll landing page for Kiss My Site (digital marketing agency, Buenos Aires). Each wheel/swipe/key/dot-click = one immediate panel transition — NOT continuous scroll-scrub. Content language: English. Dark navy + cyan/magenta neon aesthetic.

## Stack
- Vite + vanilla JS + Tailwind CSS v4 (or plain CSS — match what `reference.html` already does, don't introduce a framework reference.html doesn't use)
- GSAP core only (no ScrollTrigger needed — the snap logic is hand-rolled, not scroll-driven)
- Deploy: Vercel

## Reference file
`reference.html` in this folder is the verified, working standalone demo — built and debugged over several rounds in Claude.ai web chat. It is the source of truth for:
- Snap transition logic and timing
- Panel structure / CSS class names
- Copy (English) for every panel
- Visual design tokens (colors, type, layout)

Read it fully before writing any code. Port its structure faithfully — don't redesign from scratch.

## Snap transition (LOCKED — do not change without explicit approval)
- DURATION: 0.6s
- EASE: power2.out
- Panels are stacked absolutely, each one's `.panel-content` (or `.panel-content--logos` for grid-style panels) slides in via `yPercent` 100→0 (next) or -100→0 (prev), while the outgoing panel slides out to ∓100%
- The ENTIRE content block animates as ONE unit (opacity + y), not as many individually-timed sub-tweens. This is intentional — an earlier version animated eyebrow/headline/copy/CTA as separate tweens with fractional offsets, which caused content to randomly get stuck invisible after interrupted transitions. Do not reintroduce that pattern.
- Every transition calls `gsap.killTweensOf()` on everything about to be touched (incoming panel, outgoing panel, content block, fg, bg, pulse line) before animating, to guarantee no stale tween survives an interruption
- `onComplete` forces the final resting state (opacity:1, y:0, etc.) as a safety net regardless of what happened mid-tween
- Lock all input (`isAnimating` flag) for the full duration of each transition
- Wheel input uses gesture-end detection (not a fixed-time cooldown): a wheel "gesture" is considered active until ~220ms pass with no new wheel events. This matters because a single physical trackpad swipe can fire wheel events for well over a second — a fixed cooldown shorter than that re-triggers the next panel mid-gesture and the user never sees settled content. Do not replace this with a simple `setTimeout` cooldown.
- Inputs: wheel, touch (50px swipe threshold, `touchmove` prevented to stop native bounce), arrow keys / PageUp/PageDown / Space / Home / End, click on progress dots, click on nav links, click on footer "Contact me!"
- Keyboard navigation must NOT fire while focus is inside an `<input>`, `<textarea>`, `<select>`, or any `contenteditable` element (the Contact panel has a real form — typing in it must not jump panels)

## Panels (in order, 12 total)
| # | Class | Nav grouping | Layout shell |
|---|---|---|---|
| 0 | `panel--home` | Home | `.panel-content` (hero) |
| 1 | `panel--seo` | Services (grouped) | `.panel-content` (hero) |
| 2 | `panel--cro` | Services (grouped) | `.panel-content` (hero) |
| 3 | `panel--ecommerce` | Services (grouped) | `.panel-content` (hero) |
| 4 | `panel--funnel` | Services (grouped) | `.panel-content` (hero) |
| 5 | `panel--analytics` | Services (grouped) | `.panel-content` (hero) |
| 6 | `panel--data` | Services (grouped) | `.panel-content` (hero) |
| 7 | `panel--clients` | Clients | `.panel-content--logos` (centered grid) |
| 8 | `panel--partners` | (reached via Clients flow) | `.panel-content--logos` (centered grid) |
| 9 | `panel--cases` | Cases | `.panel-content--logos` (card grid) |
| 10 | `panel--info` | (reached via scroll) | `.panel-content--logos` (manifesto grid) |
| 11 | `panel--contact` | Contact | `.panel-content panel-content--compact` (hero + form) |

The top nav's "Services" link stays visually active across indices 1–6 (it's a single grouped link, not 6 separate ones — see `data-group="services"` in `reference.html`).

Each of the 6 Services panels (1–6) is a full hero: eyebrow + headline + copy + a 3-item `<ul class="feature-list">` (checkmark + bold lead-in + description) + CTA row. Don't strip the feature list back down to just headline+copy — it was added specifically so each service panel reads as a complete section, not a bare title.

## Per-panel background + foreground images
`reference.html` currently uses CSS gradient placeholders for both the background (`.panel-bg .gradient`) and the decorative foreground shape (`.panel-fg .fg-shape`) on every panel. These need to become real images:

- **Background**: full-bleed photo per panel, goes in `.panel-bg .gradient` as a `background-image` (keep the existing dark overlay gradients layered on top via `::before`/`::after` for text legibility — don't remove those, just add the photo underneath)
- **Foreground**: a product/device/object cutout per panel, replaces the abstract `.fg-shape` CSS shape

We have 5 source images already (Home background+foreground, SEO background+foreground) from the original Figma/Elementor export — ask the user where these live before generating or sourcing the remaining 7 panels' worth of images. Do not invent stock photo URLs; if an image is missing, flag it and use the existing gradient as a temporary fallback rather than breaking the layout.

Logo: currently embedded as a base64 data URI directly in the `<img>` tag in the nav (a cropped lips/kiss icon). For a real project, extract it to `public/images/logo.png` and reference it by path instead — cleaner to maintain, smaller HTML file.

## Typography
- Display: Unbounded (700/900 weight), used for headlines, case stat values, nav logo wordmark
- Body: Inter (400/500/600)
- Mono/labels: JetBrains Mono — eyebrows, nav-adjacent labels, footer meta text
- Headline size: `clamp(2.4rem, min(6.2vw, 7.6vh), 5.4rem)` for hero panels; `clamp(2.6rem, min(6.2vw, 7.4vh), 5.2rem)` for centered-grid panels (Clients/Partners/Cases/Info)

## Color tokens
```
--bg:      #05070d
--panel:   #0a1224
--cyan:    #00e5ff
--magenta: #ff2bd6
--ink:     #f5f7fa
--muted:   #8a93a8
--line:    rgba(245,247,250,0.12)
```
Each panel has its own radial-gradient combo (see `reference.html`) — don't flatten them to one shared background, the slight hue variation per panel is intentional.

## Known issues already fixed in reference.html (do not regress)
1. **Nav overlap**: `.panel-content` is positioned with `top`/`bottom` absolute (not padding) so content height is mathematically capped between the fixed nav and footer — this was a real bug (long headlines pushed up under the nav) and is now fixed via `overflow:hidden` as a safety net. Keep this pattern.
2. **Content silently invisible after transition**: root cause was many individually-timed sub-tweens per panel + no `killTweensOf()` before re-animating, causing GSAP overwrite conflicts that could leave text at `opacity:0` after an interrupted transition. Fixed by animating the whole content block as one unit (see Snap transition section above).
3. **Contact panel headline clipping**: the Contact panel has more content than other heroes (headline + copy + 3-field form + button), so it uses a `.panel-content--compact` variant with a smaller headline and tighter `clamp()`-based gaps that compress automatically on short viewports.

## Note for assistant
The user is non-technical (works in marketing/agency, not engineering). Briefly explain what each command/change does in plain language. Use Plan Mode for anything touching the snap-transition JS or panel structure. Pause for approval after each major step. If asked to change animation timing or logic, re-read the "Snap transition" section above first and flag if the request would reintroduce a previously-fixed bug pattern.
