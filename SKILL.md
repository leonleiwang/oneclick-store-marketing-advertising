---
name: oneclick-store-marketing
description: Create complete offline-ready marketing packs for brick-and-mortar stores from a short natural-language brief. Use when Codex needs to turn "what the store sells + store type + audience + campaign goal" into research-backed Chinese marketing copy, posters, roll-up banners, window ads, shelf talkers, price tags, event pages, Xiaohongshu/WeChat/Instagram/Discord posts, event playbooks, product image prompts, and optionally generated images for local shops such as anime merch stores, figure stores, DND/tabletop stores, pet stores, coffee shops, barbershops, nail salons, boutiques, pop-up shops, and other physical retail or service businesses.
---

# OneClick Store Marketing Skill

Use this Skill to produce a complete, owner-friendly local-store marketing package from one sentence. The default promise is: input a store, audience, and goal; research the category; choose a campaign angle; write the copy; plan the offline assets; create image prompts or images; package the final files so a store owner can use them immediately.

## Core Principle

Optimize for real foot traffic, in-store conversion, repeat visits, and owner usability. Every asset must answer one of these jobs:

- Stop a passerby.
- Make the offer instantly understandable.
- Give a reason to enter today.
- Make a product or service feel desirable.
- Create an event reason to return with friends.
- Turn visitors into social followers or community members.

Beautiful but vague assets fail. Specific, local, printable, and action-driving assets win.

## Product Mode Logic

Default to **OneClick Finished Mode**:

- Treat the user brief as permission to create finished-looking marketing assets in one pass.
- Generate images with short Chinese copy baked into the design when direct image generation is requested.
- Keep Chinese text minimal, large, and high-contrast to maximize image-model readability.
- Prioritize "usable immediately by a store owner" over perfect design-tool editability.

Also provide **Pro Editable Layer** when delivering a full pack:

- Output the exact editable Chinese copy separately in `copy-bank.md`, `print-assets.md`, and `image-prompts.md`.
- Tell the user which text belongs on each asset so the design can be refined before print.
- Use editable copy as a professional fallback, not as a blocker for the default OneClick experience.

In short: default mode should feel like "one sentence in, usable poster/social image out"; pro mode adds print-safe copy control.

## OneClick Workflow

1. Resolve the minimum brief from the user text, attachments, project files, links, and conversation.
2. Ask at most 3 questions only when the missing data would materially change the campaign. If the user wants speed, continue with labeled assumptions.
3. Run lightweight research by default unless the user says not to. Research category language, audience memes/taste, local-store tactics, seasonal hooks, platform norms, and competitor examples. Cite web sources in the final answer when used.
4. Build the `STORE_MARKETING_BRIEF` block.
5. Diagnose the primary growth job: foot traffic, event turnout, basket size, repeat visit, membership/community, new product launch, appointment booking, or clearance.
6. Diagnose the store growth driver: traffic, SKU turnover, event, community, appointment, or trust.
7. If the store has many products, run Assortment Intelligence before planning visuals.
8. Select one campaign thesis and one secondary hook. Avoid trying to say everything.
9. Generate a complete asset plan across print, in-store, social, event, and product visuals.
10. Write Chinese copy first by default. Add English/Japanese/other language variants only when requested or useful for the audience.
11. Create image prompts with a shared `CAMPAIGN_STYLE_LOCK`.
12. If image API config exists or the user explicitly asks to generate images, call `scripts/generate_image.py`. Otherwise save executable prompts.
13. Assemble a delivery folder with markdown handoff files, prompts, and generated images when available.
14. Run the self-review scorecard and revise weak assets before final delivery.

## Minimum Brief

Extract or infer these fields:

- Store type and store name, if any.
- What is being sold or promoted.
- Audience: age, identity, spending level, visit scenario, fandom/style/community.
- Campaign goal: new launch, event, opening, holiday, clearance, membership, repeat visits, booking, basket size.
- Location context: city, mall/street/campus/community, opening hours, nearby traffic source.
- Offer: discount, bundle, gift, loyalty stamp, trial, limited item, appointment perk, group deal.
- Brand tone: cute, premium, street, cozy, professional, chaotic-fun, healing, collector-grade, etc.
- Output mode: strategy only, copy pack, prompt pack, full generated visual pack, or all.
- Compliance preference: only ask when the category is sensitive or the user requests review.

Use source labels when helpful:

