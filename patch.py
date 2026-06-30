"""Patch locale UI files in-place.

This script targets the current structure under js/data/locales/ui/*.js.
It ensures these keys exist in chemTools for all configured languages:
- zeroAsFormula
- bareCoefficient
- zeroInSubscript

And it ensures tutorial sections exist for:
- ar, ru, fa, ur, tl
  - balancerTutorial
  - predictorTutorial
  - molarMassTutorial
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
LOCALES_DIR = ROOT / "js" / "data" / "locales" / "ui"


CHEMTOOLS_KEYS = {
    "zeroAsFormula": "\"{formula}\" is not a valid formula - did you type 0 (zero) instead of O (oxygen)? Try \"{suggestion}\".",
    "bareCoefficient": "\"{formula}\" is not a valid compound formula. Write formulas starting with an element symbol, e.g. \"H2O\".",
    "zeroInSubscript": "Did you type 0 (zero) instead of O (oxygen) in \"{formula}\"? Did you mean \"{suggestion}\"?",
}


TUTORIAL_BLOCK = """  \"balancerTutorial\": {
    \"modeTitle\": \"Mode Switch\",
    \"modeDesc\": \"Switch between balancing an existing equation and predicting products of a new reaction.\",
    \"scaleTitle\": \"Physics Scale\",
    \"scaleDesc\": \"This scale visualizes atom imbalance in real time.\",
    \"inputReactantsTitle\": \"Reactants\",
    \"inputReactantsDesc\": \"Enter your reactants here.\",
    \"inputProductsTitle\": \"Products\",
    \"inputProductsDesc\": \"Enter products to complete your equation.\",
    \"autoTitle\": \"Auto Balance\",
    \"autoDesc\": \"Click auto-balance to calculate integer coefficients instantly.\",
    \"feedbackTitle\": \"Status & Copy\",
    \"feedbackDesc\": \"Copy the final balanced equation with one click.\"
  },
  \"predictorTutorial\": {
    \"modeTitle\": \"Mode Switch\",
    \"modeDesc\": \"Use prediction mode to infer likely products from reactants.\",
    \"inputTitle\": \"Reactants\",
    \"inputDesc\": \"Type your reactants in this field.\",
    \"typeTitle\": \"Reaction Type\",
    \"typeDesc\": \"Choose the expected reaction category.\",
    \"predictTitle\": \"Predict Products\",
    \"predictDesc\": \"Run prediction to get products and auto-balanced equation.\",
    \"resultTitle\": \"Smart Result\",
    \"resultDesc\": \"Review predicted products, balanced equation, and rationale.\"
  },
  \"molarMassTutorial\": {
    \"inputTitle\": \"Formula Input\",
    \"inputDesc\": \"Enter any chemical formula.\",
    \"previewTitle\": \"Live Preview\",
    \"previewDesc\": \"Formula preview updates with proper subscripts in real time.\",
    \"scaleTitle\": \"Interactive Scale\",
    \"scaleDesc\": \"Scale animation reflects computed molar mass.\",
    \"receiptTitle\": \"Weight Receipt\",
    \"receiptDesc\": \"Print a detailed breakdown by atom counts and masses.\",
    \"chipsTitle\": \"Quick Examples\",
    \"chipsDesc\": \"Use quick chips to load common compounds instantly.\"
  },
"""


def upsert_chemtools_keys(text: str) -> str:
    chemtools_match = re.search(r'(\"chemTools\"\s*:\s*\{)', text)
    if not chemtools_match:
        return text

    insert_at = chemtools_match.end()
    additions = []
    for key, value in CHEMTOOLS_KEYS.items():
        if f'\"{key}\"' not in text:
            additions.append(f'\n    \"{key}\": \"{value}\",')

    if not additions:
        return text

    return text[:insert_at] + "".join(additions) + text[insert_at:]


def ensure_tutorial_blocks(text: str) -> str:
    has_all = all(k in text for k in ['\"balancerTutorial\"', '\"predictorTutorial\"', '\"molarMassTutorial\"'])
    if has_all:
        return text

    # Insert before final closing brace of exported object
    last_brace = text.rfind("};")
    if last_brace == -1:
        return text

    return text[:last_brace] + "\n" + TUTORIAL_BLOCK + text[last_brace:]


def patch_file(path: Path, add_tutorials: bool) -> None:
    original = path.read_text(encoding="utf-8")
    updated = upsert_chemtools_keys(original)
    if add_tutorials:
        updated = ensure_tutorial_blocks(updated)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"Updated: {path.name}")
    else:
        print(f"No changes: {path.name}")


def main() -> None:
    locale_files = {
        "en.js": False,
        "ar.js": True,
        "zh.js": False,
        "fr.js": False,
        "ru.js": True,
        "fa.js": True,
        "ur.js": True,
        "tl.js": True,
    }

    for file_name, add_tutorials in locale_files.items():
        path = LOCALES_DIR / file_name
        if not path.exists():
            print(f"Missing: {file_name}")
            continue
        patch_file(path, add_tutorials)

    print("Patch complete.")


if __name__ == "__main__":
    main()
