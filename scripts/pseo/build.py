#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de páginas de SEO programático (EEUU) para Kiss My Site.
Uso: python3 scripts/pseo/build.py
Escribe en public/en/agency-{service}-{state-slug}.html
"""
import html as htmlmod
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "public", "en")

# ---------------------------------------------------------------------------
# Testimonios reales (los mismos del sitio principal — confirmado con Cande)
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    dict(
        quote="When we started building Hawaianas.com.ar we were pretty lost — we knew there was potential, "
              "but wanted to get the foundations right from day one. Cande and Mati from Kiss My Site were with "
              "us at every step, sharing their experience with real generosity. Beyond the professional quality, "
              "what we value most is the human warmth — we recommend them with total confidence.",
        author="Amira Maslub", role="E-commerce Manager", company="Hawaianas",
    ),
    dict(
        quote="We're very happy with Kiss My Site's service and the support we get on our SEO strategy. The "
              "team's dedication, professionalism, and commitment stand out, along with their ability to "
              "understand our business needs and adapt their proposals to our goals. Follow-up is constant and "
              "communication very clear, with a strategic approach that goes beyond SEO to give us a full view "
              "of positioning and site experience. We recommend Kiss My Site as a professional, committed "
              "agency that genuinely gets involved in the project.",
        author="Micaela Verta", role="Sr. VTEX Analyst", company="ShopGallery",
    ),
]

METHOD_TOOLS = "Google Search Console, GA4, Semrush, Screaming Frog, Hotjar and GTM"

DIFFERENTIATORS_TABLE = [
    ("Reports vanity metrics", "Reports attributed revenue and pipeline"),
    ("One generic strategy for every client", "A roadmap built from your own data and competitors"),
    ("A rotating account manager", "The same senior consultant from audit to execution"),
    ("Locks you into a 12-month contract", "No minimum lock-in — you stay because it works"),
    ("Sends a PDF once a quarter", "Biweekly working sessions and a live shared dashboard"),
]

# ---------------------------------------------------------------------------
# Datos por página — California
# ---------------------------------------------------------------------------

SEO_CA = dict(
    slug="agency-seo-california",
    service_label="SEO",
    service_type_schema="Search Engine Optimization",
    state="California", state_abbr="CA", main_city="Los Angeles",
    title="SEO Agency in California | Free SEO Audit | Kiss My Site",
    meta_desc="Hire an SEO agency in California. Technical SEO, content and link building that grow qualified "
              "leads. Book your free audit today. Serving Los Angeles.",
    h1="SEO Agency in California",
    eyebrow="SEO Agency · California",
    hero_lede="If organic search isn't actively working for you, you're leaving qualified traffic — and sales — "
              "on the table every single day in one of the most competitive markets in the country. We audit "
              "your site, build a technical, content and authority plan around real buyer intent, and track it "
              "all the way to revenue, not just rankings.",
    hero_bullets=[
        "Complete technical audit, prioritized by revenue impact — not a 200-item checklist",
        "Content built around California buyer intent, not generic keyword volume",
        "Your own live dashboard — the same one we use, every day",
        "No lock-in contracts. If we're not moving the needle, you'll know.",
    ],
    proof_stats=[
        ("8+", "Years running SEO programs"),
        ("40+", "Active clients across industries"),
        ("+180%", "Avg. organic traffic growth, 12 months"),
        ("4.2x", "Avg. return on investment"),
    ],
    pain_h2="If you've shopped for an SEO agency in California, you've probably already lived this",
    pain_items=[
        ("Reports full of rankings and zero revenue.", "You climbed keywords into the top 3 and revenue stayed "
         "flat. Someone sold you rankings, not demand."),
        ("A content plan nobody asked to read.", "Zero search volume, zero purchase intent — traffic on paper, "
         "not in your bank account."),
        ("Technical debt nobody touches.", "Google wastes crawl budget on URLs that shouldn't exist, while your "
         "most important pages don't get indexed."),
        ("100% dependent on paid media.", "The day you pause ad spend in one of the most expensive CPC markets "
         "in the US, traffic drops to zero."),
        ("Nobody can tell you what organic actually makes.", "Not the last agency, not your analytics setup — "
         "and without that number, any conversation about budget is a guess."),
    ],
    services_h2="Full-stack SEO: technical, content and authority",
    services_lede="We don't sell isolated \"content packages.\" We work the levers that actually move organic "
                  "search, prioritized by impact on your business.",
    services_cards=[
        ("🔧", "Technical SEO", "Full crawl, Core Web Vitals, URL architecture, structured data and JS "
         "rendering, prioritized by effort vs. impact."),
        ("🔍", "Keyword research", "We map your full market by real buyer intent and match it to your catalog "
         "or service lines, fixing cannibalization and gaps."),
        ("✍️", "Content production", "Category pages, comparisons and buying guides written to win a decision — "
         "every page built around one keyword and one metric."),
        ("🔗", "Digital PR", "Editorial links from real, relevant media outlets. No link farms, no penalty "
         "risk."),
        ("📍", "Local SEO", "Google Business Profile, local landing pages and citations, so you show up for "
         "\"near me\" and city-level searches across California."),
        ("🧩", "Programmatic SEO", "Structured, data-driven landing pages at scale — built the right way, with "
         "real differentiated content, not thin duplicate pages."),
    ],
    method_h2="From audit to revenue, in four stages",
    method_steps=[
        ("Diagnostic", "Week 1–2", "We analyze your site, your direct California competitors, and your current "
         "traffic and revenue. You walk away with an actionable document either way."),
        ("Roadmap", "Week 3", "Full technical audit, intent-based keyword research and architecture mapping. "
         "We define KPIs and set up the shared dashboard."),
        ("Execution", "Month 2–6", "Monthly sprints: technical fixes alongside your dev team, content "
         "publishing and authority building. Biweekly meeting, monthly report."),
        ("Measure & iterate", "Ongoing", "We double down on what's working, cut what isn't, and open new "
         "clusters — this is where organic starts lowering acquisition cost."),
    ],
    industries=[
        ("💻", "Technology & SaaS"), ("🎬", "Entertainment & Media"), ("🏨", "Tourism & Hospitality"),
        ("🏠", "Real Estate"), ("🏥", "Healthcare"), ("👗", "Retail & Fashion"),
        ("🌱", "Agriculture & Food"), ("💼", "Professional Services"),
    ],
    approach_h2="Our approach, in practice",
    approach_lede="We don't have a published California case yet — here's what a real first engagement looks "
                  "like, based on how we actually work.",
    approach_steps=[
        ("We start with the free audit.", "A full crawl plus a review of your top California competitors. You "
         "get the three most expensive issues we find, in writing, whether you hire us or not."),
        ("We build a roadmap tied to revenue.", "Not a checklist — a prioritized plan that says which fix moves "
         "which number, and by roughly how much."),
        ("We report on what the business cares about.", "Organic traffic and rankings are inputs. The report "
         "that matters tracks leads and revenue attributed to organic."),
    ],
    faqs=[
        ("What does your California SEO service include?", "Technical audits, keyword research, on-page "
         "optimization, content production, internal linking, digital PR and programmatic SEO, with monthly "
         "reporting on traffic, rankings and leads."),
        ("How long before we see SEO results?", "Most clients see measurable movement in rankings and "
         "impressions within 3 months, and meaningful lead growth between months 4 and 8, depending on "
         "competition and the technical state of the site."),
        ("Which areas of California do you serve?", "We serve businesses across California, including Los "
         "Angeles and the surrounding metro area, as well as companies based in California that sell "
         "nationally."),
        ("How much does an SEO agency in California cost?", "Pricing depends on site size, competition and "
         "goals. We scope every engagement after the free audit and quote a fixed monthly retainer with "
         "defined deliverables, no long lock-in contracts."),
        ("How do we get started with a California project?", "Book a free audit. We review your site, your "
         "California competitors and your traffic, then send a prioritized roadmap with scope, timeline and "
         "pricing before you commit."),
        ("Do you work with our in-house team or replace it?", "Both models work. We can run SEO end to end, or "
         "act as the strategy and technical layer while your team handles content production and publishing."),
    ],
    related=[
        ("agency-seo-usa", "SEO agency USA"),
        ("agency-seo-washington", "SEO agency Washington"),
        ("agency-seo-arizona", "SEO agency Arizona"),
        ("agency-seo-oregon", "SEO agency Oregon"),
        ("agency-cro-california", "CRO agency California"),
        ("agency-ecommerce-california", "Ecommerce agency California"),
    ],
    final_h2="Get your free SEO audit for California",
    final_body="Tell us about your project and within 48 business hours we'll hand you a real analysis of your "
               "organic situation — no cost, no commitment.",
)

CRO_CA = dict(
    slug="agency-cro-california",
    service_label="CRO",
    service_type_schema="Conversion Rate Optimization",
    state="California", state_abbr="CA", main_city="Los Angeles",
    title="CRO Agency in California | Free CRO Audit | Kiss My Site",
    meta_desc="Hire a CRO agency in California. A/B testing, UX research and analytics that turn your traffic "
              "into more leads. Book your free audit. Serving Los Angeles.",
    h1="CRO Agency in California",
    eyebrow="CRO Agency · California",
    hero_lede="You already have the traffic. In a market as expensive to advertise in as California, doubling "
              "your ad spend is the most costly way to grow. We make the traffic you already have leave you "
              "more money: conversion audits, experimentation and funnel optimization, backed by method and "
              "evidence.",
    hero_bullets=[
        "Conversion audit built on quantitative and qualitative data",
        "A/B testing program: hypotheses, measurement and learning",
        "Every change validated with statistical significance, not opinion",
        "We work with what you already have — no full site redesign required",
    ],
    proof_stats=[
        ("8+", "Years running CRO programs"),
        ("40+", "Active clients across industries"),
        ("+95%", "Avg. conversion rate lift, 12 months"),
        ("1 of 3", "Leaks found in a typical first audit"),
    ],
    pain_h2="If you've been burned by a CRO agency in California before, this will sound familiar",
    pain_items=[
        ("A full redesign, sold as \"optimization.\"", "Months of work, no A/B test, no way to know what "
         "actually moved the number."),
        ("Tests that stop the moment they look good.", "Called a winner before reaching statistical "
         "significance — then the lift disappears in production."),
        ("Reports on conversion rate, never on revenue.", "A rate can go up while revenue per session goes "
         "down. Nobody checked."),
        ("One-size-fits-all \"best practice\" changes.", "Copied from a blog post, not from your actual "
         "session recordings or funnel data."),
        ("No idea what to test next.", "A single test, then silence — no backlog, no prioritization "
         "framework."),
    ],
    services_h2="Full CRO: research, testing and proof",
    services_lede="We don't run tests for the sake of testing. Every hypothesis comes from real data about your "
                  "California traffic and how it actually behaves.",
    services_cards=[
        ("🔬", "Conversion audit", "Quantitative analytics review plus heatmaps and session recordings to find "
         "where and why people drop off."),
        ("🧪", "A/B & multivariate testing", "Structured hypotheses, proper sample-size math, and statistically "
         "validated results — never a coin flip."),
        ("🛒", "Checkout & form optimization", "Field-by-field review of your highest-friction steps, where "
         "small changes move the most revenue."),
        ("📊", "Analytics & tracking review", "GA4 and GTM audited so every test is measured against numbers "
         "you can actually trust."),
        ("🧭", "UX research", "User interviews and usability testing when the data says \"something's wrong\" "
         "but not \"why.\""),
        ("📈", "Personalization", "Segment-specific experiences for your highest-value traffic once the "
         "foundational tests are won."),
    ],
    method_h2="From audit to proven lift, in four stages",
    method_steps=[
        ("Diagnostic", "Week 1–2", "We review your funnel, analytics setup and your top California competitors. "
         "You get the three most expensive leaks in writing, whether you hire us or not."),
        ("Hypothesis backlog", "Week 3", "We prioritize a testing roadmap by expected impact and effort, and set "
         "up the shared reporting dashboard."),
        ("Execution", "Month 2–6", "Monthly testing cycles: design, build, run to significance, analyze. "
         "Biweekly meeting, monthly report."),
        ("Measure & iterate", "Ongoing", "Winners get rolled out permanently, losers get documented as learning "
         "— the backlog never runs dry."),
    ],
    industries=[
        ("💻", "SaaS & Technology"), ("🛍️", "E-commerce & Retail"), ("🏨", "Travel & Hospitality"),
        ("🏥", "Healthcare"), ("🏠", "Real Estate"), ("💰", "Financial Services"),
        ("🎓", "Education"), ("💼", "Professional Services"),
    ],
    approach_h2="Our approach, in practice",
    approach_lede="We don't have a published California case yet — here's what a real first engagement looks "
                  "like, based on how we actually work.",
    approach_steps=[
        ("We start with the free audit.", "A full funnel and analytics review, plus a look at your top "
         "California competitors. You get the three most expensive leaks in writing, whether you hire us or "
         "not."),
        ("We build a hypothesis backlog, not a single test.", "Prioritized by expected revenue impact, so the "
         "roadmap survives past the first result."),
        ("We report on revenue, not just conversion rate.", "Every test tracks revenue per session and cost per "
         "lead, validated for statistical significance before we call a winner."),
    ],
    faqs=[
        ("What does your CRO service include?", "Analytics setup and review, heatmaps, session recordings, "
         "user research, a prioritized hypothesis backlog, and A/B tests on landing pages, forms and checkout, "
         "with a full analysis after each test."),
        ("How much traffic do we need for CRO to work?", "As a rule of thumb, around 10,000 monthly sessions or "
         "300 monthly conversions makes A/B testing statistically viable. Below that we use qualitative "
         "research and sequential testing instead."),
        ("Which areas of California do you serve?", "We serve businesses across California, including Los "
         "Angeles and the surrounding metro area, as well as companies based in California that sell "
         "nationally."),
        ("How much does a CRO agency in California cost?", "It depends on testing volume and the complexity of "
         "your stack. We quote a fixed monthly retainer after the free audit, with an agreed number of "
         "experiments per month."),
        ("How do we get started with a California project?", "Book a free audit. We review your site, your "
         "California competitors and your traffic, then send a prioritized roadmap with scope, timeline and "
         "pricing before you commit."),
        ("How do you prove CRO results?", "Every test reports conversion rate, cost per lead, revenue per "
         "session and average order value, validated for statistical significance in GA4 before we call a "
         "winner."),
    ],
    related=[
        ("agency-cro-usa", "CRO agency USA"),
        ("agency-cro-washington", "CRO agency Washington"),
        ("agency-cro-arizona", "CRO agency Arizona"),
        ("agency-cro-oregon", "CRO agency Oregon"),
        ("agency-seo-california", "SEO agency California"),
        ("agency-ecommerce-california", "Ecommerce agency California"),
    ],
    final_h2="Get your free CRO audit for California",
    final_body="Tell us about your project and within 48 business hours we'll hand you the most expensive leaks "
               "in your current funnel — no cost, no commitment.",
)

ECOMMERCE_CA = dict(
    slug="agency-ecommerce-california",
    service_label="Ecommerce",
    service_type_schema="Ecommerce Development",
    state="California", state_abbr="CA", main_city="Los Angeles",
    title="Ecommerce Agency in California | Store Audit | Kiss My Site",
    meta_desc="Hire an ecommerce agency in California. Shopify and BigCommerce builds, catalog SEO and checkout "
              "CRO that grow revenue. Book your free audit.",
    h1="Ecommerce Agency in California",
    eyebrow="Ecommerce Agency · California",
    hero_lede="The difference between a California store that scales and one that stalls is the foundation. We "
              "support you at every step — platform, catalog, payments and CRO — to make sure your online store "
              "is built on solid, strategic ground from day one.",
    hero_bullets=[
        "Platform selection and build: Shopify, Shopify Plus, BigCommerce, WooCommerce or VTEX",
        "Catalog and category SEO built for how people actually search",
        "Checkout CRO to close the gap between visits and orders",
        "Migrations that don't lose your existing rankings or revenue",
    ],
    proof_stats=[
        ("8+", "Years building ecommerce stores"),
        ("40+", "Active clients across industries"),
        ("+120%", "Avg. store revenue growth, 12 months"),
        ("0", "Rankings lost on a properly planned migration"),
    ],
    pain_h2="If you're evaluating an ecommerce agency in California, you've probably already run into this",
    pain_items=[
        ("A store that looks good and converts badly.", "Nobody tested the checkout with real users before "
         "launch — friction hides in the details."),
        ("A migration that tanked your rankings.", "No redirect plan, no metadata carried over, and three "
         "months of organic traffic gone."),
        ("A platform picked for the wrong reasons.", "Chosen because it was trendy, not because it fit your "
         "catalog size or growth plan."),
        ("Integrations that don't talk to each other.", "Inventory, shipping and your ERP live in three "
         "different places, and someone reconciles it by hand."),
        ("SEO treated as an afterthought.", "Category and product pages built for design, not for the searches "
         "that actually drive California traffic."),
    ],
    services_h2="Full ecommerce: build, optimize and grow",
    services_lede="We don't just launch a store and disappear. Every build is scoped around what actually grows "
                  "revenue after go-live.",
    services_cards=[
        ("🛠️", "Store builds & migrations", "Shopify, Shopify Plus, BigCommerce, WooCommerce and VTEX, with a "
         "full redirect and metadata plan on every migration."),
        ("🗂️", "Catalog & category SEO", "Faceted navigation, pagination and category structure built around "
         "real buyer search intent, not just design."),
        ("💳", "Checkout CRO", "Field-by-field review of your highest-drop-off step, tested and validated, not "
         "guessed."),
        ("🔌", "Integrations", "Stripe, PayPal and Shop Pay, plus sales tax, shipping carriers and ERP or 3PL "
         "tools, so checkout stays fast and reliable."),
        ("📈", "Analytics & attribution", "GA4 ecommerce tracking wired correctly, so every dollar of revenue is "
         "attributed to the channel that earned it."),
        ("✉️", "Lifecycle marketing", "Abandoned cart, post-purchase and win-back flows that turn one order into "
         "repeat revenue."),
    ],
    method_h2="From audit to launch, in four stages",
    method_steps=[
        ("Diagnostic", "Week 1–2", "We review your current store (or scope a new one), your California "
         "competitors, and your catalog and traffic. You get an actionable document either way."),
        ("Roadmap", "Week 3", "Platform decision, information architecture, and a prioritized backlog of fixes "
         "or build tasks, with the shared dashboard set up."),
        ("Execution", "Month 2–6", "Build or fix sprints, catalog and category SEO, checkout CRO. Biweekly "
         "meeting, monthly report."),
        ("Measure & iterate", "Ongoing", "We monitor conversion rate, AOV and organic traffic weekly after "
         "launch, and keep testing the checkout."),
    ],
    industries=[
        ("👗", "Fashion & Apparel"), ("💄", "Beauty & Personal Care"), ("🏠", "Home & Furniture"),
        ("🍔", "Food & Beverage"), ("💪", "Health & Wellness"), ("🎁", "Specialty & Gifts"),
        ("📱", "Electronics"), ("🐾", "Pet Products"),
    ],
    approach_h2="Our approach, in practice",
    approach_lede="We don't have a published California case yet — here's what a real first engagement looks "
                  "like, based on how we actually work.",
    approach_steps=[
        ("We start with the free audit.", "A full review of your store or a scoping session for a new one, plus "
         "a look at your top California competitors."),
        ("We plan the migration before we touch anything.", "Every URL mapped, every redirect planned, "
         "metadata and structured data preserved — indexation and traffic monitored daily after launch."),
        ("We report on revenue, not just traffic.", "Conversion rate, AOV and organic traffic tracked weekly, "
         "so you know the store is actually working, not just live."),
    ],
    faqs=[
        ("What ecommerce services do you offer in California?", "Ecommerce strategy, store builds and "
         "migrations, catalog and category SEO, checkout CRO, analytics, and lifecycle marketing automation."),
        ("Which ecommerce platforms do you work with?", "Shopify, Shopify Plus, BigCommerce, WooCommerce and "
         "VTEX. We recommend the platform based on catalog size, order volume and the integrations you need."),
        ("Which areas of California do you serve?", "We serve businesses across California, including Los "
         "Angeles and the surrounding metro area, as well as companies based in California that sell "
         "nationally."),
        ("Can you migrate our store without losing rankings?", "Yes. We map every URL, build the redirect plan, "
         "preserve metadata and structured data, and monitor indexation and traffic daily for the first weeks "
         "after launch."),
        ("How do we get started with a California project?", "Book a free audit. We review your site, your "
         "California competitors and your traffic, then send a prioritized roadmap with scope, timeline and "
         "pricing before you commit."),
        ("Do you handle payments, tax and shipping integrations?", "Yes. We integrate Stripe, PayPal and Shop "
         "Pay, plus sales tax, shipping carriers and ERP or 3PL tools, so checkout stays fast and reliable."),
    ],
    related=[
        ("agency-ecommerce-usa", "Ecommerce agency USA"),
        ("agency-ecommerce-washington", "Ecommerce agency Washington"),
        ("agency-ecommerce-arizona", "Ecommerce agency Arizona"),
        ("agency-ecommerce-oregon", "Ecommerce agency Oregon"),
        ("agency-seo-california", "SEO agency California"),
        ("agency-cro-california", "CRO agency California"),
    ],
    final_h2="Get your free ecommerce audit for California",
    final_body="Tell us about your store and within 48 business hours we'll hand you the highest-impact fixes — "
               "no cost, no commitment.",
)

PAGES = [SEO_CA, CRO_CA, ECOMMERCE_CA]
print(f"Loaded {len(PAGES)} page definitions.")

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def esc(s):
    return htmlmod.escape(s, quote=True)

def render_bullets(items):
    return "\n".join(f'<li>{esc(b)}</li>' for b in items)

def render_proof_stats(stats):
    return "\n".join(
        f'<div class="stat-box"><span class="stat-value">{esc(v)}</span>'
        f'<span class="stat-label">{esc(l)}</span></div>'
        for v, l in stats
    )

def render_pain_items(items):
    out = []
    for lead, body in items:
        out.append(f'''<div class="pain-row">
  <div class="pain-x"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 6l12 12M18 6L6 18"/></svg></div>
  <p><b>{esc(lead)}</b>{esc(body)}</p>
</div>''')
    return "\n".join(out)

def render_service_cards(cards):
    out = []
    for icon, title, desc in cards:
        out.append(f'''<div class="svc2-card glass glow-card">
  <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
  <h3>{esc(title)}</h3>
  <p>{esc(desc)}</p>
</div>''')
    return "\n".join(out)

def render_steps(steps):
    out = []
    for i, (title, timing, desc) in enumerate(steps, 1):
        out.append(f'''<div class="step-row">
  <div class="step-num">{i:02d}</div>
  <div>
    <h4>{esc(title)} <span style="color:var(--muted);font-weight:400;font-size:0.85rem;">— {esc(timing)}</span></h4>
    <p>{esc(desc)}</p>
  </div>
</div>''')
    return "\n".join(out)

def render_industries(industries, slug_prefix):
    out = []
    for icon, name in industries:
        out.append(f'''<div class="industry-card glass glow-card">
  <span class="industry-icon">{icon}</span>
  <span>{esc(name)}</span>
</div>''')
    return "\n".join(out)

def render_approach(steps):
    out = []
    for i, (title, body) in enumerate(steps, 1):
        out.append(f'''<div class="step-row">
  <div class="step-num">{i:02d}</div>
  <div>
    <h4>{esc(title)}</h4>
    <p>{esc(body)}</p>
  </div>
</div>''')
    return "\n".join(out)

def render_testimonials():
    out = []
    for t in TESTIMONIALS:
        out.append(f'''<div class="testi-card glass glow-card">
  <div class="testi-quote">&quot;</div>
  <blockquote>{esc(t["quote"])}</blockquote>
  <div class="testi-who">{esc(t["author"])}, {esc(t["role"])} — {esc(t["company"])}</div>
</div>''')
    return "\n".join(out)

def render_diff_table():
    cards = "\n".join(f'''<div class="why-card glass glow-card">
  <div class="why-old">
    <div class="why-old-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 6l12 12M18 6L6 18"/></svg></div>
    <p>{esc(a)}</p>
  </div>
  <div class="why-new">
    <div class="why-new-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M4 12l5 5L20 6"/></svg></div>
    <p>{esc(b)}</p>
  </div>
</div>''' for a, b in DIFFERENTIATORS_TABLE)
    return f'<div class="why-compare">{cards}</div>'

def render_faqs(faqs):
    out = []
    for q, a in faqs:
        out.append(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>')
    return "\n".join(out)

def render_related(related):
    out = []
    for slug, label in related:
        out.append(f'<a class="related-link" href="/en/{slug}">{esc(label)} <span>&rarr;</span></a>')
    return "\n".join(out)

def render_faq_schema(faqs):
    items = ",\n".join(f'''    {{
      "@type": "Question",
      "name": {json_str(q)},
      "acceptedAnswer": {{ "@type": "Answer", "text": {json_str(a)} }}
    }}''' for q, a in faqs)
    return f'''{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{items}
  ]
}}'''

def json_str(s):
    import json as _json
    return _json.dumps(s)

def render_page(d):
    canonical = f"https://kissmy.site/en/{d['slug']}"
    schema_service = f'''{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "{canonical}#business",
  "name": "Kiss My Site — {esc(d['service_label'])} Agency in {esc(d['state'])}",
  "url": "{canonical}",
  "description": {json_str(d['meta_desc'])},
  "serviceType": "{esc(d['service_type_schema'])}",
  "areaServed": {{ "@type": "State", "name": "{esc(d['state'])}" }},
  "address": {{ "@type": "PostalAddress", "addressCountry": "US" }}
}}'''
    schema_breadcrumb = f'''{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://kissmy.site/en" }},
    {{ "@type": "ListItem", "position": 2, "name": "{esc(d['service_label'])} Agency USA", "item": "https://kissmy.site/en/agency-{d['slug'].split('-')[1]}-usa" }},
    {{ "@type": "ListItem", "position": 3, "name": "{esc(d['h1'])}", "item": "{canonical}" }}
  ]
}}'''
    schema_faq = render_faq_schema(d['faqs'])

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script src="/atribucion.js"></script>
<title>{esc(d['title'])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(d['meta_desc'])}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="stylesheet" href="/assets/kms-shared.css">
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-M7NT6F3');</script>
<!-- End Google Tag Manager -->
<script type="application/ld+json">{schema_service}</script>
<script type="application/ld+json">{schema_breadcrumb}</script>
<script type="application/ld+json">{schema_faq}</script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-M7NT6F3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<canvas id="galaxy"></canvas>

<div class="page">

<svg width="0" height="0" style="position:absolute;">
  <defs>
    <filter id="navGlassFilter">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.012" numOctaves="2" seed="7" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" xChannelSelector="R" yChannelSelector="G" scale="18" />
    </filter>
  </defs>
</svg>

<nav id="siteNav">
  <a class="logo" href="/en"><img src="/images/logo-lips.png" alt="Kiss My Site" style="height:28px;width:auto;">kiss my site</a>
  <ul class="navlinks">
    <li><a href="/en#pillars">What we do</a></li>
    <li><a href="/en#packs">Packs</a></li>
    <li><a href="/en#services">Services</a></li>
    <li><a href="/en#clients">Clients</a></li>
  </ul>
  <div class="nav-right">
    <a class="nav-cta" href="#pseo-contact">Let's talk</a>
    <button class="navburger" id="navBurger" aria-label="Open menu" aria-expanded="false"><span class="bar"></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <button class="mobile-menu-close" id="mobileMenuClose" aria-label="Close menu">&times;</button>
  <ul>
    <li><a href="/en" data-close>Home</a></li>
    <li><a href="/en#pillars" data-close>What we do</a></li>
    <li><a href="/en#packs" data-close>Packs</a></li>
    <li><a href="/en#services" data-close>Services</a></li>
    <li><a href="/en#clients" data-close>Clients</a></li>
  </ul>
  <a class="mm-cta" href="#pseo-contact" data-close>Let's talk &rarr;</a>
</div>

<div class="whatsapp-float" id="whatsappFloat-wrap">
  <a class="whatsapp-float" id="whatsappFloat" href="#" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" fill="#fff"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.48 1.32 5.02L2 22l5.25-1.38a9.9 9.9 0 004.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm5.86 14.02c-.24.68-1.4 1.32-1.93 1.4-.5.08-1.11.11-1.79-.11-.41-.13-.94-.31-1.63-.6-2.86-1.24-4.73-4.13-4.87-4.32-.14-.19-1.17-1.55-1.17-2.96 0-1.41.74-2.1 1-2.39.26-.29.57-.36.76-.36.19 0 .38 0 .55.01.18.01.41-.07.64.49.24.58.81 2 .88 2.14.07.14.12.31.02.5-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.28.71 1.17 1.52 1.9 1.05.94 1.93 1.23 2.21 1.37.28.14.44.12.6-.07.16-.19.68-.79.86-1.06.18-.27.37-.22.62-.13.26.09 1.62.77 1.9.91.28.14.46.21.53.33.07.12.07.68-.17 1.36z"/></svg>
  </a>
</div>

<!-- Bloque 1: Hero -->
<section class="section service-hero" data-hue="263">
  <div class="svc2-hero">
    <div class="svc2-hero-copy">
      <div class="eyebrow">&middot; {esc(d['eyebrow'])}</div>
      <h1 class="sf-heading">{esc(d['h1'])}</h1>
      <p class="lede">{esc(d['hero_lede'])}</p>
      <ul class="svc2-bullets">
{render_bullets(d['hero_bullets'])}
      </ul>
      <div class="svc2-cta-row">
        <a class="pill pill-glow" href="#pseo-contact">Request your free audit &rarr;</a>
        <a class="pill pill-ghost" href="#pseo-method">See our method</a>
      </div>
      <div class="svc2-fineprint">Free audit, no strings attached. Response within 48 business hours.</div>
    </div>
    <div class="svc2-card glass glow-card">
      <h3>Free {esc(d['service_label'])} Audit</h3>
      <p>We review your real site and hand you the three most expensive issues — with an estimate of what they're costing you.</p>
      <a class="pill pill-glow" href="#pseo-contact">Get my audit &rarr;</a>
    </div>
  </div>
</section>

<!-- Bloque 2: Franja de prueba social -->
<section class="section" data-hue="270" style="padding-top:0;">
  <div class="proof-strip">
{render_proof_stats(d['proof_stats'])}
  </div>
</section>

<!-- Bloque 3: Diagnóstico del problema -->
<section class="section" data-hue="276">
  <div class="eyebrow">&middot; The problem</div>
  <h2 class="sf-heading">{esc(d['pain_h2'])}</h2>
  <div class="pain-list">
{render_pain_items(d['pain_items'])}
  </div>
</section>

<!-- Bloque 4: Servicio y entregables -->
<section class="section" data-hue="263" id="pseo-what">
  <div class="eyebrow">&middot; What you get</div>
  <h2 class="sf-heading">{esc(d['services_h2'])}</h2>
  <p class="section-lede">{esc(d['services_lede'])}</p>
  <div class="svc2-card-grid">
{render_service_cards(d['services_cards'])}
  </div>
</section>

<!-- Bloque 5: Metodología -->
<section class="section" data-hue="258" id="pseo-method">
  <div class="eyebrow">&middot; How we work</div>
  <h2 class="sf-heading">{esc(d['method_h2'])}</h2>
  <div class="pain-list">
{render_steps(d['method_steps'])}
  </div>
  <p style="color:var(--muted);font-size:0.9rem;margin-top:24px;">Tools we use day to day: {METHOD_TOOLS}.</p>
</section>

<!-- Bloque 6: Industrias -->
<section class="section" data-hue="283">
  <div class="eyebrow">&middot; Industries</div>
  <h2 class="sf-heading">Industries we work with in {esc(d['state'])}</h2>
  <div class="industries-grid">
{render_industries(d['industries'], d['slug'])}
  </div>
</section>

<!-- Bloque 8: Así trabajamos (sin casos de EEUU todavía) -->
<section class="section" data-hue="268">
  <div class="eyebrow">&middot; Our approach</div>
  <h2 class="sf-heading">{esc(d['approach_h2'])}</h2>
  <div class="approach-block">
    <p class="section-lede">{esc(d['approach_lede'])}</p>
    <div class="step-list">
{render_approach(d['approach_steps'])}
    </div>
  </div>
</section>

<!-- Bloque 9: Testimonios -->
<section class="section" data-hue="276">
  <div class="eyebrow">&middot; What clients say</div>
  <h2 class="sf-heading">What our clients say</h2>
  <div class="testi-grid testi-grid--two">
{render_testimonials()}
  </div>
</section>

<!-- Bloque 10: Diferenciadores -->
<section class="section" data-hue="263">
  <div class="eyebrow">&middot; Why Kiss My Site</div>
  <h2 class="sf-heading">Why {esc(d['state'])} businesses choose us over a typical agency</h2>
  {render_diff_table()}
</section>

<!-- Bloque 11: FAQs -->
<section class="section" data-hue="287">
  <div class="eyebrow">&middot; FAQs</div>
  <h2 class="sf-heading">Questions about {esc(d['service_label'])} in {esc(d['state'])}, answered</h2>
  <div class="faq-list">
{render_faqs(d['faqs'])}
  </div>
  <nav class="related-services" aria-label="Related pages">
    <span class="related-label">Related pages</span>
    <div class="related-chips">
{render_related(d['related'])}
    </div>
  </nav>
</section>

<!-- Bloque 13: CTA final y formulario -->
<section class="section" id="pseo-contact" data-hue="270">
  <div class="final-grid">
    <div class="final-copy">
      <div class="eyebrow">&middot; Get started</div>
      <h2 class="sf-heading" style="text-align:left;margin:0 0 20px;max-width:none;">{esc(d['final_h2'])}</h2>
      <p style="color:var(--muted);font-size:0.98rem;margin:0 0 24px;max-width:52ch;">{esc(d['final_body'])}</p>
    </div>
    <div class="svc2-form-card glass glow-card">
      <h3>Request your free audit</h3>
      <p>All fields marked * are required.</p>
      <form class="contact-form svc2-form" id="svc2form-{d['slug']}">
        <div><label for="f-name">Full name *</label><input id="f-name" name="name" required></div>
        <div><label for="f-email">Corporate email *</label><input id="f-email" name="email" type="email" required></div>
        <div><label for="f-company">Company *</label><input id="f-company" name="company" required></div>
        <div><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel"></div>
        <div class="full"><label for="f-message">What's your main challenge today?</label><textarea id="f-message" name="message"></textarea></div>
        <!-- Atribución: los completa atribucion.js. Dejarlos vacíos. -->
        <input type="hidden" name="utm_term"         data-attr="utm_term">
        <input type="hidden" name="utm_campaign"     data-attr="utm_campaign">
        <input type="hidden" name="utm_source"       data-attr="utm_source">
        <input type="hidden" name="utm_medium"       data-attr="utm_medium">
        <input type="hidden" name="utm_content"      data-attr="utm_content">
        <input type="hidden" name="gclid"            data-attr="gclid">
        <input type="hidden" name="gbraid"           data-attr="gbraid">
        <input type="hidden" name="wbraid"           data-attr="wbraid">
        <input type="hidden" name="fbclid"           data-attr="fbclid">
        <input type="hidden" name="landing_inicial"  data-attr="landing_inicial">
        <input type="hidden" name="referrer_inicial" data-attr="referrer_inicial">
        <input type="hidden" name="primera_visita"   data-attr="primera_visita">
        <label class="hp-field" aria-hidden="true"><input type="text" name="_hp" tabindex="-1" autocomplete="off"></label>
        <input type="checkbox" name="botcheck" class="hp-field" tabindex="-1" aria-hidden="true">
        <div class="full"><button class="pill pill-glow" type="submit">Request my free audit &rarr;</button></div>
      </form>
      <div class="svc2-success" id="svc2success-{d['slug']}">
        <h3>Thanks — request sent! 🎉</h3>
        <p>We'll be in touch within 48 business hours at the email you gave us.</p>
      </div>
    </div>
  </div>
</section>

</div>

<script src="/assets/kms-shared.js"></script>
</body>
</html>
'''

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for d in PAGES:
        html_out = render_page(d)
        path = os.path.join(OUT_DIR, f"{d['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"wrote {path} ({len(html_out.encode())} bytes)")

if __name__ == "__main__":
    main()
