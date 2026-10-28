"""Regression guard for Mermaid diagrams rendered by GitHub.

GitHub's Mermaid parser treats semicolons as statement separators, even when
introduced via HTML character references in sequence-diagram messages.
This is a targeted compatibility guard, not a substitute for renderer testing.
"""

from pathlib import Path
import re
import unittest


DOC = Path(__file__).resolve().parents[1] / "docs/architecture.md"
MERMAID_BLOCK = re.compile(r"^\x60{3}mermaid\s*\n([\s\S]*?)^\x60{3}\s*$", re.MULTILINE)


class ArchitectureMermaidTests(unittest.TestCase):
    def test_all_three_diagrams_use_github_mermaid_fences(self):
        document = DOC.read_text(encoding="utf-8")
        blocks = MERMAID_BLOCK.findall(document)
        self.assertEqual(len(blocks), 3)
        self.assertTrue(blocks[0].startswith("flowchart"))
        self.assertTrue(blocks[1].startswith("flowchart"))
        self.assertTrue(blocks[2].startswith("sequenceDiagram"))

    def test_sequence_messages_do_not_contain_statement_separators(self):
        sequence = MERMAID_BLOCK.findall(DOC.read_text(encoding="utf-8"))[2]
        for line in sequence.splitlines():
            if "->>" in line or "-->>" in line:
                message = line.partition(":")[2]
                self.assertTrue(message, f"Missing message: {line}")
                self.assertNotIn(";", message, f"Mermaid message may break at semicolon: {line}")
                self.assertNotRegex(message, r"&#\d+;", f"Encoded separator not allowed: {line}")
        self.assertIn("else Admission allowed", sequence)
        self.assertIn("end", sequence.splitlines())


if __name__ == "__main__":
    unittest.main()
