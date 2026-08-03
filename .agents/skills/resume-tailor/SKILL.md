---
name: resume-tailor
description: Tailor an existing Word resume to a pasted job description by selecting role-specific, confirmed evidence from current complete project-story documents, preserving project diversity and the base resume's layout, saving the full JD as DOCX, and rendering and auditing the final DOCX. Use when asked to tailor, target, adapt, or create a resume version for a specific job, company, or role family such as product analytics, data science, AI, LLM, or RAG.
---

# Resume Tailor

Tailor evidence, not keywords. Treat complete project-story documents as the primary source of truth and the user-selected resume as the formatting template and source for stable resume facts.

## Required companion skill

Use the installed `documents` skill whenever reading, creating, editing, or rendering DOCX files. Read its task guidance for DOCX reading/editing and rendering. Preserve an existing resume with minimal, local formatting changes; do not apply a new design preset.

## Guardrails

- Never invent or upgrade tools, methods, ownership, scope, scale, causality, metrics, or results.
- Classify evidence as `Confirmed`, `Needs confirmation`, or `Unsupported`. Only confirmed evidence may enter the resume.
- Preserve confirmed metrics exactly. Generalize confidential or proprietary details when public use is uncertain, and flag the generalization.
- Never infer contribution or ownership from a screenshot alone.
- Do not create a detailed persistent evidence index. Use local retrieval to shortlist current source sections, then verify selected evidence directly against the original project stories for every tailoring task.
- Do not overwrite existing files. Do not rename, move, or reorganize workspace materials.
- Stop and ask when company, title, or base resume is ambiguous or missing, or when a material claim requires confirmation.

## Discover the workspace

Run `scripts/discover-materials.ps1` from the workspace root. Ignore temporary Office files and `__MACOSX` metadata. Treat discovered locations as authoritative rather than assuming fixed folder names.

If `resume-tailor.local.json` exists at the workspace root, read it as the user's private experience-selection policy. Support `minimum_experiences`, `required_experiences`, `optional_experiences`, and employer-specific `bullet_limits`. Never require this local configuration to be committed or copied into the skill. If it is absent, preserve all experiences and their approximate bullet counts unless the user approves a structural change.

Maintain `.agents/resume-tailor-project-catalog.json` as a lightweight router containing only project name, employer/experience, source path, broad themes, role families, and supporting-image types. Never copy actions, methods, metrics, or narratives into it. Run `scripts/refresh-project-catalog.py` at the start of every tailoring task so additions, moves, and renames are discovered automatically. Preserve curated themes when refreshing. If a newly discovered entry has blank employer, themes, or role families, read only its overview/high-level headings and populate those routing fields before retrieval.

## Execute the workflow

### 1. Capture the job description

Extract company and job title from the pasted JD. If either is ambiguous or absent, ask before saving.

Find an existing job-description folder case-insensitively. If none exists, propose `Job Descriptions/` and create it only after the naming decision is clear. Sanitize only filename-invalid characters (`< > : " / \\ | ? *` and trailing spaces/periods), preserving readable capitalization and spacing.

Save the complete, unabridged JD as `Company Name_Job Name.docx` with clean Word formatting; do not summarize or rewrite its content. If the path exists, compare normalized document text. Ask whether to replace it or save a versioned copy; never choose silently.

### 2. Analyze the JD

Produce a structured analysis of:

- primary role identity and expected seniority;
- responsibilities and likely screening priorities;
- technical, analytical, business, product, leadership, and stakeholder expectations;
- preferred qualifications and important ATS terminology.

Separate `Core requirements`, `Supporting requirements`, `ATS keywords`, `Preferred but nonessential`, and `No confirmed evidence`. Weight responsibilities and role context more heavily than keyword repetition.

### 3. Read the selected base resume

Require the user to identify one base resume. Record its page size/count, margins, fonts, sizes, colors, section order/headings, employer and position order, dates, locations, indentation, bullet style/count, spacing, alignment, header, and contact layout.

Preserve all recorded properties. Do not add/remove/move sections or redesign without explaining the proposed change and receiving approval, except as authorized by `resume-tailor.local.json`. Keep the approximate bullet count and content density for each retained position unless the local policy or approved tailoring strategy specifies a range or explains a change.

Apply these experience-selection rules:

- Retain every experience named in `required_experiences` when a local policy exists.
- Retain at least `minimum_experiences` entries when configured; otherwise preserve every base-resume experience unless the user approves removal.
- Follow configured `bullet_limits`. Choose within a permitted range using JD relevance, confirmed evidence, project diversity, and page fit. Never add filler to reach a maximum.
- Evaluate and tailor bullets across every retained experience; do not limit tailoring to the most recent employer when older experience provides stronger JD evidence.
- Use judgment to remove an experience named in `optional_experiences` when it is materially less relevant. Explain the decision in the proposed strategy.
- Preserve employer order, dates, locations, titles, and formatting for every retained experience.
- Do not remove an experience merely to create room unless all configured constraints remain satisfied and the proposed strategy explains the tradeoff.

