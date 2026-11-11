# Visual Creation Syllabus — Design, Explainers, Image, 3D, Motion

Companion to the **Visual Creation Track — Tracker** (Claude Doc). 28 working weeks + 1 Christmas buffer.
Runs 26 Oct 2026 → 16 May 2027, alongside the Business & Finance syllabus.

---

## How to use this syllabus

**Weekly shape.** One weekend build session of 2–3 h, on the weekend day finance doesn't use:

| Block | Time | What happens |
|---|---|---|
| Review | 10 min | Skim the week's swipe-file entries; pick one to steal from |
| Learn | 30–40 min | The week's concepts + the listed reading/watching |
| Build | 90 min | The "Do" task, following the spine below |
| Log | 10–15 min | Save deliverable, prompts, settings, time taken; tick the tracker |

**Daily (10 min).** Swipe file: save one visual you saw today, name the pattern/technique, one line on why it works or fails.

**Rule.** A box is ticked only when the deliverable exists as a file **and** its prompts/settings are logged.

**After 25 Apr 2027** (finance finished): move to two sessions a week; Stages 6–7 can compress.

### The spine — used for every piece

1. **Brief** — audience, the one takeaway or feeling, format, constraints.
2. **References** — moodboard, examples, chosen pattern or chart type.
3. **Structure** — wireframe, storyboard, shot list or blockout *before* generating.
4. **Generate** — AI pass using templates from your library.
5. **Critique** — against the brief and the principles, not "does it look cool".
6. **Refine** — targeted edits, not full rerolls.
7. **Assemble** — combine, add sound/annotation, export.
8. **Ship & log** — final prompts, seeds, settings and assets into the library.

### Folder structure

```
visual-track/
  00-swipe-file/
  01-literacy/
  02-information-design/
  03-explainers/
  04-image/
  05-3d/
  06-motion/
  07-pipelines/
  08-capstone/
  library/
    patterns/        # one page per chart/diagram/explainer pattern
    prompts/         # tested prompt templates, with tool + date
    design-system/   # tokens, palettes, type scale, icon style
    playbook.md      # which tool for which job, and why
```

Naming: `wk07_design-system_v2.html`. Prompt log line: `date | tool+model | prompt | seed/settings | verdict`.

### Stage gates

| Gate | Week | Pass condition |
|---|---|---|
| Stage 0 check | 2 | 10 critiques done; can name the principle behind any fix |
| Stage 1 gate | 6 | ≥8/10 on a cold "pick the right visual" quiz; pattern library complete |
| Stage 2 gate | 9 | Cold brief → shareable explainer in ≤60 min that a test reader can explain back |
| Stage 3 gate | 13 | Image-in-your-head → image you rate ≥8/10 in ≤30 min; ≥20 tested prompts |
| Stage 4 gate | 18 | Lit, rendered scene containing an AI-generated asset, from brief in one session |
| Stage 5 gate | 23 | Short film + animated explainer done; a fresh viewer can summarise each |
| Stage 6 gate | 26 | Two pipeline runs documented with time and cost logs |
| Final | 28 | Capstone shipped; playbook written; portfolio page published |

---

## Stage 0 — Visual literacy (weeks 1–2)

Why some visuals work and others don't. Everything later is judged against this.

### Week 1 — Hierarchy and Gestalt · 26 Oct–1 Nov

**Goal:** explain where the eye lands first, and why.

**Learn**
- Visual hierarchy levers: size, weight, colour, contrast, position, whitespace.
- The four basics: contrast, repetition, alignment, proximity.
- Gestalt laws: proximity, similarity, closure, continuity, figure/ground, common region.
- Squint test: blur your eyes; what survives is the hierarchy.

**Read:** *The Non-Designer's Design Book* (Robin Williams) — the chapters on the four principles.

**Do**
- Set up the swipe file.
- Take one dense slide or document page from your own work (sanitised). Redesign it twice: once by hand-sketching, once by asking Claude to rebuild it as an HTML artifact applying the principles. Critique Claude's version against them.
- Start the visual critiques: for each, note first fixation, what's grouped, what's fighting for attention, one fix.

