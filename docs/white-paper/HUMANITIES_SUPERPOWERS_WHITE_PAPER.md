# Humanities Superpowers

## A Structured Workflow for AI-Assisted Humanities Research

**Lee Yong Wook**  
Jeonju University  
Version 1.0.0 · July 2026

---

## Abstract

Generative AI can produce polished academic prose faster than most research workflows can verify it. This asymmetry creates a distinctive risk for humanities scholarship: fluent output may conceal weak questions, unstable concepts, unexamined assumptions, fabricated or misapplied citations, shallow close reading, and premature claims of completion. Existing AI-writing tools usually optimize generation. Humanities Superpowers instead organizes scholarly work around explicit research skills and quality gates.

The framework treats AI as a **scholarly judgment scaffold**, not as an autonomous author. It provides 13 core research skills plus 1 Level 3 router. The core skills cover research-question formation, argument scoping, concept-lineage mapping, literature dialogue, argument planning, close reading, argument structuring, stress testing, citation auditing, terminology control, manuscript reviewing, peer-review response, and final submission verification. Each skill defines invocation conditions, required inputs, procedures, stop signals, anti-fabrication rules, completion criteria, and structured outputs. The router coordinates their use without becoming a fourteenth research method.

The framework rests on five principles: research precedes prose; uncertainty must remain visible; claims must be proportionate to evidence; concepts require lineage and boundary control; and completion must be demonstrated rather than asserted. These principles are implemented as quality gates that can return `PASS`, `CONDITIONAL PASS`, or `FAIL`. A failed gate is not a system error. It is a refusal to convert unresolved scholarly risk into confident language.

Humanities Superpowers does not guarantee truth, originality, publication, or citation accuracy. It aims to reduce avoidable failure by making scholarly judgment traceable, reviewable, and difficult to bypass. The project is inspired by Jesse Vincent's `obra/superpowers`, which applies composable skills and systematic verification to coding agents, but it independently adapts that general design idea to humanities research.

---

## 1. The problem is not text generation

The rapid adoption of large language models has encouraged a misleading description of scholarly work: research is often treated as a sequence that ends in writing, and writing is treated as the dominant bottleneck. From this perspective, a system that produces clear paragraphs, summaries, outlines, and references appears to solve much of the problem.

Humanities research resists that reduction. Its difficult moments occur before, within, and after prose:

- deciding whether a topic contains a genuine research problem;
- distinguishing a broad interest from a contestable question;
- defining the limits of a claim;
- tracing how a concept changes across authors, languages, periods, and media;
- deciding whether a passage supports a claim or merely resembles it;
- separating evidence, interpretation, inference, hypothesis, and speculation;
- identifying the strongest rival explanation;
- verifying whether a citation exists and whether it actually supports the sentence attached to it;
- preserving terminological consistency across a long manuscript;
- deciding whether unresolved problems require revision or prohibit submission.

These are acts of judgment. They are not reducible to stylistic fluency.

Large language models are useful precisely because they can generate candidate formulations, expose structural alternatives, compress information, compare passages, and simulate objections. But the same fluency creates a masking effect. A weak argument can sound complete. An uncertain attribution can look bibliographically plausible. A concept can drift while retaining rhetorical coherence. A summary can replace a scholarly conversation without appearing obviously deficient.

Research on fabricated citations demonstrates why generation cannot be equated with verification. Empirical studies have documented nonexistent references, corrupted bibliographic details, and authentic sources inaccurately matched to claims. The rates vary by model, discipline, and prompting conditions, but the methodological lesson is stable: a citation-shaped string is not a verified citation, and confident prose is not evidence of scholarly completion.

Humanities Superpowers begins from this mismatch:

> **AI accelerates textual production faster than scholarship can safely validate it.**

The appropriate response is not to prohibit AI or to assume that better prompting alone will solve the problem. The response is to design research workflows in which validation is explicit, records are inspectable, and unresolved uncertainty cannot be silently converted into completion.

---

## 2. From writing assistant to scholarly judgment scaffold

A writing assistant primarily asks: *What text should be produced next?*

A scholarly judgment scaffold asks different questions:

- What must be decided before text is produced?
- What evidence is available?
- Which parts are interpretation rather than established fact?
- What would make the current claim fail?
- Which tasks require the researcher's direct judgment?
- What remains unknown?
- What must be verified before proceeding?