- `User-provided`
- `Attachment/context`
- `Web-researched`
- `Inferred`
- `Assumption`
- `Default`

If assumptions materially shape the output, include `Assumptions / Defaults Used`.

## OneClick DSL

Use compact structured blocks so another agent, designer, or script can continue the work.

```text
STORE_MARKETING_BRIEF {
  store_type:
  store_name:
  product_or_service:
  audience:
  campaign_goal:
  location_context:
  offer:
  tone:
  output_mode:
}

CAMPAIGN_THESIS {
  one_sentence_pitch:
  primary_growth_job:
  emotional_hook:
  practical_hook:
  reason_to_visit_today:
  reason_to_share:
}

CAMPAIGN_STYLE_LOCK {
  visual_direction:
  palette:
  typography:
  photo_style:
  graphic_system:
  layout_rules:
  do_not_use:
}

ASSET_CARD {
  asset_name:
  channel:
  size_or_format:
  objective:
  headline:
  support_copy:
  cta:
  visual_prompt:
}
```

## Research Rules

Use research to improve specificity, not to delay delivery.

- Browse when the user asks for automatic research, current trends, platform norms, local recommendations, pricing context, or examples that may have changed.
- Prefer official platform docs, store/category examples, public local business pages, event pages, trend articles, and current social platform guidance.
- Never fabricate exact store facts, awards, sales numbers, celebrity/IP authorization, medical claims, or platform screenshots.
- For anime merch, figures, DND, tabletop, fandom, and character goods, avoid using unlicensed protected characters or logos in generated images unless the user provides authorized assets. Use original mascot/style cues instead.
- If research is unavailable, continue with `Assumption` and mark it clearly.

## Reference Loading

Load only what the task needs:

- For store-specific campaign tactics, read `references/industry-playbooks.md`.
- For poster, roll-up, window, price-tag, event-page, social, and product-image specs, read `references/deliverable-specs.md`.
- For Chinese hooks, social captions, event mechanics, and offer formulas, read `references/copy-formulas.md`.

## Strategy Engine

Choose one primary growth job:

- `Foot Traffic`: people nearby need a reason to enter now.
- `New Product Launch`: make the new item feel fresh, scarce, and socially shareable.
- `Event Turnout`: create a low-friction reason to come at a specific time.
- `Basket Size`: bundle, set, collect, add-on, upgrade, or gift logic.
- `Repeat Visit`: stamp card, drops, club nights, appointment cycle, community.
- `Community`: Discord/WeChat group, DND league, board game night, pet club, coffee tasting, nail lookbook.
- `Appointment Booking`: scarcity, slots, transformation preview, service menu clarity.
- `Clearance`: urgency without cheapening the brand.

Then map it to one local-store mechanic:

- Stamp rally / stamp card
- Lucky draw
- Newcomer night
- Group buy
- Limited drop
- Friend-get-friend
- Check-in gift
- Member day
- Theme night
- Before/after wall
- Mystery bag
- Photo spot challenge
- Reservation perk

## Store Growth Driver Diagnosis

Diagnose the campaign before writing copy or prompts. Pick one primary driver and optionally one secondary driver:

- **Traffic-Driven**: The main problem is not enough people entering the store. Use storefront visibility, location cues, today-only reasons, check-in gifts, and low-friction CTAs.
- **SKU-Turnover-Driven**: The store has many products and needs faster browsing, clearer recommendations, bundles, or shelf navigation. Use category cards, staff picks, price tags, bestseller/new-arrival labels, and bundle logic.
- **Event-Driven**: The store needs a specific time-based reason to gather people. Use event posters, rules, prize mechanics, staff scripts, and social announcements.
- **Community-Driven**: The store needs repeat visits and social retention. Use group-join benefits, member days, theme nights, Discord/WeChat announcements, and UGC prompts.
- **Appointment-Driven**: Service stores need bookings. Use transformation previews, service menus, slot scarcity, before/after assets, and booking CTAs.
- **Trust-Driven**: The buyer needs confidence before entering or buying. Use proof, real photos, staff recommendations, FAQ, warranty, origin/material notes, or safety disclaimers.

This is the local-store equivalent of ecommerce conversion-driver diagnosis. It prevents the Skill from making one pretty poster when the real problem is assortment navigation, event turnout, or community retention.

## Store Campaign Pack Golden Rule