**Deliverables:** swipe file (≥3 entries) · principles note with an example of each · 3 critiques · before/after slide.

**Check yourself:** for any visual, can you say in one sentence what is seen first and which lever caused it?

### Week 2 — Colour, type, grids · 2–8 Nov

**Goal:** make deliberate colour and type choices instead of defaults.

**Learn**
- Colour: HSL thinking; palette types (monochrome, analogous, complementary); semantic colour (one accent for "look here"); greys do most of the work.
- Accessibility: WCAG AA contrast 4.5:1 for body text; colour-blind-safe palettes; never encode meaning in colour alone.
- Type: serif vs sans; a modular type scale; line length ~45–75 characters; line height; weight before size.
- Grids: column grids, spacing scales (4/8 px), bento layouts; F and Z reading patterns.

**Read:** *Refactoring UI* (Wathan & Schoger) — hierarchy, colour, typography sections. Skim *Thinking with Type* (Ellen Lupton) on text.

**Do**
- Build a one-page HTML artifact with Claude using a stated type scale and a 5-colour palette; check contrast with a checker.
- Finish the remaining 7 critiques.

**Deliverables:** colour/type/grid note · 7 critiques · one-page palette+type test.

**Stage 0 check:** 10 critiques done; you can name the principle behind every fix.

---

## Stage 1 — Information design (weeks 3–6)

Choosing the right visual for the question. Output is your **pattern library**: one page per pattern with *what it is · the question it answers · when not to use it · an example*.

Core rule: **start from the question, not the data.** Use the FT *Visual Vocabulary* categories as the master map: deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, flow.

### Week 3 — Charts I: comparison, change over time, composition · 9–15 Nov

**Learn**
- Comparison/magnitude: bar (horizontal for long labels; always start at zero), dot plot, lollipop, ranked bar.
- Change over time: line (zero not required), slope chart (two points in time), area, small multiples instead of spaghetti lines.
- Part-to-whole: stacked bar vs 100% stacked, treemap, waterfall (the P&L bridge), why pies rarely help (>3 slices).
- Declutter: remove borders, gridlines, legends where direct labels work; title states the finding.

**Read:** *Storytelling with Data* (Cole Nussbaumer Knaflic) — choosing an effective visual; clutter. FT Visual Vocabulary poster.

**Do (finance crossover):** using the Mash Direct or Around Noon P&L from the finance track, build in a Claude artifact (Chart.js): revenue trend line · margin slope chart · cost composition stacked bar · revenue-to-profit waterfall.

**Deliverables:** 4 charts + ≥8 pattern-library pages.

### Week 4 — Charts II: distribution, relationship, flow; chart crimes · 16–22 Nov

**Learn**
- Distribution: histogram (bin choice changes the story), box plot, violin, strip/beeswarm, ECDF.
- Relationship: scatter, bubble, heatmap, connected scatter. Correlation ≠ cause.
- Flow: Sankey, funnel, alluvial. Maps briefly: choropleths must be normalised (per capita, not raw counts).
- Chart crimes: truncated bar axes, dual y-axes, 3D, rainbow colour scales, area/size misperception, means hiding skew.

**Read:** *Fundamentals of Data Visualization* (Claus Wilke, free online) — distributions; proportional ink.

**Do**
- Ask Claude for a skewed synthetic dataset (e.g. order values). Show it as histogram + box plot; annotate mean vs median.
- A scatter of two business variables; a Sankey of cash flowing through a company.
- Make one deliberately misleading chart and its honest twin.

**Deliverables:** 6 charts · crime/fix pair · library pages updated.

### Week 5 — Process and system diagrams · 23–29 Nov

**Learn**
- Flowchart: one direction, decision diamonds, one verb per box.
- Swimlane: who does what; handoffs are where things break.
- Sequence diagram: actors, lifelines, messages — ideal for API and LLM request flows.
- State machine: states, transitions, triggers.
- Architecture: the C4 model (context → container → component → code); pick the zoom level for the audience.
- ER and data-flow diagrams.

**Read:** c4model.com overview; Mermaid documentation (flowchart, sequence, state, ER).