The word **scaffold** is deliberate. A scaffold supports work without becoming the work itself. It provides sequence, stability, and access. It can make difficult operations visible and repeatable. It does not replace the researcher who determines the significance of a text, the legitimacy of an inference, the ethical boundaries of interpretation, or the contribution of an argument.

Humanities Superpowers therefore rejects two symmetrical errors.

The first is **automation triumphalism**: the assumption that an AI system can independently conduct humanities research because it can produce recognizable academic forms.

The second is **methodological abstention**: the assumption that because AI cannot replace scholarly judgment, it has no legitimate role in research practice.

Between these positions lies a more useful design problem: how can an AI agent be constrained to support inquiry without laundering uncertainty into authority?

The framework answers by treating research as a sequence of composable skills governed by quality gates.

---

## 3. Design inheritance and methodological independence

Humanities Superpowers was inspired by Jesse Vincent's `obra/superpowers`, a public project that describes itself as a composable-skills methodology for coding agents. Its central commitments include systematic rather than ad hoc work, evidence over claims, planning before implementation, debugging discipline, and verification before completion.

The present project adopts the **general architectural insight** that agent behavior improves when complex work is decomposed into reusable procedural skills with explicit invocation rules and completion tests.

It does not transplant software-development procedures into humanities research. The domains differ in decisive ways.

Software development often has executable tests, reproducible failures, formal interfaces, and observable program behavior. Humanities arguments rarely have binary truth tests. They depend on textual interpretation, historical context, conceptual precision, comparative judgment, evidentiary adequacy, and disciplinary standards that are contestable rather than mechanically decidable.

Accordingly, the framework replaces coding-oriented tests with scholarly quality gates:

| Software-development concern | Humanities-research analogue |
|---|---|
| specification | research question and scope boundary |
| test case | counterexample, rival interpretation, source check |
| debugging | diagnosing conceptual drift or inferential failure |
| code review | manuscript review and objection simulation |
| dependency tracking | claim–reason–evidence mapping |
| regression test | terminology and citation re-audit after revision |
| release gate | submission-readiness verification |

This analogy is useful only when its limits remain visible. A humanities quality gate does not prove that an interpretation is true. It establishes that specified risks have been checked, unresolved issues are recorded, and claims are proportionate to available evidence.

---

## 4. Core principles

### 4.1 Research before prose

The framework does not treat a polished paragraph as the default output of every task. Many skills produce records instead:

- research-question matrices;
- scope boundaries;
- concept-lineage tables;
- literature-position maps;
- claim–reason–evidence diagrams;
- close-reading notes;
- objection ledgers;
- citation audits;
- terminology ledgers;
- revision matrices;
- submission-gate reports.

Prose becomes legitimate after the argument has enough structure to justify it.

### 4.2 Unknown is better than fabricated

An agent must be allowed—and sometimes required—to return:

- `UNKNOWN`;
- `UNVERIFIED`;
- `SOURCE REQUIRED`;
- `PAGE NUMBER REQUIRED`;
- `CLAIM EXCEEDS EVIDENCE`;
- `RESEARCHER DECISION REQUIRED`.

These labels are not signs of poor performance. They preserve the epistemic state of the research.

### 4.3 Evidence over confidence

The framework distinguishes at least five statuses:

1. **Verified evidence** — directly checked against a reliable source.
2. **Interpretation** — a reasoned account of evidence.
3. **Inference** — a conclusion drawn from one or more premises.
4. **Hypothesis** — a proposition requiring further investigation.
5. **Unknown** — information not presently established.

A strong output does not erase these distinctions.

### 4.4 Bounded claims over inflated novelty

AI systems often reward assertive novelty language: “first,” “unprecedented,” “completely overlooked,” “fundamentally transforms.” Humanities Superpowers requires novelty claims to be bounded by the search actually performed.

Acceptable:

> Within the reviewed scholarship on platform aesthetics, this study identifies an underdeveloped relation between interface design and the temporal organization of attention.

Unacceptable without exhaustive evidence:

> No previous scholar has examined this issue.

### 4.5 Completion must be demonstrated

The statement “the paper is complete” is itself a claim. The framework requires evidence for that claim: completed audits, resolved stop signals, documented exceptions, and a final gate report.

