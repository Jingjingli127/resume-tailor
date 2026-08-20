---
name: resume-tailor
description: Tailor an existing Word resume to a pasted job description by selecting role-specific, confirmed evidence from current complete project-story documents, preserving project diversity and the base resume's layout, saving the full JD as DOCX, and rendering and auditing the final DOCX. Use when asked to tailor, target, adapt, or create a resume version for a specific job, company, or role family such as product analytics, data science, AI, LLM, or RAG.
---

# Resume Tailor

Tailor evidence, not keywords. Treat complete project-story documents as the primary source of truth and the user-selected resume as the formatting template and source for stable resume facts.

## DOCX support

Use the installed `documents` skill when available for DOCX reading and editing guidance. Preserve an existing resume with minimal, local formatting changes; do not apply a new design preset.

For visual QA, export with `scripts/export-word-pdf.ps1` on Windows or LibreOffice elsewhere, then render page PNGs with `scripts/render-pdf-pages.py`. Use the repository requirements and do not require an additional PDF stack merely for redundancy.

## Guardrails

- Never invent or upgrade tools, methods, ownership, scope, scale, causality, metrics, or results. Only directly verified or user-confirmed claims may enter the final resume; retrieval results and reasonable inferences remain candidates until verified or explicitly confirmed.
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

Keep requirement boundaries intact for retrieval. Do not collapse the JD into a single keyword query.

Define the role-specific value proposition that the resume should communicate. Identify the target professional identity, two or three most important strengths, the value those strengths enable, and one credible differentiator when available. Use this value proposition to guide the summary and early-bullet emphasis; do not substitute branding language for evidence.

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

Read and follow `references/retrieval-workflow.md`. Route with the catalog, retrieve requirement-level candidates, and verify every selected claim directly against original project-story sections. Treat cache content, rankings, and classifications as advisory only. Never present transferable evidence as the missing domain or method. Search selectively across projects and inspect images only when they can resolve a material evidence question.

Build an ephemeral map with: JD requirement; best supporting project; specific component; confirmed evidence; source section; status; strength; recommended angle; clarification needed. Do not save detailed evidence as a reusable index.

When an accomplishment lacks sufficient context or impact, diagnose the Situation or objective, Obstacle or analytical problem, Action and method, and Result before drafting. Prefer a confirmed quantitative result, then a confirmed operational or decision outcome, then defensible qualitative stakeholder value. Ask the smallest targeted question needed to resolve a material gap. Avoid generic endings such as `supported data-informed decisions` when the evidence can identify what changed for the stakeholder.

Use role-specific emphasis:

- Product Analytics: lifecycle, adoption, funnel behavior, experimentation, KPIs, rollout, decisions.
- Data Science: problem formulation, preparation, feature engineering, statistics/ML, evaluation, explainability, deployment, impact.
- AI/LLM: LLM/RAG architecture, retrieval, evaluation, experiments, workflow integration, responsible AI, adoption.
- Data, analytics, product, and technology roles: retain at least one confirmed LLM, GenAI, or agentic-AI accomplishment in Experience when relevant evidence exists. Treat this as a portfolio preference, not a keyword mandate; preserve the actual system architecture and never insert AI terminology into unrelated work or displace substantially stronger core evidence.

### 5. Design the bullet portfolio

Default each bullet to one distinct project or substantial business problem. Consolidate source bullets that merely describe stages of the same end-to-end project, but do not combine unrelated projects, split one project into cosmetic variants, or let one project provide a majority under an experience without explicit approval. Name the project, product, platform, or business problem when doing so helps an external reader understand the accomplishment.

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

Always wait for explicit content approval before creating or modifying the final tailored resume. Treat the approved portfolio, ordering, and bullet count as locked. During layout optimization, shorten wording only when meaning is preserved; never remove, replace, or reorder approved content without further approval.

### 7. Write from confirmed evidence

Draft with a flexible pattern: `Primary action verb + named project or business problem + method/scope + concrete result`. Prefer substantive evidence and emphasis changes over keyword swaps. Use accurate JD terminology naturally, past tense for completed work, a credible professional voice, and lengths that fit the base layout. Represent the documented level of ownership precisely and do not turn association into causality.

