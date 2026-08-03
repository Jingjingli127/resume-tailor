# Resume Tailor

Resume Tailor is an evidence-grounded Codex skill for tailoring Word resumes to job descriptions. It retrieves role-relevant material from current project-story documents, requires source verification before drafting claims, preserves project diversity, and audits the final DOCX against the selected base resume.

## Highlights

- Tailors project emphasis instead of performing keyword substitution
- Labels evidence as Confirmed, Needs confirmation, or Unsupported
- Uses a lightweight project catalog and hash-invalidated local retrieval cache
- Verifies shortlisted evidence against original DOCX sections
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

## Privacy

The repository intentionally contains no resumes, project stories, job descriptions, project catalogs, evidence maps, or generated documents. Use fictional data for any examples committed to a public fork. Review staged files and document metadata before every public push.

## License

MIT