---

## 5. The 13 core research skills

### 5.1 Formulating a research question

A topic is not yet a research question. “AI and literature,” “platform aesthetics,” or “memory in modern fiction” identify fields of interest. A research question must specify a tension, object, relation, and stakes.

The skill asks:

- What is puzzling, contradictory, absent, or insufficiently explained?
- What material will be analyzed?
- Which relation is contestable?
- What answer would change an existing interpretation?
- Can the question be answered within the available evidence and format?

The skill stops when the question is merely thematic, contains its conclusion, presupposes an unverified fact, or requires evidence beyond the project’s reach.

### 5.2 Scoping the argument boundary

Scope is not an apology for what the paper cannot do. It is a methodological declaration of what the argument is entitled to claim.

The skill records:

- object of analysis;
- time period;
- language and corpus limits;
- theoretical frame;
- excluded questions;
- level of generalization;
- transfer conditions.

A scope boundary prevents local observations from becoming universal claims.

### 5.3 Mapping concept lineage

Concepts are historical and relational. The same term may change across authors, translations, institutions, and media environments. A lineage map therefore distinguishes:

- first verified occurrence relevant to the project;
- changes in definition;
- inherited assumptions;
- contested translations;
- conceptual neighbors;
- points where the present study departs from prior usage.

The goal is not to produce a decorative list of theorists. It is to show which conceptual operations are inherited, modified, rejected, or newly proposed.

### 5.4 Conducting literature dialogue

A literature review is not a sequence of summaries. It is a structured account of positions, agreements, disagreements, methods, objects, and unresolved problems.

The skill organizes sources by function:

- foundational definition;
- dominant interpretation;
- revisionist account;
- methodological model;
- counterposition;
- empirical or archival support;
- gap relevant to the current study.

The output must explain why each source matters to the argument, not merely what it says.

### 5.5 Planning the humanities argument

The argument plan decomposes a thesis into:

- principal claim;
- subsidiary claims;
- reasons;
- evidence required;
- warrants connecting evidence to claim;
- objections;
- dependencies;
- points of interpretive risk.

This skill prevents section headings from substituting for argument structure.

### 5.6 Performing close reading

Close reading is neither quotation accumulation nor paraphrase. It attends to form, diction, syntax, image, rhythm, framing, omission, sequence, material presentation, and historical context.

The skill requires the agent to distinguish:

- what is directly observable in the passage or artifact;
- what interpretive claim is made;
- what contextual evidence supports the interpretation;
- what alternative reading remains possible.

For images and media artifacts, the same logic applies to composition, interface, temporality, affordance, and mode of address.

### 5.7 Structuring the researcher’s argument

This skill does not authorize ghostwriting from an empty prompt. It reorganizes researcher-supplied claims, notes, evidence, and draft material into a coherent argumentative sequence.

It may:

- identify missing transitions;
- reorder claims;
- separate background from intervention;
- mark unsupported assertions;
- propose paragraph functions;
- identify repetition;
- preserve the researcher’s conceptual vocabulary.

It must not create sources, evidence, or a scholarly position the researcher has not authorized.

### 5.8 Stress-testing the argument

An argument should encounter its strongest challenge before peer review.

The skill tests:

- counterexamples;
- rival causal or interpretive explanations;
- category mistakes;
- circularity;
- overgeneralization;
- equivocation;
- unacknowledged normative assumptions;
- dependence on a single fragile source;
- cases where the thesis becomes unfalsifiable.

A strong stress test aims to improve the argument, not merely attack it.

### 5.9 Auditing citations

Citation auditing contains two distinct questions:

1. Does the source exist with the stated bibliographic details?
2. Does the source support the claim for which it is cited?

The second question is frequently neglected. A real article can still be misrepresented.

The audit records:

- source status;
- author and title verification;
- publication venue and date;
- DOI, ISBN, stable URL, or catalog record where relevant;
- page or location verification;
- quotation accuracy;
- claim–source fit;
- primary versus secondary citation status.

An unverified citation remains unverified even if it looks plausible.

### 5.10 Checking terminology consistency

Humanities manuscripts often use stylistic variation where conceptual stability is required. Near-synonyms may conceal real differences; translations may shift; abbreviations may change meaning.

The terminology ledger records:

