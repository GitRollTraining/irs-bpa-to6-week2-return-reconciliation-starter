import json
import os
import sqlite3
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from return_desk.parser import identity
from return_desk.reconcile import reconcile


class BatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    expected: list[dict]


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS batches (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            db.execute(
                "CREATE TABLE IF NOT EXISTS inspections (id TEXT PRIMARY KEY, batch_id TEXT NOT NULL, payload TEXT NOT NULL)"
            )

    def connect(self):
        return sqlite3.connect(self.path)

    def save_inspection(self, report):
        with self.connect() as db:
            db.execute(
                "INSERT INTO inspections VALUES (?, ?, ?)",
                (report["inspection_id"], report["batch_id"], json.dumps(report)),
            )


def create_app(path=None):
    app = FastAPI()
    store = Store(path or os.environ.get("RETURN_DESK_DB", "data/desk.sqlite3"))
    app.state.store = store

    @app.exception_handler(sqlite3.Error)
    async def storage_error(request, exc):
        return JSONResponse(
            status_code=503,
            content={"detail": "Storage unavailable; nothing accepted. Retry when storage is available."},
        )

    @app.get("/api/health")
    def health():
        with store.connect() as db:
            db.execute("SELECT 1")
        return {"status": "ok"}

    @app.get("/api/batches")
    def batches():
        with store.connect() as db:
            return [json.loads(row[0]) for row in db.execute("SELECT payload FROM batches ORDER BY rowid")]

    def get_batch(batch_id):
        with store.connect() as db:
            row = db.execute("SELECT payload FROM batches WHERE id=?", (batch_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Batch not found")
        return json.loads(row[0])

    @app.post("/api/batches", status_code=201)
    def register(body: BatchInput):
        name = body.name.strip()
        if not 1 <= len(name) <= 100 or not 1 <= len(body.expected) <= 20:
            raise HTTPException(422, "Name must be 1–100 characters and list must contain 1–20 identities")
        try:
            expected = [identity(**x) for x in body.expected]
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, str(exc)) from exc
        if len({(x["return_id"], x["year"]) for x in expected}) != len(expected):
            raise HTTPException(422, "Duplicate expected identity")
        batch = {"batch_id": str(uuid4()), "name": name, "expected": expected}
        with store.connect() as db:
            db.execute("INSERT INTO batches VALUES (?, ?)", (batch["batch_id"], json.dumps(batch)))
        return batch

    @app.get("/api/batches/{batch_id}/inspections")
    def inspections(batch_id: str):
        get_batch(batch_id)
        with store.connect() as db:
            return [
                {"inspection_id": row[0], "ready": json.loads(row[1])["ready"]}
                for row in db.execute("SELECT id,payload FROM inspections WHERE batch_id=? ORDER BY rowid", (batch_id,))
            ]

    @app.post("/api/batches/{batch_id}/inspections", status_code=201)
    async def inspect(batch_id: str, files: Annotated[list[UploadFile], File()]):
        batch = get_batch(batch_id)
        if not 1 <= len(files) <= 30:
            raise HTTPException(422, "Supply 1–30 files")
        uploads = []
        for file in files:
            raw = await file.read(262145)
            if len(raw) > 262144:
                raise HTTPException(413, "Each file must be at most 262144 bytes; delivery rejected")
            uploads.append((file.filename or "unnamed", raw))
        report = reconcile(batch, uploads)
        store.save_inspection(report)
        return report

    @app.get("/api/batches/{batch_id}/inspections/{inspection_id}")
    def report(batch_id: str, inspection_id: str):
        with store.connect() as db:
            row = db.execute(
                "SELECT payload FROM inspections WHERE id=? AND batch_id=?", (inspection_id, batch_id)
            ).fetchone()
        if not row:
            raise HTTPException(404, "Inspection not found")
        return JSONResponse(
            json.loads(row[0]),
            headers={"Content-Disposition": f'attachment; filename="inspection-{inspection_id}.json"'},
        )

    return app
