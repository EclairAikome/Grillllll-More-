# House style guide: Ajinomoto Instagram post visuals

Distilled from ~30 finished posts by the previous in-house designer (One Piece x Ajinomoto
gyoza collab, product posts, engagement posts, POSM). This is the visual DNA to reproduce
for the **dry-food calendar** (AGF Blendy Coffee, Tumix, Seri-Aji, Mayonnaise, Hondashi,
MSG, Aji-Shio). The IP (One Piece / TOEI) is collab-specific and is **dropped** for dry
food; keep everything else.

---

## 1. Canvas & export

- **Aspect:** **1080 × 1350 portrait (4:5)** — ALWAYS. This is the Instagram feed post
  layout. Never square, never any other ratio.
- **Working/export size:** web **1080 × 1350**; print-grade **4320 × 5400** (4×, ≈ 300 DPI).
  The renderer keeps 4:5 at any width (`height = width × 5/4`).
- **Safe margins:** keep logos and headlines inside a ~6% margin (≈ 65 px on the 1080-wide
  canvas). Hero photos may **bleed off** edges; text and brand furniture never do.

## 2. The fixed "frame" — corner furniture (constant on every post)

This is what makes the feed look like one brand. Positions are constant; only the
center changes.

| Slot | Content | Notes |
|---|---|---|
| **Top-right (LOCKED)** | "Eat Well, Live Well." tagline above the round **Aj** logo + **AJINOMOTO** wordmark | See §2a — fixed position & size, non-negotiable on every post. |
| **Top-left** | Campaign / category lockup | Collab used the One Piece logo here. For dry food → a category/campaign banner or the specific product logo (e.g. *Blendy*, *Seri-Aji* logo). Ask user for it. |
| **Bottom-left** | Small corporate / licensing marks | Collab: TOEI + ©E.O/S.T.A. For dry food: Ajinomoto corporate mark, or leave empty. |

Furniture sits on the **top layer**, always above photos and patterns.

### 2a. Ajinomoto lockup — MANDATORY locked placement

The "Eat Well, Live Well." + **Aj** + **AJINOMOTO** lockup is **locked to a fixed top-right
box on every single post**. Measured from the reference Seri-Aji creative (1080×1350). This
is a hard requirement — it is enforced in code (`LOGO_BOX` in `render_post.py`) and **cannot
be overridden by a spec**.

| Property | Value | On 1080×1350 |
|---|---|---|
| Lockup **width** | 0.213 × canvas width | ≈ 230 px |
| **Right margin** (gap to right edge) | 0.055 × canvas width | ≈ 59 px |
| **Top margin** (gap to top edge) | 0.047 × canvas height | ≈ 63 px |
| Aspect | follows the supplied PNG (~1.53:1) | ≈ 230 × 150 px |
| Anchor | TOP-RIGHT | right edge ≈ x:1021, top ≈ y:63 |

Supply the real lockup as a transparent PNG at `assets/brand/eat-well-aji.png`. It is scaled
to the locked width and pinned to the locked top-right corner. Until it exists, a
typographic stand-in is drawn **in the exact same box** so the position is always correct.

## 3. Typography (fonts bundled in `assets/fonts/`)

| Role | Font | Treatment |
|---|---|---|
| **Headline & SKU caption (personality font)** | **UID Deep sea** (`UID Deep sea.ttf`) — a hand-painted brush/marker face | ALL CAPS for headlines, Title Case for SKU captions. Almost always with a **stroke outline** (white text + dark outline, or dark text + white outline) and frequently a soft drop shadow. This font carries the whole brand voice. |
| **Condensed callouts / labels / badges** | **DIN Condensed** (`DINCondensed-VF.ttf`) — tall narrow caps | Used for tags, small all-caps labels, "No.1" style callouts, pack-size text. |
| **Body / fine print / disclaimers** | **Myriad Pro Regular** (`MyriadPro-Regular.otf`) | Neutral sans for legal lines, multi-line descriptive copy. |

Headline sizing on the 4500 canvas: ~260–360 px cap height for primary headlines,
~150–200 px for SKU captions. Letter-spacing slightly loose on the brush font.

## 4. Colour

**One dominant saturated background colour per post**, chosen to echo the SKU's packaging.
Sampled from the previous designer's finished files:

| Hex | Use seen |
|---|---|
| `#D02329` / `#D03543` | Pork / red product, brand red |
| `#69903D` | Chicken / green product |
| `#F0857F` | Coral / "Pops" lighter product |
| `#5C9EDA` | Chicken-&-veg / blue product |
| `#1F1134` (navy) `#323D2D` (olive) | Dark split-panel grounds (Product post 2) |

Accents: cyan highlight bars (~`#5FD0E0`), yellow "ground" strips (~`#F4D21E`), white.

**Per-SKU starting palette for dry food** (confirm with user, adjust to real packaging):