**Do (work crossover, sanitised):** for a system you work on — C4 context + container diagrams; a sequence diagram of an LLM/agent request with tool calls; a swimlane for a client onboarding process.

**Deliverables:** 5 diagrams · Mermaid snippets saved to `library/patterns/`.

### Week 6 — Conceptual diagrams and explainer patterns · 30 Nov–6 Dec · **Stage 1 gate**

**Learn**
- Conceptual: mind map vs concept map (concept maps label the links), timeline/roadmap, 2×2 matrix, Venn, pyramid, journey map, driver tree (e.g. ROIC tree), layered stack, iceberg.
- Explainer patterns: annotated diagram, small multiples, progressive disclosure, scrollytelling, before/after, analogy-first, zoom (overview → detail), worked example.

**Read:** Bret Victor, *Explorable Explanations* (essay); browse Nicky Case's explorables.

**Do:** a progressive-disclosure or scrollytelling explainer of *how the three financial statements link* (counts toward finance too).

**Stage 1 gate:** have Claude generate 10 cold "what would you show?" questions. Answer each in under a minute with pattern + justification. Pass at ≥8/10. Pattern library complete.

---

## Stage 2 — Explainers on demand (weeks 7–9)

Turn Stages 0–1 into a fast, repeatable service for yourself and the people you work with.

### Week 7 — Brief template and personal design system · 7–13 Dec

**Learn**
- Explainer brief fields: audience, what they already know, the single takeaway, likely misconceptions, context of use (live screen-share, async, mobile), format, length.
- Design tokens: palette (incl. chart palette), type scale, spacing scale, radius, icon style, diagram conventions.
- Explainer writing: headline as claim, chunking, one idea per screen, concrete example before abstraction.

**Do**
- Write the brief template.
- Build a design-system page (HTML artifact) showing your tokens in use.
- Write an explainer system prompt v1 that applies brief + design system. Optional engineer's route: package it as a Claude skill with skill-creator.

**Deliverables:** brief template · design-system file · explainer prompt v1.

### Week 8 — Explainers 1–3 · 14–20 Dec

**Do**
1. Work: a technical concept (e.g. how RAG or tool-using agents work) for a non-technical client.
2. Finance: working capital and the cash conversion cycle.
3. Finance: break-even, as an interactive slider explainer.

Time each from brief to shareable. Target: under 45 min by explainer 3.

**Deliverables:** 3 explainers · time log · prompt notes on what needed fixing.

### Buffer · 21–27 Dec

Catch-up or rest.

### Week 9 — Explainers 4–5, testing, retro · 28 Dec–3 Jan · **Stage 2 gate**

**Do**
- Explainer 4: something a colleague or someone you mentor actually asked about.
- Explainer 5: give it to someone; ask them to explain it back. Note where they stumble.
- Retro: update the prompt to v2 based on recurring fixes.

**Stage 2 gate:** cold brief → shareable explainer in ≤60 min that a test reader can explain back.

---

## Stage 3 — Image generation (weeks 10–13)

Getting what's in your head onto the screen, consistently.

### Week 10 — Tool survey and prompt anatomy · 4–10 Jan

