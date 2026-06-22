---
name: dryfood-ig-visuals
version: 1.0.0
description: |
  Produce Ajinomoto dry-food Instagram post visuals in the in-house art style,
  one square post per SKU. Use when the user asks to design, lay out, or build IG / social
  post graphics, a content calendar, or product creatives for the dry-food range — AGF
  Blendy Coffee, Tumix, Seri-Aji, Mayonnaise, Hondashi, MSG (Aji-no-moto), Aji-Shio — or
  any single one of them. Reproduces the layout grid, brush fonts, bold colour backgrounds,
  layer stacking and engagement formats; leaves labelled placeholders for real food photos
  the user supplies. Triggers: "make an IG post for <SKU>", "dry food calendar visuals",
  "design a product post", "social creative for Blendy/Hondashi/Mayonnaise/etc".
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Dry-food IG visuals (house style)

Distilled from ~30 finished posts by the previous in-house designer, kept in the team's
design archive. This skill
reproduces that visual system and applies it to the 7 dry-food SKUs, **one square post per
SKU**, with each post deliberately different from the others so the feed never looks
repetitive.

**Read `references/style-guide.md` first** — it is the single source of truth for the
grid, fonts, colours, layer stack, layout archetypes and the variety matrix. This file
covers *how to run a job*; the style guide covers *what the style is*.

## The 7 SKUs
AGF Blendy Coffee · Tumix · Seri-Aji · Mayonnaise · Hondashi · MSG (Aji-no-moto) · Aji-Shio

## Hard rules
1. **Real photos only for any finished-food or product element.** Never illustrate the
   food or the pack. Until the user supplies the photo, render a **labelled placeholder**
   box and tell them exactly what shot is needed (see step 4).
2. **One SKU per visual.** No multi-SKU compositions for the calendar.
3. **Variety is mandatory.** Every post must differ from its neighbours on **≥3 axes** of
   the variety matrix (background hue, watermark motif, layout archetype, product quadrant,
   supporting element, headline treatment). Track this across the set — never ship two
   adjacent posts in the same archetype + colour.
4. **Canvas is always 1080×1350 portrait (4:5).** Never square. Print export 4320×5400.
5. **Ajinomoto lockup is LOCKED top-right on every post** — fixed position & size, enforced
   in code (`LOGO_BOX`), not spec-overridable. See style guide §2a.
6. **Brand frame is constant.** Fixed corner furniture (see style guide §2).
7. **Ask for any missing asset.** Brand logos, product packshots, lifestyle photos — if you
   need it and don't have it, ask rather than fabricate.

## Workflow per post

1. **Confirm the brief.** SKU, key message/headline, and which layout archetype + base
   colour (propose from the style-guide table; the suggested assignment already spreads the
   7 SKUs across archetypes A–F). If doing the whole calendar, lock the per-SKU archetype/
   colour plan up front so the variety matrix is satisfied by construction.

2. **Write the spec.** Copy `specs/_TEMPLATE.json` to `specs/<sku>.json` and fill it:
   background, pattern, the image boxes (hero + packshot), highlight bar, headline + SKU
   caption, and furniture. Coordinates are fractions (0..1) of the square canvas. A worked
   example is `specs/blendy-coffee.json`.

3. **Render with placeholders.** Run the engine:
   ```
   python scripts/render_post.py specs/<sku>.json --size 1080
   ```
   Output lands in `output/<sku>_1080.png`. Open it, sanity-check the composition (no text/
   placeholder collisions, packshot has breathing room, furniture clear of the margins),
   and nudge coordinates in the spec until it reads well. Render at `--size 4500` for the
   final print-grade file.

4. **Report needed photos.** For each placeholder, give the user a short, concrete shot
   list — what product/dish, angle, background (cut-out vs edge-bleed). Example:
   > For the Blendy post I need: (1) **packshot** — Blendy jar, front, clean cut-out on a
   > transparent background; (2) **hero** — coffee being poured into a white mug, overhead,
   > steam visible. Drop them in `assets/photos/blendy/` and I'll swap them in.

5. **Swap in real photos & finalise.** Point each image element's `"file"` at the supplied
   photo (set `"placeholder": false`), re-render, review, export at 4500².

## The render engine (`scripts/render_post.py`)
Deterministic Pillow renderer. It guarantees the fixed brand frame + the three bundled
fonts identically on every post, and reads one JSON spec for everything that varies. Layout
archetypes are expressed through the spec (background, pattern kind, image boxes, text
positions) — see `specs/_TEMPLATE.json` for the full schema and `references/style-guide.md`
§6 for what each archetype A–F looks like. Patterns supported: `dots`, `diagonal`,
`ground` (bottom colour strip), `glyphs` (repeated rotated watermark), `none`.

## Bundled assets
- `assets/fonts/` — the three real fonts from the previous designer's kit: **UID Deep sea** (brush
  headlines/captions — the brand personality face), **DIN Condensed** (callouts/labels),
  **Myriad Pro** (fine print).
- `assets/brand/` — *(you create this)* drop the official **Eat Well / Aji signature**,
  the **Ajinomoto corporate mark**, and any per-SKU product logos (Blendy, Seri-Aji, …)
  here as transparent PNGs. Until present, the renderer draws a typographic stand-in so
  layouts are still reviewable. **Ask the user for these logos.**
- `assets/photos/<sku>/` — *(you create this)* the user's supplied real packshots and
  lifestyle photos per SKU.

## First-run checklist for the calendar
- [ ] Lock the 7-SKU plan (archetype + base colour each) so the variety matrix holds.
- [ ] Get the brand furniture PNGs (Aji signature, corporate mark, product logos).
- [ ] Build each spec, render with placeholders, send the per-SKU photo shot-list.
- [ ] Collect photos → swap in → review → export 4500².
