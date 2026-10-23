"""Regression coverage for public, credential-free Achillea validation."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_public import validate_documents, validate_fixture, validate_repository


def fixture() -> dict:
    return {
        "schemaVersion": "0.1-draft",
        "status": "proposal-only; no implementation certified",
        "events": ["dispatch", "reduce"],
        "scenarios": [{
            "id": "first",
            "initialState": {"phase": "idle"},
            "intents": [{"type": "BEGIN"}],
            "reducerContract": [{"on": "BEGIN"}],
            "effectContract": [{"on": "BEGIN"}],
            "expectedTrace": [{"event": "dispatch"}],
            "expectedFinalState": {"phase": "ready"},
        }],
    }


class PublicValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.write("README.md", "[spec](docs/spec.md)\n")
        self.write("docs/spec.md", "draft\n")
        self.write("web/index.html", '<a href="../README.md">Home</a>\n')
        self.write("docs/specifications/conformance/application-cycle-v0.1.json", json.dumps(fixture()))

    def write(self, path: str, contents: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")
        return target

    def test_clean_public_repository(self) -> None:
        self.assertEqual([], validate_repository(self.root))

    def test_invalid_json_fails(self) -> None:
        self.write("docs/specifications/conformance/application-cycle-v0.1.json", "{broken")
        self.assertIn("invalid JSON", "\n".join(validate_repository(self.root)))

    def test_duplicate_ids_fail(self) -> None:
        candidate = fixture()
        candidate["scenarios"].append(candidate["scenarios"][0].copy())
        self.assertIn("duplicate scenario id", "\n".join(validate_fixture(candidate)))

    def test_bad_trace_and_missing_final_state_fail(self) -> None:
        candidate = fixture()
        candidate["scenarios"][0]["expectedTrace"] = [{"event": "unknown"}]
        candidate["scenarios"][0].pop("expectedFinalState")
        issues = "\n".join(validate_fixture(candidate))
        self.assertIn("unknown/missing event", issues)
        self.assertIn("expectedFinalState", issues)

    def test_missing_markdown_target_fails(self) -> None:
        self.write("README.md", "[missing](docs/absent.md)\n")
        self.assertIn("missing link target", "\n".join(validate_documents(self.root)))

    def test_missing_html_target_fails(self) -> None:
        self.write("web/index.html", '<img src="missing.png">\n')
        self.assertIn("missing link target", "\n".join(validate_documents(self.root)))

    def test_escaped_path_and_symlink_target_fail(self) -> None:
        self.write("README.md", "[escape](../secret.md)\n")
        self.assertIn("escapes repository", "\n".join(validate_documents(self.root)))
        (self.root / "secret-link.md").symlink_to(self.root.parent)
        self.write("README.md", "[escape](secret-link.md)\n")
        self.assertIn("escapes repository", "\n".join(validate_documents(self.root)))

    def test_inline_code_not_treated_as_link(self) -> None:
        tick = chr(96)
        self.write("README.md", f"{tick}[example](missing.md){tick} [actual](docs/spec.md)\n")
        self.assertEqual([], validate_documents(self.root))

    def test_four_space_indented_fence_does_not_mask_link(self) -> None:
        tick = chr(96)
        self.write("README.md", f"    {tick * 3}\n[broken](missing.md)\n")
        self.assertIn("missing link target", "\n".join(validate_documents(self.root)))

    def test_html_character_reference_cannot_hide_scheme(self) -> None:
        self.write("README.md", "[bad](javascript&colon;alert)\n")
        self.assertIn("unsupported URI scheme", "\n".join(validate_documents(self.root)))

    def test_empty_link_label_and_encoded_paths(self) -> None:
        self.write("README.md", "![](docs/nope.png)\n[](docs/spec.md)\n")
        self.assertIn("missing link target", "\n".join(validate_documents(self.root)))
        self.write("README.md", "[encoded](docs/%73pec.md)\n")
        self.assertEqual([], validate_documents(self.root))

    def test_missing_site_is_failure(self) -> None:
        (self.root / "web/index.html").unlink()
        self.assertIn("Missing public site", "\n".join(validate_documents(self.root)))


if __name__ == "__main__":
    unittest.main()