**Learn**
- Intuition-level mechanics (link to your Master's): latent diffusion, guidance scale, seeds, samplers; autoregressive/multimodal image models vs diffusion, and why they differ on text rendering and instruction-following.
- Prompt anatomy: subject · action · setting · composition/shot · camera and lens · lighting · style/medium · mood · colour · aspect ratio. Negative prompts where supported.
- Reproducibility: seeds, fixed settings, logging.

**Do**
- Ask Claude to search for the current landscape before you start (it changes monthly). Candidates: Midjourney, GPT and Gemini image models, Flux, Ideogram, Recraft, Krea.
- Run the same 3 prompts (a portrait, a product shot, an infographic with text) in 4 tools.
- Score each tool on: quality, prompt adherence, text rendering, consistency features, editing, API access, cost, commercial licence.

**Deliverables:** tool comparison sheet · prompt anatomy template.

### Week 11 — References and consistency · 11–17 Jan

**Learn**
- Image, style and character references; seed locking; LoRAs (what they are, when worth training).
- Character sheets: turnaround (front/side/back), expressions, outfit; fixed palette and lighting.
- Moodboards as a prompt input.

**Do:** design an original character and world. Character sheet + 4 scenes that keep identity.

**Deliverables:** character bible (sheet, palette, prompt block, references).

### Week 12 — The editing toolkit · 18–24 Jan

**Learn**
- Inpainting, outpainting, region and instruction-based edits; background removal; AI upscaling.
- Text in images; vector generation for icons and logos.
- Light compositing in Photopea, Figma or Affinity: layers, masks, colour matching.

**Do**
- Fix 3 flawed generations without rerolling.
- A poster with legible headline text.
- A small icon set in your design-system style (vector).

**Deliverables:** 3 before/after fixes · poster · icon set.

### Week 13 — Series and ComfyUI · 25–31 Jan · **Stage 3 gate**

**Learn**
- ComfyUI basics: checkpoint loader, text encode, KSampler, VAE decode; ControlNet (pose, depth, edges); image-prompt adapters. Run locally or on a cloud GPU.

**Do**
- Finish the 12-image series: one world, a simple narrative arc. **Keep it** — it becomes the storyboard source in Stage 5.
- Build one ControlNet workflow (e.g. pose-matched character).

**Stage 3 gate:** describe an image in writing first; reach a result you rate ≥8/10 for match in ≤30 min. Prompt library ≥20 tested prompts.

---

## Stage 4 — 3D (weeks 14–18)

Controllable geometry, camera and light — the backbone for consistent motion later.

### Week 14 — Blender I: interface and modelling · 1–7 Feb

**Learn:** viewport navigation; object vs edit mode; grab/rotate/scale; extrude, inset, loop cut, bevel; origins; real-world scale and units.

**Watch:** Blender Guru's beginner (donut) series, or Blender's official fundamentals videos — first few parts.

**Do:** block out a desk scene: mug, lamp, laptop, notebook.

**Deliverables:** blockout `.blend` + viewport screenshot.

### Week 15 — Blender II: modifiers, materials, lighting · 8–14 Feb

**Learn**
- Modifiers: subdivision, mirror, array, bevel, boolean, solidify. Clean topology basics.
- UV unwrapping intuition; Principled BSDF; PBR texture maps.
- Lighting: HDRI environments, three-point lighting, light temperature for mood.

**Do:** materials and lighting on the desk scene.

### Week 16 — Blender III: camera, render, animation · 15–21 Feb

**Learn**
- Camera: focal length, depth of field, composition (Stage 0 applies).
- Eevee vs Cycles; samples and denoising; render passes.
- Keyframes, graph editor, a turntable animation.

**Do:** final still render + 5 s turntable.

**Deliverables:** first finished scene (still + turntable).

### Week 17 — AI 3D and cleanup · 22–28 Feb

**Learn**
- Text-to-3D and image-to-3D; typical flaws (messy topology, baked lighting, bad UVs).
- Cleanup: remesh, decimate, retopology basics, re-texturing.
- Auto-rigging (e.g. Mixamo) and posing.
- Overview: photogrammetry and Gaussian splatting from phone captures.

**Do:** survey current tools (Meshy, Tripo, Hunyuan3D, Rodin, etc.). Generate your Stage 3 character from its sheet; clean up; rig; pose in the desk scene.

**Deliverables:** cleaned, rigged character in scene · tool notes.

### Week 18 — Blender Python and MCP · 1–7 Mar · **Stage 4 gate**

**Learn**
- `bpy` API and the scripting workspace; procedural scenes; geometry nodes intro.
- Blender MCP: Claude driving Blender in natural language. Needs a desktop setup (Claude Desktop or Claude Code), not the mobile app.

**Do**
- Script a data-driven 3D chart from finance data (e.g. margin by year as extruded bars).
- Build one scene entirely through Claude + MCP; note where it helps and where it fumbles.

**Stage 4 gate:** from a written brief, produce a lit, rendered scene containing an AI-generated asset in one session.

---

## Stage 5 — Motion & film (weeks 19–23)

Telling stories in time: generative video, sound, edit, and code-driven animation.

### Week 19 — Film grammar and storyboarding · 8–14 Mar

**Learn**
- Shot sizes (extreme close-up → extreme wide), angles, camera moves (pan, tilt, dolly, truck, crane, orbit, handheld), lens feel.
- Continuity: 180° rule, eyeline, screen direction, match cuts, J and L cuts.
- Structure for 30–60 s: hook in the first 3 seconds, one turn, a clear ending.

**Read:** *Grammar of the Shot* and *Grammar of the Edit* (Bowen & Thompson). Optional: *In the Blink of an Eye* (Walter Murch).

**Do:** script a 45 s short with Claude → shot list (size, angle, move, duration) → storyboard from your Stage 3 series → animatic (stills timed to scratch audio).

**Deliverables:** script · shot list · animatic.

### Week 20 — Video tool survey and keyframe workflow · 15–21 Mar

**Learn**
- Text-to-video vs image-to-video vs start/end-frame control.
- Motion prompting: describe camera motion and subject motion separately; one action per clip.
- Constraints: clip length, resolution, credit cost.

**Do:** have Claude search the current landscape first (Seedance, Higgsfield, Kling, Veo, Runway, Sora and whatever is new). Animate the same storyboard frame in 3 tools; score on motion quality, prompt adherence, consistency, camera control, cost, licence.

**Deliverables:** video tool comparison sheet.

### Week 21 — Consistency and camera control · 22–28 Mar

**Learn**
- Carrying identity across shots: same reference frames, same lighting description, same palette.
- Coverage: wide, mid and close of the same beat. Generate takes; select ruthlessly.
- Clip extension; basic lip-sync options.
- Hybrid trick: render a camera move in Blender and use it as guidance where tools allow.

**Do:** generate every shot of the short, ≥3 takes each; pick selects.

**Deliverables:** selects folder + take log.

### Week 22 — Sound and edit · 29 Mar–4 Apr

**Learn**
- Sound layers: voice-over, music, SFX, ambience. Bad audio ruins good picture.
- Mixing: voice clearly above music; a consistent loudness target (around −14 LUFS is a common platform target).
- Editing in DaVinci Resolve or CapCut: timeline, trims, pacing, sparing transitions.
- Simple colour grade for one consistent look.
- Export: H.264, 1080p; 16:9 and 9:16 versions.

**Do:** VO (e.g. ElevenLabs), music (generated or licensed), SFX; edit, grade, export.

**Deliverables:** short film v1.

### Week 23 — Code-driven motion · 5–11 Apr · **Stage 5 gate**

**Learn**
- Remotion (React), Manim (Python), Motion Canvas (TypeScript).
- When code beats generative: precision, diagrams, data, text, cheap edits.
- Claude writes the scenes; you direct and review renders.

**Do:** a 60 s animated explainer of a Stage 1–2 concept (e.g. how a DCF works, or how RAG works) with VO.

**Stage 5 gate:** short film and explainer both done; a fresh viewer can summarise each in one sentence.

---

## Stage 6 — Composition pipelines (weeks 24–26)

Combining media, with each one used for what it's best at.

### Week 24 — Pipeline design · 12–18 Apr

**Learn**
- Strengths by medium: generative image/video for texture, realism and mood; code for precision; 3D for controllable camera and consistent geometry; human edit for timing and taste; Claude as orchestrator (script, shot list, prompts, code).
- Hybrid patterns: 3D blockout → depth/edge pass → styled generation; image keyframes → video; code-animated diagrams over generated b-roll.
- Asset management: folder conventions, versioning, prompt/seed logs.
- Rights: check each tool's commercial terms; disclosure norms; avoid real people's likenesses and others' IP; content credentials (C2PA) as a concept.

**Do:** write pipeline templates for three outputs: explainer video, product ad, short narrative film. Each lists steps, tool per step, handoff format, time and cost estimate.

**Deliverables:** 3 pipeline templates · asset-management conventions.

### Week 25 — Pipeline run 1: product ad · 19–25 Apr

**Do:** a 15–30 s ad for a fictional product, in 16:9 and 9:16. Run the full spine. Log time and cost per step.

**Deliverables:** ad (both ratios) · run log.

### Week 26 — Pipeline run 2: concept explainer video · 26 Apr–2 May · **Stage 6 gate**

**Do:** a 60–90 s explainer mixing code-driven motion, generated b-roll and at least one 3D shot.

**Stage 6 gate:** both runs documented with time and cost logs; pipeline templates updated with what actually happened.

---

## Stage 7 — Capstone (weeks 27–28)

### Week 27 — Capstone build · 3–9 May

Pick one idea that's yours. Options: a short film of your own concept; a pilot of an explainer series; a visual identity plus launch video for a side project.

**Do:** brief → references → structure → generation, using your playbook.

### Week 28 — Capstone finish and playbook · 10–16 May · **Final gate**

**Do**
- Assemble, polish, export.
- Write `playbook.md`: which tool for which job and why, your default pipelines, prompt templates, known failure modes.
- Publish a portfolio page (an artifact) linking the best piece from each stage.

---

## Appendix A — Chart chooser (by question)

| The question | First choice | Alternatives | Avoid |
|---|---|---|---|
| Which is bigger? | Horizontal bar | Dot plot, lollipop | 3D bars, pies with many slices |
| How did it change? | Line | Slope (2 points), small multiples | Many overlapping lines |
| What is it made of? | Stacked bar | Treemap, 100% stacked | Pie with >3 slices |
| How did we get from A to B? | Waterfall | Annotated bar | Separate disconnected bars |
| How is it spread? | Histogram | Box, violin, ECDF | Showing only the mean |
| Are these related? | Scatter | Bubble, heatmap | Dual-axis line chart |
| Where does it flow? | Sankey | Funnel, alluvial | Spaghetti arrows |
| How does it work? | Flowchart / sequence | Swimlane, state machine | Prose |
| How is it built? | Architecture (C4) | Layered stack | One giant box diagram |
| How do ideas relate? | Concept map | Mind map, 2×2, Venn | Bullet lists |
| What's the plan? | Timeline / roadmap | Gantt | Table of dates |

## Appendix B — Templates

**Explainer brief**
```
Audience:            
They already know:   
The one takeaway:    
Likely misconception:
Context of use:      (live share / async / mobile)
Format & length:     
Pattern(s):          
```

**Image prompt**
```
[subject + action], [setting], [shot size + angle], [lens/camera],
[lighting], [style/medium], [mood], [palette], [aspect ratio]
Refs: [character ref] [style ref]   Seed: ___   Avoid: ___
```

**Video shot prompt**
```
Shot [n] — [size], [angle], [duration]s
Camera: [move, speed]
Subject: [one action]
Start frame: [file]   End frame: [file, optional]
Continuity: [lighting, palette, wardrobe notes]
```

**Pipeline run log**
```
Step | Tool + model | Input | Output file | Time | Cost | Notes
```

## Appendix C — Core reading and references

- Robin Williams — *The Non-Designer's Design Book*
- Adam Wathan & Steve Schoger — *Refactoring UI*
- Ellen Lupton — *Thinking with Type*
- Cole Nussbaumer Knaflic — *Storytelling with Data*
- Claus Wilke — *Fundamentals of Data Visualization* (free online)
- Edward Tufte — *The Visual Display of Quantitative Information* (optional, classic)
- Financial Times — *Visual Vocabulary*
- Simon Brown — the C4 model (c4model.com)
- Bret Victor — *Explorable Explanations*
- Christopher Bowen & Roy Thompson — *Grammar of the Shot*, *Grammar of the Edit*
- Walter Murch — *In the Blink of an Eye* (optional)
- Official docs: Mermaid, Chart.js, Blender manual, Remotion, Manim, and each generative tool you adopt

## Appendix D — Watch-outs throughout

- Defaults are decisions you didn't make — choose palette, type and chart type on purpose.
- The title should state the finding, not the topic.
- Averages hide skew; show the distribution when it matters.
- Tool landscapes change monthly; re-survey before committing, and log the date with every prompt.
- Check commercial licence terms before anything leaves your laptop.
- Don't generate real people's likenesses or others' characters and brands.
