from collections import defaultdict
from uuid import uuid4

from return_desk.parser import InputIssue, parse_xml


def reconcile(batch, uploads):
    files, groups = [], defaultdict(list)
    expected_keys = {(x["return_id"], x["year"]) for x in batch["expected"]}
    for name, raw in uploads:
        item = {"file_id": str(uuid4()), "filename": name, "record": None, "issues": [], "outcome": "invalid"}
        try:
            item["record"] = parse_xml(raw)
        except InputIssue as exc:
            item["issues"] = [exc.issue]
        if item["record"] is not None:
            r = item["record"]
            groups[(r["return_id"], r["year"])].append(item)
        files.append(item)
    for key, members in groups.items():
        for item in members:
            if len(members) > 1:
                item["outcome"] = "duplicate"
                item["issues"] = [
                    {
                        "code": "DUPLICATE_IDENTITY",
                        "message": "Every copy must be resolved",
                        "identity": {"return_id": key[0], "year": key[1]},
                        "file_ids": [m["file_id"] for m in members],
                    }
                ]
            elif key in expected_keys:
                item["outcome"] = "matched"
            else:
                item["outcome"] = "unexpected"
                item["issues"] = [{"code": "UNEXPECTED_IDENTITY", "message": "Identity was not expected"}]
    missing = [x for x in batch["expected"] if (x["return_id"], x["year"]) not in groups]
    counts = {
        status: sum(f["outcome"] == status for f in files)
        for status in ("matched", "duplicate", "unexpected", "invalid")
    }
    counts.update(total=len(files), missing=len(missing))
    return {
        "format_version": 1,
        "synthetic": True,
        "disclaimer": "Training transport reconciliation; not tax validation",
        "batch_id": batch["batch_id"],
        "inspection_id": str(uuid4()),
        "batch_name": batch["name"],
        "expected": batch["expected"],
        "counts": counts,
        "missing": missing,
        "files": files,
        "ready": not any(counts[k] for k in ("missing", "duplicate", "unexpected", "invalid")),
    }
