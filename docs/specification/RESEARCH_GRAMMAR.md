# Research Grammar

## 1. Purpose

Research grammar describes valid relationships among research objects. It is not a formula for interpretation. It prevents common category mistakes, such as treating a quotation as an argument or a citation as proof.

## 2. Core production rules

The following notation is conceptual:

```text
ResearchProblem ::= Observation + UnresolvedTension + Stakes
ResearchQuestion ::= Object + Problem + AnalyticalRelation + EvidencePath
Claim ::= Proposition + Scope + SupportStatus
SupportedClaim ::= Claim + EvidenceItem + Warrant
Interpretation ::= ObservedFeature + InterpretiveMove + ConceptualFrame + AlternativeReading
Argument ::= Thesis + SupportingClaims + Warrants + Objections + Replies + Limitations
VerifiedCitation ::= SourceExistenceCheck + LocatorCheck + ClaimSupportCheck
SubmissionReady ::= ArgumentGate(PASS) + CitationGate(PASS) + TerminologyGate(PASS) + MetadataGate(PASS)
```

## 3. Valid transitions

### 3.1 Topic to research question

A topic MAY generate several observations. It becomes a research question only after a tension and an evidentiary path are identified.

Invalid:

```text
platform aesthetics -> “How are platforms aesthetic?”
```

Valid:

```text
observed interface convergence
+ tension between apparent neutrality and perceptual governance
+ bounded corpus
-> contestable research question
```

### 3.2 Source to claim

A source does not automatically entail a claim.

```text
SourceRecord + located passage + interpretive reasoning -> possible support for Claim
```

A citation attached to a sentence without a claim-support explanation is incomplete.

### 3.3 Concept to analytical use

```text
ConceptRecord + defined boundary + operational role -> valid analytical use
```

Name-dropping a theorist does not create a concept record.

### 3.4 Close reading to interpretation

```text
textual/artifactual feature
+ location
+ pattern or anomaly
+ interpretive move
+ alternative reading
-> Interpretation
```

The grammar forbids moving directly from a detached quotation to a totalizing conclusion.

### 3.5 Objection to revision

```text
Objection + consequence assessment -> reply | limitation | claim revision | claim withdrawal
```

A response that merely repeats the original claim is not a valid reply.

## 4. Claim-support matrix

Every central claim SHOULD be paired with:

- at least one evidence type;
- an explicit warrant;
- a known limitation;
- a plausible objection;
- a verification state.

The matrix MAY show that a claim is currently unsupported. That is preferable to decorative citation.

## 5. Prohibited transformations

A conforming skill MUST NOT perform these transformations silently:

- `unknown -> verified`
- `researcher-supplied -> source-verified`
- `interpretation -> fact`
- `correlation -> causation`
- `single example -> general historical claim`
- `source mention -> source support`
- `terminological similarity -> conceptual identity`
- `reviewer request -> mandatory truth`
- `polished prose -> completed argument`

## 6. Argument topology

Arguments may be linear, cumulative, dialectical, genealogical, comparative, or constellational. The grammar does not require one topology. It requires that dependencies be visible.

A map MUST identify:

- which claim the thesis depends on;
- which evidence is necessary rather than illustrative;
- which objection is potentially fatal;
- which limitation narrows rather than destroys the argument.

## 7. Iteration

Research is recursive. A failed citation audit may return the workflow to literature dialogue; a concept-lineage conflict may require reformulating the question. Circular workflow is valid when the reason for return is recorded.