- preferred term;
- definition;
- excluded meanings;
- translation;
- first use;
- abbreviations;
- related but non-equivalent terms;
- permitted variation;
- revision decisions.

### 5.11 Reviewing the manuscript

This skill simulates a demanding but constructive reviewer. It evaluates:

- significance of the research problem;
- originality proportional to evidence;
- engagement with scholarship;
- conceptual consistency;
- adequacy of textual analysis;
- argument structure;
- counterargument handling;
- citation integrity;
- fit between title, abstract, introduction, body, and conclusion.

The review must rank problems by severity and identify what evidence would resolve them.

### 5.12 Responding to peer review

Peer-review response is treated as a traceable revision process. Each reviewer comment receives:

- classification;
- interpretation of the underlying concern;
- action taken;
- manuscript location;
- justification when not adopted;
- residual risk.

The skill discourages defensive rhetoric and cosmetic revision.

### 5.13 Verifying before submission

The final skill produces a gate report rather than a celebratory summary. It checks:

- question and scope;
- argument and evidence;
- terminology;
- citations;
- quotations and page numbers;
- counterarguments;
- abstract and title alignment;
- author information;
- acknowledgments and disclosure;
- privacy and confidential data;
- journal or venue requirements;
- unresolved placeholders.

The result is one of:

- `PASS` — no known blocking issue remains;
- `CONDITIONAL PASS` — non-blocking issues are documented and accepted by the researcher;
- `FAIL` — one or more blocking issues remain.

---

## 6. Quality gates as epistemic friction

Many AI interfaces are designed to minimize friction. The user asks; the system responds. In routine tasks this can be useful. In research, friction can be epistemically productive.

Humanities Superpowers introduces **deliberate friction** at points where error is costly:

- before a topic is accepted as a question;
- before a concept is treated as original;
- before a source summary becomes a literature claim;
- before an interpretation becomes a generalized thesis;
- before a citation is accepted;
- before a manuscript is declared complete.

This friction is not bureaucratic delay for its own sake. It is a structured pause that demands evidence, boundaries, or researcher judgment.

A gate should satisfy four conditions:

1. **Specificity** — it identifies what is being checked.
2. **Traceability** — it records the basis of the decision.
3. **Non-circumvention** — it cannot be passed by fluent restatement alone.
4. **Actionability** — failure indicates what must happen next.

### 6.1 Why gates can fail

A framework that always passes is not a validation framework. It is a formatting tool.

The worked example in this repository intentionally fails the final gate because no verified source set is supplied. The failure demonstrates the governing principle:

> **Absence of verification must remain visible, even when the argument is promising.**

### 6.2 Gate outputs

Each gate should produce a small record:

```text
Gate: Citation audit
Status: FAIL
Blocking issue: Three central claims cite sources not checked against the original publications.
Evidence: Citation ledger rows C04, C07, C11.
Required action: Verify source existence, bibliographic details, and claim–source fit.
Researcher decision required: No
Next skill: auditing-citations
```

This format makes failure useful.

---

## 7. Human and AI responsibilities

The framework does not assign all difficult thinking to the human and all mechanical labor to the AI. The division is more precise.

### 7.1 Appropriate AI responsibilities

AI can assist with:

- generating alternative formulations of a research question;
- comparing scope options;
- organizing researcher-provided sources into positions;
- extracting candidate concepts from verified texts;
- identifying missing warrants;
- proposing objections;
- detecting inconsistent terminology;
- checking internal document consistency;
- producing audit tables;
- tracking reviewer comments and revisions;
- flagging unresolved placeholders.

### 7.2 Non-delegable researcher responsibilities

The researcher remains responsible for:

- selecting the research problem;
- determining interpretive significance;
- verifying sources against originals;
- approving conceptual definitions;
- judging whether evidence is adequate;
- making ethical decisions;
- deciding how to represent persons, communities, and contested histories;
- accepting or rejecting theoretical commitments;
- authorizing the final manuscript;
- disclosing AI use according to relevant policies.

### 7.3 Shared responsibilities

Some tasks are collaborative:

- argument revision;
- counterargument exploration;
- terminology refinement;
- literature clustering;
- manuscript restructuring;
- response-to-review drafting.

In these cases, the system should show its transformations and preserve the researcher’s ability to reverse them.

---

## 8. Anti-patterns