When the user says "完整营销包", "宣传营销包", "一整套", "新品上架", "活动", "线下店宣传", or asks for a store campaign without narrowing the scope, default to a multi-asset pack, not a single image.

Default full pack:

- **1 traffic hero poster**: gets people to notice and enter.
- **1 window ad**: readable from outside; shortest copy.
- **1 roll-up banner**: explains campaign and offer in-store.
- **1 event/flyer page**: rules, time, reward, join method.
- **4 shelf talkers / price tags**: new arrival, bestseller, staff pick, bundle.
- **4 social visuals**: Xiaohongshu cover, WeChat Moments image, Instagram square, group announcement image.
- **4 product/lifestyle images**: hero product display, new-arrival shelf, bundle recommendation, community/event scene.
- **Copy pack**: headlines, CTAs, staff scripts, social captions, group message.
- **Event playbook**: rules, schedule, prize setup, staff checklist.

Each visual asset must have its own `ASSET_CARD` and prompt. Reuse one `CAMPAIGN_STYLE_LOCK` so the pack feels like one campaign, not random posters.

If API generation is enabled and the user asked for direct delivery, generate each asset by calling `scripts/generate_image.py` once per `ASSET_CARD`. A one-image smoke test is acceptable only when the user explicitly asks to test one image.

## Assortment Intelligence

Physical stores often sell many SKUs. Do not automatically cram every product into one poster.

First classify the assortment:

- `Hero SKU`: the product or series that should pull people into the store.
- `New Arrivals`: fresh items that create urgency.
- `Best Sellers`: proven items that reduce decision friction.
- `Staff Picks`: curated recommendations that create personality.
- `Entry Items`: low-price impulse buys.
- `Bundle Items`: products that naturally sell together.
- `Community Items`: products tied to events, fandom, tables, clubs, or repeat visits.

Then choose a layout strategy:

- **One Hero + Supporting Grid**: best for new launches with one strong campaign hook.
- **Category Navigation Pack**: best for stores with many SKUs, such as board game shops, guzi stores, pet stores, and beauty salons.
- **Social Carousel / Multi-Poster Set**: best when products need explanation or recommendations.
- **Shelf-Level Conversion System**: best when the goal is faster browsing and higher basket size.
- **Event-Led Pack**: best when products are secondary to a timed gathering.

Decision rule:

- If there are more than 5 meaningful products or categories, create a campaign system: one hero poster plus category/shelf/social assets.
- If there are 2-5 products, create one hero poster with a product grid plus separate shelf talkers.
- If there is one hero product or IP theme, create one dominant hero visual plus supporting assets.
- If the user provides no SKU list, infer 3-5 plausible categories and label them as assumptions.

For a board game store, do not put "all board games" into one visual. Split into useful buyer paths such as: newcomer-friendly party games, DND/TRPG night, strategy board games, family games, new arrivals, and staff picks.

## Copy Defaults

Write the primary copy in Chinese unless the user requests another language. Keep print copy short and forceful:

- Poster headline: 6-14 Chinese characters when possible.
- Poster subhead: 1 short sentence.
- CTA: concrete action, not vague enthusiasm.
- Price tag: product name + selling point + price/offer + optional mini hook.
- Window ad: readable at 3-5 meters.
- Social caption: hook in first line; include visit reason, time, address placeholder, and call to comment/save/share.

Do not write generic lines like "品质生活，从这里开始" unless the store is truly positioned that way. Prefer category-native language.

## Default Deliverables

When the user asks for a complete pack, deliver:

1. `campaign-brief.md`: research summary, target audience, campaign thesis, offer, style lock.
2. `copy-bank.md`: Chinese headlines, subheads, CTAs, price-tag lines, staff scripts, social captions.
3. `print-assets.md`: poster, roll-up banner, window ad, shelf talker, price tag, flyer/event page copy.
4. `social-pack.md`: Xiaohongshu, WeChat Moments, Instagram, Discord/WeChat group announcement.
5. `event-playbook.md`: event concept, schedule, rules, prizes, staff checklist, low-budget setup.
6. `image-prompts.md`: executable prompts for every visual asset.
7. `generated-campaigns/<slug>-<yyyymmdd-hhmmss>/`: prompts and images if generated.

Default visual count:

- 1 key visual poster
- 1 roll-up banner
- 1 window ad
- 4 price tags or shelf talkers
- 1 event page/flyer
- 4 social visuals
- 4 product/lifestyle images

