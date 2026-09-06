#!/usr/bin/env python3
"""Register oxo-flow-community pipelines on WorkflowHub (site issue #72).

For every pipeline with a staged repo + metadata.json:
  1. build a Workflow RO-Crate (ro-crate-py): main.oxoflow as the main
     ComputationalWorkflow, the site's metro DAG SVG as the diagram image,
     metadata from metadata.json (title / description / creators placeholder /
     license mapped to WorkflowHub's closed enum / repo URL / keywords);
  2. POST it to https://workflowhub.eu/workflows with
     `workflow[project_ids][]=479`, `workflow[workflow_class_id]=15` (the
     Workflow Description Language class — all catalog entries use it) and
     the API token ($WORKFLOWHUB_TOKEN);
  3. record the returned workflow id in data/workflowhub.json
     (name -> {"id": N, "url": ..., "title": ...}), so re-runs skip
     already-registered pipelines (idempotent).

Publishing + DOI minting (`POST /workflows/:id/publish`, `POST /workflows/:id/
mint_doi`) is deliberately NOT part of this script — those DOIs are
per-version and should be minted deliberately once per release, not on every
registration run.

Requires: pip install rocrate requests
Env: WORKFLOWHUB_TOKEN (required), WORKFLOWHUB_PROJECT (optional, default
     479), STAGING (optional, default ~/Documents/GitHub/oxo-community/
     staging).
"""

from __future__ import annotations

import io
import json
import os
import pathlib
import sys
import tempfile
import time
import zipfile

import requests
from rocrate.rocrate import ROCrate

ROOT = pathlib.Path(__file__).resolve().parent.parent
PIPELINES = ROOT / "data" / "pipelines.json"
MAPPING = ROOT / "data" / "workflowhub.json"
SITE_DAG = ROOT / "docs" / "assets" / "dag"

STAGING = pathlib.Path(
    os.environ.get("STAGING", pathlib.Path.home() / "Documents" / "GitHub" / "oxo-community" / "staging")
)
BASE = "https://workflowhub.eu"
PROJECT_ID = os.environ.get("WORKFLOWHUB_PROJECT", "479")

# WorkflowHub (SEEK) license enum has no Apache/MIT; map to the closest
# permissive enum and keep the real SPDX id in the crate description.
LICENSE_MAP = {"apache-2.0": "other-open", "mit": "other-open"}


def token() -> str:
    tok = os.environ.get("WORKFLOWHUB_TOKEN")
    if not tok:
        sys.exit("set WORKFLOWHUB_TOKEN (WorkflowHub → Account → API token)")
    return tok


def workflow_file(repo: pathlib.Path) -> pathlib.Path | None:
    for cand in [repo / "main.oxoflow", *sorted(repo.glob("*.oxoflow")), *sorted(repo.glob("workflow/*.oxoflow"))]:
        if cand.is_file():
            return cand
    return None


def build_crate(meta: dict, wf: pathlib.Path, svg: pathlib.Path | None) -> bytes:
    """One Workflow RO-Crate per pipeline, returned as zip bytes."""
    crate = ROCrate()
    wf_props = {
        "name": meta["title"],
        "description": meta.get("description", ""),
        "license": LICENSE_MAP.get(meta.get("license", "").lower(), "notspecified"),
        "url": meta.get("repo_url", ""),
        "keywords": meta.get("tags", []),
        "programmingLanguage": {"@id": "https://github.com/Traitome/oxo-flow"},
    }
    crate.add_workflow(source=wf, dest_path=wf.name, main=True, lang="nextflow",
                       lang_version=None, properties=wf_props)
    crate.add_jsonld({
        "@id": "https://github.com/Traitome/oxo-flow",
        "@type": "ComputerLanguage",
        "name": "oxo-flow",
        "url": "https://github.com/Traitome/oxo-flow",
    })
    root = crate.root_dataset
    root["name"] = meta["title"]
    root["description"] = meta.get("description", "")
    root["license"] = LICENSE_MAP.get(meta.get("license", "").lower(), "notspecified")
    root["url"] = meta.get("repo_url", "")
    root["keywords"] = meta.get("tags", [])
    root["datePublished"] = meta.get("created")
    root["publisher"] = "oxo-flow-community"
    root["creativeWorkStatus"] = "Active"
    if svg and svg.is_file():
        crate.add_file(svg, dest_path="diagram.svg",
                       properties={"name": "Workflow diagram (metro map)",
                                   "encodingFormat": "image/svg+xml"})
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = pathlib.Path(tmp) / "ro_crate.crate.zip"
        crate.write_zip(zip_path)
        return zip_path.read_bytes()


def post(name: str, crate_bytes: bytes) -> int:
    data = {"workflow[project_ids][]": PROJECT_ID,
            "workflow[title]": name,
            "workflow[workflow_class_id]": "15"}
    files = {"ro_crate": ("ro_crate.crate.zip", crate_bytes,
                          "application/zip")}
    r = requests.post(f"{BASE}/workflows", data=data, files=files,
                      headers={"Authorization": f"Token {token()}"},
                      timeout=120)
    if r.status_code not in (200, 201):
        raise requests.HTTPError(f"HTTP {r.status_code}: {r.text[:500]}")
    return int(r.json()["data"]["id"])


def main() -> int:
    pipelines = json.loads(PIPELINES.read_text())
    mapping = json.loads(MAPPING.read_text()) if MAPPING.is_file() else {}
    todo = [p["name"] for p in pipelines if p["name"] not in mapping]
    print(f"{len(mapping)} already registered, {len(todo)} to do")
    for name in todo:
        repo = STAGING / name
        if not repo.is_dir():
            print(f"skip {name}: no staged checkout at {repo}")
            continue
        meta_f = repo / "metadata.json"
        wf = workflow_file(repo)
        if not meta_f.is_file() or wf is None:
            print(f"skip {name}: missing metadata.json or workflow file")
            continue
        meta = json.loads(meta_f.read_text())
        svg = SITE_DAG / f"{name}.svg"
        crate_bytes = build_crate(meta, wf, svg if svg.is_file() else None)
        for attempt in range(1, 6):
            try:
                wid = post(meta["title"], crate_bytes)
                break
            except requests.RequestException as e:  # noqa: PERF203
                print(f"  attempt {attempt} failed: {e}")
                time.sleep(5 * attempt)
        else:
            print(f"FAIL {name}: giving up after 5 attempts")
            continue
        url = f"{BASE}/workflows/{wid}"
        mapping[name] = {"id": wid, "url": url, "title": meta["title"]}
        MAPPING.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
        print(f"registered {name} -> {url}")
    print(f"done: {len(mapping)}/{len(pipelines)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