### 8.1 Prompt-to-paper

**Pattern:** A broad topic is entered, a complete paper is generated, and references are added afterward.

**Failure:** The appearance of structure precedes the research decisions that should justify it.

**Correction:** Begin with question formation, scope, and verified sources.

### 8.2 Citation decoration

**Pattern:** Citations are used to make prose look scholarly.

**Failure:** Source existence and claim–source fit are not checked.

**Correction:** Run citation audit before accepting the paragraph.

### 8.3 Theory-name accumulation

**Pattern:** Multiple theorists are mentioned without explaining conceptual inheritance or disagreement.

**Failure:** Name density substitutes for theoretical work.

**Correction:** Build a concept-lineage map.

### 8.4 Summary-list literature review

**Pattern:** “Scholar A argues…, Scholar B argues…, Scholar C argues…”

**Failure:** No relation among positions is established.

**Correction:** Organize sources by claims, methods, objects, and conflicts.

### 8.5 Stylistic synonym drift

**Pattern:** A key concept is replaced by near-synonyms to avoid repetition.

**Failure:** Conceptual meaning becomes unstable.

**Correction:** Use a terminology ledger.

### 8.6 Reviewer theater

**Pattern:** An AI simulates reviewers only to praise the paper or produce generic concerns.

**Failure:** The review performs rigor without testing the argument.

**Correction:** Require severity ranking, evidence, and actionable objections.

### 8.7 Completion by tone

**Pattern:** The agent says “the manuscript is now polished and publication-ready.”

**Failure:** Readiness is asserted rather than demonstrated.

**Correction:** Run the final submission gate.

---

## 9. Implementation architecture

The repository uses a simple, inspectable architecture:

```text
skills/       reusable methods
workflows/    ordered combinations of skills
templates/    structured research records
examples/     worked demonstrations
tests/        invocation and routing cases
scripts/      repository validation
assets/       diagrams
```

Each `SKILL.md` contains front matter and fixed sections. The stable schema supports both human reading and agent routing.

The substantive skills are intentionally limited. The project does not aim to encode every humanities method. It provides a small core that can be extended through discipline-specific contributions.

### 9.1 Skill schema

Every skill includes:

- Purpose
- When to use
- Inputs required
- Procedure
- Stop signals
- Completion criteria
- Anti-fabrication rules
- Output format
- Good invocation
- Bad invocation
- Next skills
- Limitations

### 9.2 Routing

The `using-humanities-superpowers` skill selects methods according to the task’s current state. It should not force every project through every skill. A reviewer-response task may begin near the end of the workflow. A close-reading exercise may require only three or four skills.

### 9.3 Validation

The repository validator checks:

- skill names and metadata;
- required sections;
- link integrity;
- plugin manifests;
- expected examples;
- intentional failure behavior;
- release placeholders.

Repository validation cannot establish scholarly truth. It verifies that the framework itself is structurally intact.

---


## 10. Why humanities research needs domain-specific safeguards

General-purpose research assistance often assumes that accuracy can be improved primarily by retrieving more information. Retrieval is important, but humanities scholarship presents additional problems that cannot be solved by source access alone.

### 10.1 Interpretation is not extraction

A passage does not contain one detachable meaning waiting to be retrieved. Meaning emerges through relations among wording, form, genre, historical situation, textual transmission, audience, and the questions brought to the object. An AI system may identify themes or paraphrase a passage, yet still miss the interpretive operation that makes the passage significant.

For this reason, the close-reading skill does not ask only what a text says. It requires a record of observable features, interpretive claims, contextual support, and plausible alternatives. This structure prevents interpretation from being presented as if it were a directly extracted fact.

### 10.2 Concepts travel unevenly

Humanities concepts move across languages and disciplines. A translated term may acquire associations absent from the source language. A concept borrowed from philosophy may function differently in literary criticism, media studies, history, or cultural policy. Later scholars may preserve the term while altering its object or explanatory role.

A model trained on large textual corpora can reproduce these usages without distinguishing them. Concept-lineage mapping and terminology control are therefore not optional refinements. They are safeguards against silent theoretical substitution.

### 10.3 Archives are incomplete and situated

Historical and archival scholarship routinely works with absence, damaged records, selective preservation, institutional cataloguing, and unequal visibility. A system that treats searchable availability as equivalent to historical existence may reproduce archival bias. Conversely, it may fill documentary gaps with plausible narrative continuity.

