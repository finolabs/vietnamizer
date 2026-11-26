# Contract: run record

The harness writes one JSON object per run beside its output:

```json
{"article": "D02", "model": "claude-opus-5-5", "version": "0.16.2", "rep": 1, "label": "t038-1a2b3c4d",
 "cost_usd": 0.327, "cache_write": 22019, "cache_read": 180022, "output": 5723, "seconds": 51.2, "turns": 6,
 "reads": [{"tool": "Skill", "target": "vietnamizer:vietnamizer"}, {"tool": "Read", "target": "<install>/skills/vietnamizer/references/writing-workflow.md"}],
 "valid": true}
```

**Fields:**
- `reads` lists every tool call, in order.
- `target` is the skill name or the file path.
- Paths outside the run's install folder make `valid` false.

**Index:** the index file has the same shape as `runs-t035.json`. Each entry gets an added `"valid"` field, and `holdout_036.py score` reads only valid entries: the harness writes only valid runs to the index.

**Report:** cost and time are means per model and version. Reads are counted per file.
