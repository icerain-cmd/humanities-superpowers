---
name: performing-close-reading
description: Use when an interpretation must be grounded in specific textual, visual, rhetorical, formal, interface, archival, performative, or material features rather than thematic summary or theoretical labeling.
version: 1.0.0
language: en
license: MIT
---

# Performing Close Reading

## Purpose

Produce accountable interpretations by separating what is observable in an object from the interpretive moves made about it. The skill keeps quotation, description, inference, contextual claim, and theoretical implication distinct while allowing them to interact.

## Contract

**Accepts**
- A supplied passage, image, scene, interface, recording, performance description, archival item, or material artifact.
- Provenance and context available to the researcher.
- A research question or claim to test.

**Requires**
- Direct access to the object or a reliable reproduction.
- Enough context to avoid obvious misidentification or truncation.
- A stated analytical purpose.

**Produces**
- Observation records.
- Interpretive inferences linked to observed features.
- At least one rival reading.
- Contextual claims requiring verification.
- A close-reading gate report.

**May produce**
- A revised local claim.
- A list of additional contextual sources needed.
- `FAIL` when the object is unavailable, corrupted, mistranscribed, or insufficient for the requested conclusion.

**Fails when**
- The requested analysis depends on an object not supplied or reliably accessible.
- Quoted language cannot be distinguished from paraphrase.
- The interpretation requires invented context, authorial intention, or source history.
- The requested conclusion exceeds what the object can establish.

**Guarantees**
- Observations and interpretations are separately labeled.
- Every interpretive claim points to at least one specific feature.
- Rival readings and evidentiary limits remain visible.

**Does not guarantee**
- A uniquely correct interpretation.
- Historical representativeness, authorial intention, or broader causal explanation.
- That local evidence alone can support the manuscript’s largest claim.

## When to use

Use with literary, philosophical, visual, cinematic, digital, performative, architectural, archival, and interface objects. Use when a draft moves from quotation directly to theme, when theory substitutes for attention, or when a single local feature is made to represent an entire period or culture.

Do not use this skill to summarize a whole book from memory, identify an absent image, or produce authoritative meaning without examining the object.

## Inputs required

Collect:

1. Exact object or reliable reproduction.
2. Provenance: creator, date, edition, location, version, or capture context when available.
3. Unit of analysis: word, sentence, motif, frame, gesture, interaction, layout, sequence, material trace, or relation.
4. Research question and target claim.
5. Relevant contextual facts already verified.
6. Translation status and edition differences where applicable.

If the object is partial, identify the boundary explicitly.

## Procedure

### 1. Establish the object record

Describe what has been supplied and what has not. Record edition, image crop, screenshot date, transcription quality, translation, and missing context. Assign a verification state to provenance claims.

### 2. Observe before interpreting

Select observation dimensions appropriate to the object. Do not apply a text-only checklist to every medium.

**Textual and rhetorical objects**
- diction, syntax, rhythm, voice, address, quotation, repetition, omission, figuration, paragraph or argumentative sequence;

**Still images and visual artifacts**
- framing, composition, scale, perspective, visual hierarchy, color relation, illumination, gaze, cropping, caption relation, surface, and material support;

**Film, sound, and time-based media**
- shot scale, camera movement, duration, cut, transition, sequencing, sound-image relation, silence, rhythm, performance, and temporal discontinuity;

**Interfaces and interactive systems**
- affordance, constraint, information hierarchy, navigation path, default state, feedback, response time, error state, permission, state transition, visibility, and the relation between displayed options and unavailable actions;

**Performance, architecture, and material objects**
- gesture, spatial organization, movement path, audience relation, texture, wear, repair, access, scale, and embodied or institutional constraint.

Record only features directly available in the supplied object. A screenshot does not establish hidden interaction states; a transcript does not preserve every sonic or embodied feature.

### 3. Segment the object

Choose meaningful units and explain why they are analytically relevant. Avoid cherry-picking a striking phrase while ignoring nearby qualification, irony, contradiction, or formal reversal.

### 4. Build inference chains

For each interpretation use:

```text
Observed feature
→ interpretive move
→ local claim
→ qualification
```

State the warrant connecting feature and claim. A metaphor does not automatically establish a social fact; an interface choice does not automatically reveal designer intention.

