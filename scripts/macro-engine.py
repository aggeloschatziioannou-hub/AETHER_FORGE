import os
import json
import subprocess
import sys
import re
import shutil
from datetime import datetime, UTC

GITNEXUS_META = ".gitnexus/meta.json"
SOKG_PATH = "memory-vault/gitnexus-sokg.json"
TODO_PATH = "memory-vault/todo.md"
LEDGER_PATH = "memory-vault/evolution-ledger.json"
IGNORE_DIRS = {".git", "node_modules", ".next", ".gitnexus", "__pycache__"}
IGNORE_FILES = {"package-lock.json", "pnpm-lock.yaml"}
IGNORE_EXTS = {".png", ".ico", ".jpg", ".jpeg", ".gif", ".svg"}


def get_environment_snapshot():
    snapshot = {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    binaries = {
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "firebase": ["firebase", "--version"],
        "git": ["git", "--version"],
    }
    for name, args in binaries.items():
        try:
            res = subprocess.run(args, capture_output=True, text=True, timeout=5)
            snapshot[name] = res.stdout.strip() if res.returncode == 0 else "NOT_FOUND"
        except Exception:
            snapshot[name] = "NOT_FOUND"
    return snapshot


def scan_files(root):
    files = []
    for dirpath, dirs, names in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        if rel == ".":
            rel = ""
        parts = rel.split(os.sep)
        if any(p in IGNORE_DIRS or p.startswith(".") for p in parts):
            continue
        for name in sorted(names):
            if name in IGNORE_FILES:
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in IGNORE_EXTS:
                continue
            path = os.path.join(dirpath, name)
            try:
                stat = os.stat(path)
                files.append({
                    "path": os.path.relpath(path, root),
                    "size_bytes": stat.st_size,
                    "ext": ext,
                })
            except OSError:
                pass
    return files


def get_git_state():
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5
        ).stdout.strip()
        recent = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, timeout=5
        ).stdout.strip().split("\n")
        return {"branch": branch, "recent_commits": recent}
    except Exception:
        return {"branch": "unknown", "recent_commits": []}


def parse_tasks(path):
    completed = []
    pending = []
    stages = []
    if not os.path.exists(path):
        return completed, pending, stages
    with open(path) as f:
        for line in f:
            m = re.match(r"- \[([ x])\] (.+)", line)
            if m:
                task = m.group(2).strip()
                if m.group(1) == "x":
                    completed.append(task)
                else:
                    pending.append(task)
            m2 = re.match(r"- \[([ x])\] STAGE (\d+) :: (.+) -> (.+)", line)
            if m2:
                stages.append({
                    "id": int(m2.group(2)),
                    "title": m2.group(3).strip(),
                    "status": m2.group(4).strip(),
                    "done": m2.group(1) == "x",
                })
    return completed, pending, stages


def get_app_config():
    pkg = "aether-forge-app/package.json"
    if not os.path.exists(pkg):
        return {}
    with open(pkg) as f:
        data = json.load(f)
    return {
        "name": data.get("name"),
        "version": data.get("version"),
        "scripts": data.get("scripts", {}),
        "dependencies": list(data.get("dependencies", {}).keys()),
        "devDependencies": list(data.get("devDependencies", {}).keys()),
    }


def find_gitnexus():
    gitnexus = shutil.which("gitnexus")
    if gitnexus:
        return gitnexus
    candidates = [
        os.path.expanduser("~/.global_modules/bin/gitnexus"),
        os.path.expanduser("~/.npm-global/bin/gitnexus"),
        "/usr/local/bin/gitnexus",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def run_gitnexus_analyze():
    gitnexus = find_gitnexus()
    if not gitnexus:
        print("gitnexus not found. Install: npm install -g gitnexus")
        return
    try:
        res = subprocess.run(
            [gitnexus, "analyze"],
            capture_output=True, text=True, timeout=120
        )
        print(res.stdout)
        if res.returncode != 0:
            print(f"gitnexus stderr: {res.stderr}")
    except subprocess.TimeoutExpired:
        print("gitnexus analyze timed out")


def read_gitnexus_stats():
    if not os.path.exists(GITNEXUS_META):
        return None
    try:
        with open(GITNEXUS_META) as f:
            return json.load(f).get("stats")
    except (json.JSONDecodeError, KeyError):
        return None


def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH) as f:
        return json.load(f)


def run_seed_instructions():
    try:
        subprocess.run(
            [sys.executable, "scripts/seed-instructions.py"],
            capture_output=True, text=True, timeout=30
        )
        print("Instruction DB refreshed")
    except Exception as e:
        print(f"seed-instructions failed: {e}")


def read_evolution_from_db():
    try:
        import sqlite3
        conn = sqlite3.connect("memory-vault/project-instructions.db")
        c = conn.cursor()
        c.execute("SELECT id, timestamp, agent, event_type, summary FROM evolution ORDER BY id DESC LIMIT 20")
        rows = c.fetchall()
        conn.close()
        return [{"id": r[0], "timestamp": r[1], "agent": r[2], "type": r[3], "summary": r[4]} for r in rows]
    except Exception as e:
        return []


def run_macro_aggregation():
    print("Running macro aggregation — GitNexus-powered")
    env = get_environment_snapshot()
    git = get_git_state()
    app_config = get_app_config()
    completed_tasks, pending_tasks, stages = parse_tasks(TODO_PATH)
    files = scan_files(".")
    ledger = load_ledger()

    run_seed_instructions()
    run_gitnexus_analyze()
    stats = read_gitnexus_stats()
    evolution = read_evolution_from_db()

    if os.path.exists(SOKG_PATH):
        os.remove(SOKG_PATH)
        print(f"Removed old SOKG: {SOKG_PATH}")

    bundle = {
        "generated_at": env["timestamp"],
        "environment": env,
        "git": git,
        "app": app_config,
        "tasks": {
            "completed": completed_tasks,
            "pending": pending_tasks,
            "stages": stages,
        },
        "file_inventory": {
            "total_count": len(files),
            "total_size_bytes": sum(f["size_bytes"] for f in files),
            "files": files,
        },
        "gitnexus": stats,
        "evolution_log": evolution,
        "ledger_entries": len(ledger),
    }

    os.makedirs("memory-vault/analytics", exist_ok=True)
    path = "memory-vault/analytics/project-state-bundle.json"
    with open(path, "w") as f:
        json.dump(bundle, f, indent=2)

    print(f"Snapshot written ({os.path.getsize(path)} bytes)")
    if stats:
        print(f"GitNexus: {stats.get('nodes', 0)} symbols, "
              f"{stats.get('edges', 0)} relationships, "
              f"{stats.get('communities', 0)} clusters")
    print(f"Tasks: {len(completed_tasks)} completed, {len(pending_tasks)} pending")
    print(f"Evolution entries: {len(evolution)}")
    print("Done")


if __name__ == "__main__":
    run_macro_aggregation()