Adjust the count to the user's scope.

## Campaign Style Lock

Every multi-asset campaign must use one shared style lock. It must define:

- Visual direction.
- 2-3 main colors and 1 accent.
- Typography style.
- Photo/product rendering style.
- Graphic components: labels, stickers, frames, icons, dividers.
- Layout density for print vs social.
- Texture or material cues.
- Prohibited elements that would weaken the brand or create IP risk.

Default style lock:

```text
Campaign Style Lock: coherent local retail campaign system; high-readability Chinese poster typography; strong storefront visibility; product-first composition; clean hierarchy with one bold headline, one supporting line, and one concrete CTA; consistent palette with one attention color, one dark text color, one light background color, and one secondary accent; real-world print-friendly contrast; social variants keep the same palette, type style, label shapes, and product mood; avoid clutter, fake licensed logos, unreadable text, and generic stock-ad aesthetics.
```

## Image Prompt Rules

Write prompts in English for image models unless the user requests Chinese prompts. Put Chinese text as explicit short text placeholders.

Prompt structure:

1. `Campaign Style Lock`.
2. Asset name and channel.
3. Store type, product/service, audience, campaign goal.
4. Composition and key visual.
5. Exact on-image Chinese text placeholders.
6. Lighting, colors, materials, mood.
7. Print/social readability constraints.
8. IP/compliance constraints.
9. Size or aspect ratio.

Use `clean readable Chinese text placeholders` when the image model may render text poorly, and also provide editable text separately in the markdown handoff.

## Direct Image Generation

Use `scripts/generate_image.py` for OpenAI-compatible Images APIs.

Environment:

```dotenv
IMG_BASE_URL=https://api.openai.com/v1
IMG_MODEL=gpt-image-1.5
IMG_API_KEY=your-api-key
```

Compatible aliases: `OPENAI_BASE_URL`, `OPENAI_API_BASE`, `OPENAI_IMAGE_MODEL`, `OPENAI_MODEL`, `OPENAI_API_KEY`.

Command examples:

```bash
python scripts/generate_image.py --mode prompt --prompt-file prompts/poster-01.txt --job-dir generated-campaigns/guzi-launch-20260515-180000 --asset-type poster --size 1024x1536
python scripts/generate_image.py --mode image --prompt-file prompts/social-xhs-01.txt --job-dir generated-campaigns/guzi-launch-20260515-180000 --asset-type social --size 1024x1024
python scripts/generate_image.py --prompt "original product display photo for a trendy anime merch store..." --job-dir generated-campaigns/guzi-launch-20260515-180000 --asset-type product
```

Rules:

- If config is missing and `--mode auto`, save and print prompts instead of failing.
- Save prompts to `<job-dir>/prompts/`.
- Save images under `<job-dir>/<asset-type>/`.
- Use `poster`, `rollup`, `window`, `price-tag`, `event-page`, `social`, `product`, `extra`, or `custom`.
- Do not print real API keys.

Use `scripts/create_pack.py` to scaffold a delivery folder when helpful:

```bash
python scripts/create_pack.py --slug guzi-launch --store-type "谷子店" --audience "大学生" --campaign-goal "新品上架"
```

## Output Format

For a strategy or prompt-only response, output:

1. **Store Marketing Brief**
2. **Research Notes** with sources if used
3. **Campaign Thesis**
4. **Offer And Event Mechanics**
5. **Campaign Style Lock**
6. **Copy Bank**
7. **Print Asset Plan**
8. **Social Pack**
9. **Event Playbook**
10. **Image Prompts**
11. **Assumptions / Defaults Used**
12. **Self-review Scorecard**

For a generated pack, output:

1. **What I Made**
2. **Campaign Thesis**
3. **Generated Files**
4. **Usage Notes For The Store Owner**
5. **Assumptions / Defaults Used**
6. **Next Test Ideas**

## Self-review Scorecard

Before final delivery, check:

- Could a passerby understand the offer in 1 second?
- Does every asset have one clear job?
- Is the copy category-native instead of generic?
- Is the CTA concrete and local-store actionable?
- Are print assets readable at the likely viewing distance?
- Do social posts feel native to the platform?
- Does the event mechanic have rules, timing, staff needs, and a low-budget setup?
- Are image prompts consistent through one style lock?
- Are assumptions and researched facts separated?
- Is the final package useful to a busy store owner without extra explanation?
