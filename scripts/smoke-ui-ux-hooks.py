"""Optional SessionStart runtime and post-tool command smoke checks.

No external model call, provider credentials, application edits or persisted task.
Uses isolated CODEX_HOME and one-invocation trust for only these reviewed hooks.
"""

import argparse
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default=shutil.which("codex"))
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI is required for this optional runtime smoke test")
    spec = importlib.util.spec_from_file_location("hook_install", ROOT / "scripts/install-ui-ux-hooks.py")
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    observations = []

    class ModelStub(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            # Keep only booleans/counts, never the context or transcript itself.
            content = json.dumps(body.get("input", []))
            observations.append({"health": "UI/UX library available" in content,
                                 "integrity": "VERIFIED: UI/UX package integrity only" in content,
                                 "unverified": "NOT VERIFIED: UI/UX hook" in content})
            sequence = len(observations)
            item = {"type": "message", "id": "msg_end", "role": "assistant", "status": "completed",
                    "content": [{"type": "output_text", "text": "Smoke completed", "annotations": []}]}
            response = {"id": f"resp_{sequence}", "object": "response", "status": "completed", "output": [item],
                        "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}
            events = [
                {"type": "response.created", "response": {**response, "status": "in_progress", "output": []}},
                {"type": "response.output_item.added", "output_index": 0, "item": item},
                {"type": "response.output_item.done", "output_index": 0, "item": item},
                {"type": "response.completed", "response": response},
            ]
            payload = "".join("data: " + json.dumps(event) + "\n\n" for event in events).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    server = ThreadingHTTPServer(("127.0.0.1", 0), ModelStub)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with tempfile.TemporaryDirectory(prefix="ui-ux-runtime-") as temporary:
            base = Path(temporary)
            codex = base / ".codex"
            codex.mkdir()
            skills = base / "skills"
            for name in ("ui-spec", "ui-build", "ui-verify"):
                shutil.copytree(ROOT / "skills" / name, skills / name)
                (skills / name / "library-root.txt").write_text(str(ROOT / "docs/ux"), encoding="utf-8")
            definitions = installer.definitions(ROOT, skills, codex)
            (codex / "hooks.json").write_text(json.dumps({"hooks": {key: [value] for key, value in definitions.items()}}), encoding="utf-8")
            (codex / "config.toml").write_text(
                'model = "hook-smoke"\nmodel_provider = "hook_smoke"\n'
                '[model_providers.hook_smoke]\nname = "Offline hook smoke"\n'
                f'base_url = "http://127.0.0.1:{server.server_port}/v1"\n'
                'wire_api = "responses"\nrequires_openai_auth = false\nrequest_max_retries = 0\n'
                'stream_max_retries = 0\nsupports_websockets = false\n', encoding="utf-8")
            environment = dict(os.environ, CODEX_HOME=str(codex), UI_UX_DOCS_ROOT=str(ROOT / "docs/ux"))
            result = subprocess.run([args.codex, "exec", "--ephemeral", "--skip-git-repo-check", "--json",
                                     "--dangerously-bypass-hook-trust", "Run the deterministic offline hook smoke."],
                                    cwd=base, env=environment, stdin=subprocess.DEVNULL,
                                    capture_output=True, text=True, encoding="utf-8", timeout=45)
            if result.returncode or len(observations) != 1 or not observations[0]["health"] or observations[0]["unverified"]:
                # CLI stderr may contain configuration paths, never provider input.
                raise RuntimeError(json.dumps({"exit": result.returncode, "observations": observations,
                                               "stderr_tail": result.stderr[-1800:]}))
            # Exercise the exact installed command and JSON protocol independently.
            # This does not assert that Codex dispatched PostToolUse after a real tool.
            definition = definitions["PostToolUse"]["hooks"][0]
            command = ([shutil.which("pwsh") or "powershell.exe", "-NoProfile", "-Command", definition["commandWindows"]]
                       if os.name == "nt" else ["/bin/sh", "-c", definition["command"]])
            event = json.dumps({"hook_event_name": "PostToolUse", "session_id": "smoke", "tool_name": "Bash"})
            replies = []
            for _ in range(2):
                check = subprocess.run(command, input=event, cwd=base, env=environment,
                                       capture_output=True, text=True, encoding="utf-8", timeout=10, check=True)
                replies.append(json.loads(check.stdout))
            if "VERIFIED: UI/UX package integrity only" not in json.dumps(replies[0]) or replies[1] != {}:
                raise RuntimeError("Post-tool command did not report integrity and suppress the duplicate")
            records = json.loads((codex / "cache/ui-ux-hooks-state.json").read_text())
            if len(records) != 1:
                raise RuntimeError("Expected one session fingerprint after repeated tool events")
            print(json.dumps({"status": "VERIFIED", "scope": "Actual Codex SessionStart; direct installed PostToolUse command and duplicate suppression. Codex post-tool dispatch is NOT VERIFIED.", "model_requests": len(observations), "cache_records": len(records)}))
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