| SKU | Suggested base | Rationale |
|---|---|---|
| AGF Blendy Coffee | warm coffee brown `#6B4226` / cream `#E8D9C0` | coffee tones |
| Tumix | bright accent (red/orange) `#E2511E` | confirm packaging |
| Seri-Aji | deep red `#C0202B` | seasoning red |
| Mayonnaise | soft butter yellow `#F6D55C` | mayo |
| Hondashi | dashi gold / teal `#E0A33C` or `#1E8C8C` | broth |
| MSG (Aji-no-moto) | clean red-on-white `#E20A17` | iconic red/white |
| Aji-Shio | cool grey-blue `#5B7C99` | pepper/salt |

## 5. Layer stack (bottom → top)

1. **Solid colour background**
2. **Tonal pattern / split / ground** — a low-contrast repeated watermark (product
   silhouette, plates, circles, themed icons) at ±10–15% of the base colour; OR a diagonal
   colour split (corners darker); OR a flat colour "ground" strip across the bottom third.
3. **Large hero element** — real food photo (overhead dish, pour, bowl) that may bleed to
   the edges, OR character/illustration. For dry food this is **real photography**.
4. **Product packshot** — the focal SKU, a clean cut-out PNG with a soft drop shadow. The
   single most important object; everything points to it.
5. **Floating accents** — cut-out food pieces, sparkles, flags/banners, motion lines,
   No.1 burst badges.
6. **Headline highlight bar** — optional rounded rectangle behind the headline (cyan/yellow).
7. **Headline + SKU caption** — brush font, outlined.
8. **Corner furniture** — brand logos + copyright, fixed positions, always on top.

## 6. Layout archetypes (rotate these for variety)

The previous designer never repeated the same composition twice in a series. Six recurring archetypes:

- **A — Hero packshot + prop:** product centered/lower, one supporting subject beside it,
  flat colour or patterned bg. (Product post 1/3)
- **B — Split panels:** 2–3 vertical colour panels, one subject + packshot per panel,
  unifying headline across the bottom. (Product post 2)
- **C — Full-bleed lifestyle photo:** appetising dish photo fills the frame, packshot
  inset lower, headline over a translucent/solid strip. (Design 14)
- **D — Watermark pattern + corner product:** tonal repeated motif fills bg, single
  packshot in one quadrant, SKU caption beside it. (Product post 3-01/03)
- **E — Ground-strip showcase:** coloured strip across the bottom holds several packshots
  / dish cut-outs lined up, subject above, headline banner. (Design 5/6)
- **F — Engagement / interactive:** maze, matching, "pick your favourite", clock/compass
  arrangement, quiz question in brush font at the bottom. (Engagement posts, Teaser)

## 7. Variety matrix — MANDATORY across the 7 SKUs

To prevent feed fatigue, **every post in the calendar must differ on at least 3 axes**
from its neighbours. Track these as you build:

1. **Background hue** — no two adjacent posts share a base colour.
2. **Watermark motif** — silhouette vs plates vs circles vs none vs diagonal split.
3. **Layout archetype** — cycle A–F; don't repeat the previous post's archetype.
4. **Product quadrant** — where the packshot sits (lower-centre / right / left / inset).
5. **Supporting element** — lifestyle photo vs prop vs character-free pattern vs engagement.
6. **Headline position & treatment** — top banner vs bottom quiz vs over-photo strip;
   outline colour swapped.

Suggested assignment (one SKU per archetype keeps the set obviously varied):

| SKU | Archetype | Base hue |
|---|---|---|
| AGF Blendy Coffee | C full-bleed lifestyle (coffee pour) | coffee brown |
| Tumix | A hero + prop | orange/red |
| Seri-Aji | E ground-strip showcase | deep red |
| Mayonnaise | D watermark + corner product | butter yellow |
| Hondashi | C lifestyle (miso/dashi bowl) | dashi gold/teal |
| MSG | B split panels OR F engagement | red/white |
| Aji-Shio | A hero + prop | grey-blue |

(Confirm with user; swap freely as long as the matrix stays satisfied.)

## 8. Real-photo rule & placeholder protocol

Any **finished-food / product element must be a real photograph** (user-supplied), never
illustrated. While building, leave a **labelled placeholder**: a dashed-outline box filled
with a faint tint and centred text describing exactly what photo goes there, e.g.

> `[PHOTO — packshot: AGF Blendy jar, front, clean cut-out on transparent bg]`
> `[PHOTO — hero: coffee being poured into white mug, overhead, edge-bleed]`

Then return a short note listing the photos needed for that post. When the user uploads,
swap each placeholder for the real image at the same box and re-render.

## 9. Finishing touches the previous designer consistently applied

- Soft drop shadow under every packshot and cut-out (grounds it on the colour).
- Headline outline stroke ≈ 3–4% of cap height.
- Slight rotation (2–6°) on floating accents and sometimes the headline banner — keeps it
  lively, hand-made.
- Bright "No.1 / Made in Japan / authentic" burst badges where a claim is available.
- Generous breathing room around the packshot; never crowd the focal product.