### 5. Test pattern and exception

Check repetition, contrast, sequence, and negative space. Identify whether the selected feature is typical, exceptional, transitional, or ambiguous within the supplied object.

### 6. Introduce theory only after description

Use theoretical concepts to sharpen a relation already visible in the object. Define the concept’s function. Do not merely rename an observation with prestigious vocabulary.

### 7. Generate a rival reading

Construct the strongest plausible alternative. Specify which features support it and which features weaken it. Do not create a trivial straw alternative.

### 8. Separate local from contextual claims

Label claims about historical reception, production conditions, authorship, audience, institutional context, or platform design as contextual and verify them separately. The object may prompt such claims but does not prove them alone.

### 9. Test scale

Ask what the object supports at the level of passage, work, corpus, period, medium, or culture. Block movement to a higher level when sampling or contextual evidence is missing.

### 10. Iterate between part and whole

Use a controlled hermeneutic loop. Reconsider local observations in relation to the developing account of the whole object, then return to the local unit to test whether the broader account has distorted, omitted, or over-weighted it. Record each material revision of the interpretation.

```text
local feature
→ provisional account of the whole
→ return to the feature
→ confirmed, qualified, or revised interpretation
```

Iteration MUST not become a license for unfalsifiable interpretation. Each return must identify what changed and which feature warrants the change.

### 11. Record negative findings

State when the object does not support the proposed claim. A negative close reading is valid and may require revising the argument map.

### 12. Issue the gate report

Return `PASS` when observations, inference chains, rival reading, and scale limits are explicit. Return `CONDITIONAL PASS` when contextual verification remains. Return `FAIL` when the object or provenance is inadequate.

## Stop signals

Stop when:
- a quotation may be inaccurate or translated from an unidentified edition;
- the image or interface is cropped in a way that removes necessary context;
- authorial intention is asserted without documentary evidence;
- formal observation is replaced by plot summary or theoretical labeling;
- one example is used to characterize an entire corpus;
- the researcher asks for “the real meaning” as a singular fact.

## Completion criteria

Complete only when:
- the object and its limits are identified;
- at least two concrete features are recorded;
- interpretation is linked through explicit warrants;
- at least one strong rival reading is addressed;
- contextual claims are separated and verification needs listed;
- the supported claim is scaled appropriately;
- unsupported claims are marked `not supported`;
- a gate report and handoff are present.

## Anti-fabrication rules

- Never reconstruct missing text, frames, interface states, or archival content as fact.
- Do not invent page numbers, editions, translations, captions, or metadata.
- Do not attribute intention without evidence.
- Do not treat theoretical fit as proof.
- Preserve ambiguity where features support multiple readings.
- Mark transcriptions and researcher descriptions according to provenance.

## Output format

```md
## Object record
Object:
Provenance:
Boundary:
Verification state:

## Observations
### O1
Feature:
Location:
Description:

## Interpretive inferences
### I1
Based on:
Interpretive move:
Warrant:
Local claim:
Qualification:

## Rival reading
Reading:
Supporting features:
Limiting features:

## Context to verify

## Claim test
Claim:
Result: supported | partially supported | not supported | unknown
Scale permitted:

## Gate report
Gate: Close-reading gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: planning-humanities-argument
```

## Good invocation

> Closely read the supplied passage from the identified edition. Separate observation from interpretation, test my claim about mediated distance, and include the strongest rival reading.

## Bad invocation

> Tell me what this novel really means. I do not have the passage, but make the interpretation sound theoretically sophisticated.

The bad invocation lacks the object and asks theoretical fluency to replace evidence.

## Next skills

- `planning-humanities-argument` to place the local finding in a dependency map.
- `structuring-humanities-argument` to integrate the reading into researcher-authored prose.
- `stress-testing-argument` to test scale, alternatives, and counterexamples.

## Limitations

Close reading does not by itself establish historical prevalence, social causation, reception, or authorial intention. Different disciplinary traditions also define legitimate objects and interpretive warrants differently; the skill must remain responsive to those traditions. The listed dimensions are prompts for attention, not a universal ontology of media. Interpretation may require repeated movement between part and whole, and that iterative movement must remain traceable to observable features.