### 4. Build a temporary evidence map

Read `references/retrieval-workflow.md` and use its staged retrieval process:

1. Route broadly with the lightweight catalog.
2. Run `scripts/retrieve-project-evidence.py` against the complete saved JD to rank heading-based sections locally.
3. Use the hash-invalidated cache only as disposable acceleration data. Never treat cached text or rankings as evidence.
4. Re-open each shortlisted section directly from its original DOCX with `--verify-path` and `--section-index` before classifying a claim as confirmed.
5. When evidence spans ownership, method, and result sections, add `--context-sections 1` or increase it selectively. Combine sections only when they clearly describe the same project scope and remain mutually consistent.
6. Read additional projects when ownership, context, methods, or results remain unclear.

Search across multiple projects before choosing evidence, but do not load every complete document into context by default. Use selective image inspection only when the document refers to an image, evidence may be missing, a UI clarifies the work, a chart may verify a result, or verification is needed.

Build an ephemeral map with: JD requirement; best supporting project; specific component; confirmed evidence; source section; status; strength; recommended angle; clarification needed. Do not save detailed evidence as a reusable index.

Use role-specific emphasis:

- Product Analytics: lifecycle, adoption, funnel behavior, experimentation, KPIs, rollout, decisions.
- Data Science: problem formulation, preparation, feature engineering, statistics/ML, evaluation, explainability, deployment, impact.
- AI/LLM: LLM/RAG architecture, retrieval, evaluation, experiments, workflow integration, responsible AI, adoption.

### 5. Design the bullet portfolio

Default each bullet to one distinct project or substantial business problem. Do not combine unrelated projects, split one project into cosmetic variants, or let one project provide a majority under an experience without explicit approval.

Create a proposed portfolio organized by retained experience, with bullet position, represented project/problem, primary competency, JD relevance, and whether it keeps, replaces, or reframes an existing bullet. Review and tailor all retained experiences. Place the strongest relevant evidence early within each experience while preserving breadth across problems, methods, stakeholders, and outcomes. When a configured bullet range permits multiple counts, justify the selected count using relevance, evidence strength, diversity, and page fit. Surface any relevance-versus-diversity tradeoff and explain any decision to remove an optional experience.

### 6. Obtain content approval

Before generating the final resume, show:

1. concise JD summary;
2. most important competencies;
3. temporary JD-to-project evidence map;
4. proposed bullet portfolio;
5. bullets to keep, replace, remove, or substantially reframe;
6. evidence gaps and factual questions;
7. draft revised bullets.

Wait only when a material claim, sensitive detail, filename conflict, or structural change requires confirmation.

### 7. Write from confirmed evidence

Draft with a flexible pattern: `Action + problem/scope + method + decision/implementation + outcome`. Prefer substantive evidence and emphasis changes over keyword swaps. Use accurate JD terminology naturally, past tense for completed work, a credible professional voice, and lengths that fit the base layout. Represent the documented level of ownership precisely and do not turn association into causality.

### 8. Audit and deliver

Trace every substantive claim to a current project story, selectively verified image, or confirmed resume fact. Audit requirement coverage, early-bullet strength, project diversity, competency range, technical depth, natural ATS alignment, dates/titles/tools/metrics, confidentiality, and meaningful differentiation from other role-family versions.

Save to the existing appropriate output folder. If no convention exists, use `Company Name_Job Name_Resume.docx`. Preserve the base resume's visual structure, page count, and density.

Render the base and tailored DOCX with the `documents` skill's `render_docx.py`; inspect every page PNG at 100%. Compare page count, margins, fonts/sizes, sections, indentation, spacing, alignment, wrapping, and page breaks. Iterate and re-render after changes. If LibreOffice is unavailable, perform structural OOXML checks and disclose that visual QA could not be completed.

Return a concise coverage report with strongly supported, partially supported, and unsupported requirements; project diversity by final bullet; important changes; and claims needing confirmation.

## Failure conditions

Do not finalize when the base resume is unspecified, required naming is ambiguous, a required experience is absent, an experience violates configured bullet limits, fewer than the configured minimum experiences remain, unresolved material claims remain in draft bullets, a project unintentionally dominates, an existing file would be overwritten, or the latest DOCX has not passed the render gate (except the documented LibreOffice fallback).