The framework requires absence to be represented as absence. Missing evidence can motivate a research question, but it cannot be converted into a positive historical claim without justification.

### 10.4 Normative judgment cannot be hidden inside summary

Humanities research often addresses contested identities, violence, colonialism, gender, religion, memory, and political representation. Describing a scholarly debate can involve normative choices about terminology, voice, and whose testimony is treated as authoritative. AI-generated neutrality may conceal rather than resolve these choices.

Humanities Superpowers therefore marks ethical and representational decisions as researcher responsibilities. The system can identify where a decision occurs and present alternatives, but it must not disguise the decision as an automatic summary result.

### 10.5 Disagreement is not noise

In many technical tasks, disagreement can indicate error or insufficient data. In humanities scholarship, sustained disagreement may be constitutive of the field. Competing readings can remain rationally defensible because they prioritize different evidence, concepts, or values.

The purpose of stress testing is not to eliminate disagreement and produce one final answer. It is to clarify what the thesis explains, what it leaves unresolved, and what commitments distinguish it from rival accounts.

### 10.6 Style can carry argument

In literature, philosophy, rhetoric, and media studies, form is not merely packaging. Syntax, metaphor, sequence, voice, and genre can perform conceptual work. An AI system that “improves clarity” may erase ambiguity, rhythm, or rhetorical tension essential to the argument or object of analysis.

The structuring skill therefore separates organizational revision from stylistic homogenization. It should identify the function of a passage before altering its form, and it should preserve deliberate difficulty unless the researcher decides otherwise.

### 10.7 Citation practices vary by object

Humanities researchers cite monographs, edited volumes, archival folders, manuscripts, artworks, performances, films, websites, interviews, translations, and editions. Verification cannot be reduced to DOI lookup. Edition, translator, archive collection, folio, timestamp, or exhibition context may be decisive.

The citation audit is designed as an extensible record rather than a single database check. Discipline-specific variants can add the metadata needed for their objects while preserving the two central questions: does the source exist as described, and does it support the claim?

### 10.8 The contribution may be conceptual rather than predictive

Many evaluation systems reward predictive accuracy, benchmark performance, or measurable causal explanation. Humanities contributions may instead redescribe an object, reveal a hidden assumption, connect previously separated traditions, offer a more precise concept, or reinterpret a canonical text.

Such contributions still require evidence and argument. But they should not be judged by a false model of experimental verification. Humanities Superpowers uses procedural accountability precisely because it can support rigorous reasoning without pretending that every interpretive claim has a mechanical test.

---

## 11. Governance, disclosure, and research records

Responsible use requires more than good prompts. It requires a record of how AI participated in the research process.

A minimal research log should record:

- the agent or model used;
- the date of significant interactions;
- the skills or workflows invoked;
- source materials supplied to the system;
- substantive transformations proposed by the system;
- decisions accepted, rejected, or revised by the researcher;
- citations or facts independently verified;
- unresolved limitations;
- disclosure requirements of the intended venue.

This record serves several purposes. It supports reproducibility, helps the researcher identify where conceptual drift entered the manuscript, enables co-authors to inspect AI-assisted changes, and provides a basis for accurate disclosure.

The framework does not prescribe one universal disclosure statement. Journal and institutional policies differ and continue to change. It does prescribe a principle:

> **Disclosure should describe material research assistance, not merely name a tool.**

A useful disclosure distinguishes language editing from literature organization, argument mapping, coding, translation, image analysis, or reviewer-response assistance. It should also state that the author verified sources and accepts responsibility for the final work.

Research logs should not contain confidential manuscripts, protected personal information, embargoed archival material, or data that the researcher is not authorized to share with an external system. Privacy and access conditions must be checked before materials are supplied to an agent.

---
## 12. Evaluation framework

A research-methodology repository should be evaluated on more than adoption or user satisfaction. Humanities Superpowers proposes five evaluation dimensions.

### 10.1 Procedural fidelity

Did the agent invoke the correct skill at the correct stage? Did it stop when required inputs were missing?

### 10.2 Epistemic transparency

Did the output distinguish evidence, interpretation, inference, hypothesis, and unknowns?

### 10.3 Fabrication resistance

