# Evidence retrieval workflow

## Stages

1. **Route with the catalog.** Use `.agents/resume-tailor-project-catalog.json` to identify likely projects by broad themes and role families. Keep the catalog free of claims, actions, methods, metrics, and narratives.
2. **Extract locally.** Run `scripts/retrieve-project-evidence.py` with the complete saved JD or an attached UTF-8 text file. The script splits each current DOCX into heading-based sections locally.
3. **Reuse safely.** Store extracted sections under the operating system's temporary directory. Compare SHA-256 hashes on every run; refresh only changed source documents.
4. **Rank candidates.** Apply lexical ranking plus concept expansion and catalog routing metadata. Cap repeated query-term weight, prefer primary Action/Result/Method sections, and down-rank derivative interview summaries. Return only a small number of high-scoring sections, with a default per-project cap to preserve cross-project discovery.
5. **Treat results as candidates.** Never classify a search result as confirmed evidence.
6. **Verify at source.** Re-open each selected section directly from its original DOCX with `--verify-path` and `--section-index`. Add `--context-sections 1` when ownership, method, metric, or context crosses section boundaries. Increase context selectively rather than loading the entire document.
7. **Expand selectively.** Increase `--top`, inspect another project, or review a relevant image only when the initial evidence is incomplete.
8. **Build the temporary map.** Convert only verified evidence into `Confirmed`; classify ambiguous or absent evidence normally.

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
  --per-project 3
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

## Cache boundaries

- Treat the cache as disposable acceleration data, never as evidence.
- Do not place the cache in the skill or project-material folders.
- Do not manually edit cached extraction files.
- Hash validation prevents stale content when a source document changes.
- Delete the cache at any time without losing project information.
