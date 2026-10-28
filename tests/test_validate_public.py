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
            "reducerContract": [{"on": "BEGIN", "stateChange": {"phase": "ready"}}],
            "effectContract": [{"on": "BEGIN", "action": "none"}],
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


    def test_outside_site_symlink_is_rejected(self) -> None:
        site = self.root / "web/index.html"
        site.unlink()
        outside = self.root.parent / (self.root.name + "-outside-site.html")
        outside.write_text('<a href="missing.html">outside</a>', encoding="utf-8")
        self.addCleanup(outside.unlink)
        site.symlink_to(outside)
        self.assertIn("escapes repository", "\n".join(validate_documents(self.root)))

    def test_reference_style_targets_and_undefined_labels(self) -> None:
        self.write("README.md", "[first][known] [second][absent]\n[known]: docs/missing.md\n")
        result = "\n".join(validate_documents(self.root))
        self.assertIn("missing link target", result)
        self.assertIn("undefined reference label: absent", result)

    def test_valid_reference_style_links_and_collapsed_form(self) -> None:
        self.write("README.md", "[spec][Known] [Known][]\n[known]: docs/spec.md\n")
        self.assertEqual([], validate_documents(self.root))

    def test_reference_definition_inside_code_is_ignored(self) -> None:
        tick = chr(96)
        self.write("README.md", f"{tick * 3}\n[ref]: docs/absent.md\n{tick * 3}\n")
        self.assertEqual([], validate_documents(self.root))

    def test_invalid_contract_array_entries_are_rejected(self) -> None:
        candidate = fixture()
        scenario = candidate["scenarios"][0]
        scenario["intents"] = [None]
        scenario["reducerContract"] = ["malformed"]
        scenario["effectContract"] = [{}]
        result = "\n".join(validate_fixture(candidate))
        self.assertIn("intents[0] requires object", result)
        self.assertIn("reducerContract[0] requires object", result)
        self.assertIn("effectContract[0] requires object", result)

    def test_missing_contract_discriminators_fail(self) -> None:
        candidate = fixture()
        scenario = candidate["scenarios"][0]
        scenario["intents"] = [{}]
        scenario["reducerContract"] = [{"on": "BEGIN"}]
        scenario["effectContract"] = [{"on": "BEGIN"}]
        result = "\n".join(validate_fixture(candidate))
        self.assertIn("nonempty type", result)
        self.assertIn("missing stateChange", result)
        self.assertIn("missing action", result)

    def test_required_fixture_validated_behind_in_repository_directory_symlink(self) -> None:
        # Recursive discovery sees the physical JSON, but not its path through
        # the required conformance-directory symlink. It must not skip validation.
        old = self.root / "docs/specifications/conformance"
        (old / "application-cycle-v0.1.json").unlink()
        old.rmdir()
        real = self.root / "docs/synthetic-contracts"
        real.mkdir(parents=True)
        (real / "application-cycle-v0.1.json").write_text("{}", encoding="utf-8")
        old.symlink_to(real, target_is_directory=True)
        self.assertIn("schemaVersion must be", "\\n".join(validate_repository(self.root)))

    def test_multiline_reference_definition_target_is_accepted(self) -> None:
        self.write("README.md", "[spec][ref]\\n[ref]:\\n  docs/spec.md\\n")
        self.assertEqual([], validate_documents(self.root))

    def test_multiline_reference_definition_broken_target_is_rejected(self) -> None:
        self.write("README.md", "[spec][ref]\\n[ref]:\\n  docs/absent.md\\n")
        self.assertIn("missing link target", "\\n".join(validate_documents(self.root)))

    def test_reference_definition_without_continuation_is_undefined(self) -> None:
        self.write("README.md", "[spec][ref]\\n[ref]:\\n\\nNext paragraph.\\n")
        self.assertIn("undefined reference label", "\\n".join(validate_documents(self.root)))

    def test_symlinked_json_cannot_escape_checkout(self) -> None:
        target = self.root / "docs/specifications/conformance/application-cycle-v0.1.json"
        target.unlink()
        outside = self.root.parent / (self.root.name + "-outside-fixture.json")
        outside.write_text(json.dumps(fixture()), encoding="utf-8")
        self.addCleanup(outside.unlink)
        target.symlink_to(outside)
        self.assertIn("JSON file escapes repository", "\n".join(validate_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