Did the system avoid inventing sources, quotations, page numbers, archival details, or novelty claims?

### 10.4 Argumentative value

Did the workflow reveal missing warrants, counterexamples, rival explanations, or scope problems that would otherwise remain hidden?

### 10.5 Researcher agency

Did the system preserve meaningful decisions for the researcher and make transformations reversible and inspectable?

Future empirical evaluation can compare unstructured AI assistance with the framework on tasks such as question quality, citation validity, terminology stability, objection coverage, and reviewer-rated argument coherence.

---

## 13. Limitations

Humanities Superpowers has important limitations.

First, procedural compliance does not guarantee good scholarship. A researcher can complete every template and still produce a weak interpretation.

Second, quality gates rely on the availability and quality of evidence. A citation audit cannot verify a source that the system cannot access, and it must not pretend otherwise.

Third, disciplinary variation matters. Methods appropriate to literary studies may not transfer directly to history, philosophy, art history, religious studies, cultural studies, or linguistics without adaptation.

Fourth, the framework can create excessive proceduralism. Researchers should use the smallest set of skills adequate to the task.

Fifth, AI systems may follow the visible form of a skill while violating its purpose. Validation therefore requires inspection of outputs, not only confirmation that sections exist.

Sixth, the framework cannot settle contested interpretations. It can make assumptions and evidence visible, but scholarly disagreement remains irreducible.

Seventh, the project does not provide legal, ethical, or institutional authorization for AI use. Researchers must follow journal, university, funder, archive, and privacy requirements.

---

## 14. Research and development agenda

The project’s next stages include:

1. deeper discipline-specific skill variants;
2. a benchmark set for invocation and stop-signal behavior;
3. paired examples showing unstructured versus scaffolded AI assistance;
4. citation-verification integrations that preserve source provenance;
5. multilingual terminology ledgers;
6. transparent research logs for agent-assisted workflows;
7. community review by humanities scholars from different fields;
8. formal study of whether quality gates improve manuscript review outcomes.

The long-term objective is not to automate humanities research. It is to make AI-assisted research more accountable to the practices that give scholarship its authority.

---

## 15. Conclusion

Generative AI changes the speed and surface form of academic work, but it does not remove the need for scholarly judgment. It increases that need.

Humanities Superpowers responds by shifting the center of AI-assisted research from prose generation to procedural accountability. Its skills do not ask only what the agent can produce. They ask what must be known, checked, bounded, interpreted, challenged, and recorded before a claim deserves acceptance.

The framework’s most important output may therefore be neither a paragraph nor a paper. It may be a justified refusal:

- the question is not yet researchable;
- the concept is not yet stable;
- the evidence does not support the claim;
- the citation is not verified;
- the manuscript is not ready.

Such refusals are not obstacles to scholarship. They are part of scholarship.

> **Support scholarly judgment. Never replace it.**

---

## References

A source-by-source verification record is available in [`citation-audit.md`](citation-audit.md).


Asai, Akari, et al. “Synthesizing Scientific Literature with Retrieval-Augmented Language Models.” *Nature* (2026). https://doi.org/10.1038/s41586-025-10072-4

Jiang, Che, et al. “On Large Language Models’ Hallucination with Regard to Known Facts.” *Proceedings of NAACL 2024* (2024). https://aclanthology.org/2024.naacl-long.60/

Li, Junyi, et al. “The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models.” *Proceedings of ACL 2024* (2024). https://aclanthology.org/2024.acl-long.586/

UNESCO. *Guidance for Generative AI in Education and Research*. Paris: UNESCO, 2023. https://unesdoc.unesco.org/ark:/48223/pf0000386693

Walters, William H., and Esther Isabelle Wilder. “Fabrication and Errors in the Bibliographic Citations Generated by ChatGPT.” *Scientific Reports* 13 (2023). https://doi.org/10.1038/s41598-023-41032-5

Vincent, Jesse. *Superpowers: An Agentic Skills Framework & Software Development Methodology*. GitHub repository. https://github.com/obra/superpowers

---

## Suggested citation

Lee, Yong Wook. *Humanities Superpowers: A Structured Workflow for AI-Assisted Humanities Research*. Version 1.0.0. Jeonju University, 2026.

Methodological restraint is therefore not a limitation of the framework; it is its central scholarly commitment.
