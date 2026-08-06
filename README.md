# Resume Tailor

Resume Tailor is an evidence-grounded Codex skill for tailoring Word resumes to job descriptions. It retrieves role-relevant material from current project-story documents, requires source verification before drafting claims, preserves project diversity, and audits the final DOCX against the selected base resume.

## The problem it solves

Giving a chatbot only a base resume and a job description usually produces shallow tailoring. The model can see the wording already on the resume, but it has no knowledge of the fuller projects behind those bullets. As a result, it tends to rephrase existing statements, insert job-description keywords, or make cosmetic adjustments without changing the underlying evidence.

That is a problem because the same project can legitimately demonstrate different competencies:

- A Data Analyst application may emphasize data preparation, SQL analysis, KPI development, visualization, trend identification, and business recommendations.
- A Data Scientist application may emphasize problem formulation, feature engineering, statistical methods, machine learning, evaluation, explainability, and implementation.
- A Product Analytics application may emphasize user behavior, funnels, adoption, experimentation, rollout measurement, and product decisions.
- An AI or LLM application may emphasize retrieval architecture, evaluation, workflow integration, responsible AI, and user adoption.

Resume Tailor starts from complete project stories rather than treating the existing resume bullets as the full universe of available evidence. For each JD, it selects a different set of confirmed project components, builds a role-specific evidence map, and then drafts a project-diverse bullet portfolio. The goal is substantive tailoring: different target roles should result in genuinely different project emphasis, not merely different keywords.

## Role scope

Out of the box, Resume Tailor is optimized for Data Science, Data Analytics/BI, Product Analytics, Machine Learning, and AI/LLM roles, plus adjacent experimentation, risk, research, and data-product positions. Its evidence-grounding architecture can be adapted to other project-based professions.

### Extending it to other professions

The evidence-verification and document-QA workflow is profession-agnostic. Supporting another field mainly requires adding its competency emphasis to `SKILL.md`, domain vocabulary and heading patterns to `retrieve-project-evidence.py`, and appropriate catalog and portfolio-diversity rules. Test each new role family with fictional project stories and JDs to ensure it selects meaningfully different evidence without introducing unsupported claims.

## Highlights

- Tailors project emphasis instead of performing keyword substitution
- Labels evidence as Confirmed, Needs confirmation, or Unsupported
- Uses a lightweight project catalog and hash-invalidated local retrieval cache
- Verifies shortlisted evidence against original DOCX sections
- Distinguishes direct, transferable, and unsupported project evidence without blocking stretch applications
- Preserves the base resume's structure and visual hierarchy
- Supports private, workspace-specific experience policies
- Prevents silent overwrites and requires rendered document QA

## Installation

Clone the repository into a workspace or copy `.agents/skills/resume-tailor/` into the corresponding project-scoped skills directory.

Install the Python dependencies:

```powershell
py -m pip install -r requirements.txt
```

Python 3.11 or newer is recommended. Microsoft Word is supported by the included Windows PDF-export helper. A compatible DOCX-to-PDF renderer such as LibreOffice can be used on other systems.

## Workspace setup

Keep resumes, project stories, job descriptions, and generated output outside the skill directory. The discovery script searches the workspace rather than requiring fixed folder names.

Optionally copy `examples/resume-tailor.local.example.json` to `resume-tailor.local.json` and replace the fictional values with private experience-selection rules. This local file is ignored by Git.

Create or refresh the lightweight routing catalog:

```powershell
py .agents/skills/resume-tailor/scripts/refresh-project-catalog.py --workspace .
```

The generated `.agents/resume-tailor-project-catalog.json` is ignored by Git because it can contain employer names, project names, and local source paths.

## Use

Invoke the project-scoped skill and provide a base resume, company, job title, and complete job description:

```text
Use $resume-tailor to tailor my specified base resume to this job description.
Preserve formatting, use only confirmed evidence, and show the evidence map and
proposed bullet portfolio before generating the final DOCX.
```

## Evidence retrieval and project mapping

The retrieval layer is designed to avoid two common failure modes: repeatedly loading every project story into the model context and maintaining a second detailed evidence database that becomes stale when the original documents change.

The workflow uses the original project-story documents as the only detailed sources of truth:

```text
Complete project stories
        |
        v
Lightweight project catalog
        |
        v
Weighted JD requirements
        |
        v
Per-requirement section retrieval
        |
        v
Direct source verification
        |
        v
Temporary JD-to-project evidence map
        |
        v
Project-diverse bullet portfolio
```

### 1. Lightweight catalog routing

`refresh-project-catalog.py` discovers current complete-story documents and maintains a compact catalog containing only:

- project name;
- employer or experience;
- source-document path;
- broad project themes;
- relevant role families;
- available supporting-image types.

The catalog helps decide which projects are likely to matter for a JD, but deliberately excludes detailed actions, methodologies, metrics, and narratives. Those facts remain in the original documents, so users do not have to maintain the same evidence in two places. Refreshing the catalog also discovers newly added, moved, or renamed project stories.

### 2. JD-driven section retrieval

`retrieve-project-evidence.py` separates the JD into responsibilities, minimum qualifications, role context, and preferred qualifications, then ranks project-story sections independently for every requirement. Responsibilities and minimum qualifications receive more weight than preferred qualifications. The script combines lexical BM25-style ranking, limited concept expansion, catalog routing metadata, heading-aware weighting, and per-project and per-requirement result caps.

The per-project cap prevents one highly similar project from crowding every other project out of a requirement's candidate set. Primary action, method, testing, and result sections receive preference, while derivative interview summaries are down-weighted.

Candidates are labeled `direct`, `transferable`, or `no_confirmed_evidence` from their exact, distinctive, and concept coverage against the original section text. These labels are advisory rather than application gates: transferable evidence must not claim the missing domain, and absent evidence does not prevent the workflow from producing a truthful stretch-application resume. JSON output includes a non-blocking resume strategy for every requirement and a deduplicated portfolio shortlist that excludes unsupported candidates. Flat whole-JD ranking remains available only as a diagnostic fallback.

### 3. Hash-invalidated local cache

Extracted sections are cached only as disposable acceleration data in the operating system's temporary directory. Every source document receives a SHA-256 hash. Unchanged documents can reuse their extraction, while edited documents are extracted again automatically.

The cache is never treated as evidence and can be deleted without losing project information. This provides faster repeated searches without creating a permanent duplicate evidence index.

### 4. Direct verification and cross-section context

Retrieval results are candidates, not confirmed claims. Before a fact can enter a resume, the selected section is reopened directly from its original DOCX using its source path and section index.

When ownership, methodology, or results span adjacent sections, contextual verification can include neighboring sections with `--context-sections`. This supports cross-section evidence while keeping the review focused and traceable. It does not combine unrelated sections or convert an inference into a confirmed claim.

Supporting images are reviewed selectively when they may clarify a referenced interface, workflow, result, or metric. Screenshot content alone is never used to infer ownership.

### 5. Temporary evidence map and portfolio design

Verified evidence is mapped to the current JD in a temporary table containing the requirement, best supporting project, project component, source section, evidence status and strength, recommended resume angle, and any clarification needed.

The map is rebuilt for each JD rather than saved as a permanent factual database. The resulting bullet portfolio is then checked for both JD coverage and project diversity, so tailoring changes the evidence and project emphasis instead of merely inserting keywords into an existing resume.

## Privacy

The repository intentionally contains no resumes, project stories, job descriptions, project catalogs, evidence maps, or generated documents. Use fictional data for any examples committed to a public fork. Review staged files and document metadata before every public push.

## License

MIT
