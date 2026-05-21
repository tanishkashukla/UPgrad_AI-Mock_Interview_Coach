from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS = ROOT / "prompts"


def load_prompt(name: str) -> str:
    for ext in (".md", ".txt"):
        p = PROMPTS / f"{name}{ext}"
        if p.exists():
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {name}")
