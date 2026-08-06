# Evidence retrieval workflow

## Stages

1. **Route with the catalog.** Use `.agents/resume-tailor-project-catalog.json` to identify likely projects by broad themes and role families. Keep the catalog free of claims, actions, methods, metrics, and narratives.
2. **Extract locally.** Run `scripts/retrieve-project-evidence.py` with the complete saved JD or an attached UTF-8 text file. The script splits each current DOCX into heading-based sections locally.
3. **Reuse safely.** Store extracted sections under the operating system's temporary directory. Compare SHA-256 hashes on every run; refresh only changed source documents.
4. **Parse and weight requirements.** Separate responsibilities, minimum qualifications, role context, and preferred qualifications. Weight them at `1.35`, `1.25`, `1.10`, and `0.80` respectively. Treat unstructured text as `other` with weight `1.00`.
5. **Rank per requirement.** Apply lexical ranking plus concept expansion, heading weighting, and catalog routing metadata independently for each requirement. Cap repeated query-term weight and per-project results. Use the deduplicated portfolio shortlist only for navigation; inspect each requirement's candidates when building the evidence map.
6. **Treat results as candidates.** Never classify a search result as confirmed evidence.
7. **Verify at source.** Re-open each selected section directly from its original DOCX with `--verify-path` and `--section-index`. Add `--context-sections 1` when ownership, method, metric, or context crosses section boundaries. Increase context selectively rather than loading the entire document.
8. **Expand selectively.** Increase `--per-requirement`, inspect another project, or review a relevant image only when the initial evidence is incomplete. Use `--mode flat` only to diagnose an unstructured query, not as the default evidence-mapping workflow.
9. **Build the temporary map.** Convert only verified evidence into `Confirmed`; classify ambiguous or absent evidence normally.

## Commands

Refresh the lightweight catalog after adding, moving, or renaming project-story documents:

```powershell
py .agents/skills/resume-tailor/scripts/refresh-project-catalog.py --workspace .
```

Retrieve candidates from a saved JD:

```powershell
py .agents/skills/resume-tailor/scripts/retrieve-project-evidence.py `
  --workspace . `
  --jd-docx "Job Descriptions/Company_Role.docx" `
  --top 8 `
  --per-project 3 `
  --per-requirement 3 `
  --format json
```

Retrieve candidates directly from an attached or saved UTF-8 text JD:

```powershell
py .agents/skills/resume-tailor/scripts/retrieve-project-evidence.py `
  --workspace . `
  --query-file "path/to/pasted-text.txt" `
  --top 8 `
  --per-project 3
```

Verify one candidate directly against its source:

```powershell
py .agents/skills/resume-tailor/scripts/retrieve-project-evidence.py `
  --workspace . `
  --verify-path "Projects/Project/complete story.docx" `
  --section-index 12 `
  --context-sections 1
```

Use `--format json` for structured processing. Use `--cache-dir` only when the default system temporary directory is unavailable.

The JSON payload contains `requirements`, where each entry includes its category, weight, text, and candidate sections. The top-level `results` list is a deduplicated portfolio shortlist aggregated with weighted reciprocal rank so raw BM25 scores from differently sized requirements are not compared directly. `--mode flat` preserves whole-query ranking for debugging and backward compatibility.

## Cache boundaries

- Treat the cache as disposable acceleration data, never as evidence.
- Do not place the cache in the skill or project-material folders.
- Do not manually edit cached extraction files.
- Hash validation prevents stale content when a source document changes.
- Delete the cache at any time without losing project information.