- Write the summary from the role-specific value proposition, typically in two or three concise sentences. Communicate one professional identity, two or three relevant strengths, the value delivered, and a credible differentiator when useful. Differentiate the candidate rather than list generic qualifications or years-of-experience formulas, without turning the summary into a resume recap.
- Frame accomplishments around why the work mattered, using a confirmed metric or a defensible non-quantified outcome such as faster access to evidence, reduced processing time, improved risk assessment, a completed review cycle, fewer errors, stakeholder use, or a reusable capability. State what changed for the stakeholder instead of ending with a generic claim. When stronger impact is plausible but undocumented, label it `Needs confirmation`, explain the inference, and obtain user approval. Never invent impact, causality, adoption, ownership, scope, or metrics.
- Begin every Experience bullet with one clear primary action verb. Do not coordinate two opening verbs, such as `Built and optimized` or `Designed and implemented`; select the verb that best represents the primary contribution and describe supporting work later in the sentence.
- Calibrate bullet length to JD relevance, evidence strength, and page value instead of forcing uniform length. Allow the strongest, most role-relevant bullets to use up to three rendered lines when the added detail materially strengthens the match; keep supporting or lower-priority bullets shorter. Never pad a weak bullet or remove useful evidence merely to make bullet lengths look consistent.
- Translate internal, proprietary, or domain-specific labels into audience-friendly language when the exact term does not help an external reviewer. For example, prefer `legal documents` over `case-assessment documents`. Preserve the underlying scope and meaning, and retain the original term only when the JD uses it or accuracy requires it.
- Do not use em dashes (`—`) in resume content because they can make the writing feel AI-generated. Rewrite with a comma, semicolon, colon, parentheses, or a separate sentence. En dashes (`–`) remain appropriate for numeric and date ranges such as `2023–Present`.

### 8. Audit and deliver

Trace every substantive claim to a current project story, selectively verified image, or confirmed resume fact. Audit requirement coverage, early-bullet strength, project diversity, competency range, technical depth, natural ATS alignment, dates/titles/tools/metrics, confidentiality, single-verb bullet openings, absence of em dashes in resume content, and meaningful differentiation from other role-family versions.

Save to the existing appropriate output folder. If no convention exists, use `Company Name_Job Name_Resume.docx`. Preserve the base resume's visual structure, page count, and density.

Normalize section-heading rules before rendering. When headings use bottom paragraph borders, run `scripts/normalize-section-rules.py` on the tailored DOCX so every rule uses one canonical border definition and explicit zero left/right paragraph indents. Audit the rendered PDF to confirm that all section rules begin and end at the same horizontal positions; matching color and thickness alone is insufficient.

Prioritize first-page value and utilization because some reviewers may not continue to page 2. Put the strongest, most role-relevant evidence on page 1 and use its available space well. Avoid manual page breaks, content ordering, or premature section moves that leave material avoidable whitespace on page 1. Prefer moving relevant content forward or rebalancing natural breaks before changing typography or spacing; never make the page crowded, reduce readability, shrink text below the base resume's size, or add filler merely to make page 1 look full.

Render the source and tailored DOCX using the DOCX-support path and inspect every page at 100%. Compare page count, margins, typography, sections, indentation, spacing, alignment, wrapping, page breaks, and first-page utilization. Iterate after changes. If Word and LibreOffice are unavailable, perform structural checks and disclose that visual QA was not completed.

After the final render passes, clean up task-created working artifacts before delivery. Inventory the exact paths first, then remove only artifacts created during the current tailoring task, including QA PDFs, rendered page PNGs and their output folders, temporary editing or conversion scripts, temporary extracted text, and disposable comparison files. Never remove the final resume, saved JD, source materials, caches owned by another workflow, pre-existing user files, or any artifact whose ownership is uncertain. Verify with a final filesystem check that no task-created QA or temporary artifacts remain outside an intentional temporary/cache location.

Return a concise coverage report with strongly supported, partially supported, and unsupported requirements; project diversity by final bullet; important changes; and claims needing confirmation.

## Shipping gate

Do not finalize until the source and output name are unambiguous, the user has approved the content portfolio, every substantive claim is verified or user-confirmed, the resume complies with any local experience policy, the latest DOCX passes structural and visual QA, and task-created temporary artifacts are cleaned up.
