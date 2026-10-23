"""CI gate for the green checks in the harness and flowable tables.

build_site.py shows a green check on a lesson only when scripts/lesson_status.py can back it.
These tests run the same code, so a lesson cannot keep a check once its script breaks.

Run:  python3 -m pytest tests -q
"""
import pytest

import lesson_status

RECORDS = lesson_status.collect(run=False)
OFFLINE = [(r["rel"], s) for r in RECORDS.values() for s in r["scripts"] if s["kind"] == "offline"]
XML = [(r["rel"], x) for r in RECORDS.values() for x in r["xml"]]


@pytest.mark.parametrize("lesson,script", OFFLINE, ids=[f"{l.split('phases/')[1]}/{s['name']}" for l, s in OFFLINE])
def test_offline_script_exits_zero(lesson, script):
    result = lesson_status.run_script(script["path"])
    if result["rc"] != 0 and script["networked"] and lesson_status.SERVICE_ERRORS.search(result["out"]):
        pytest.skip("needs a live service")
    assert result["rc"] == 0, result["out"]


@pytest.mark.parametrize("lesson,xml", XML, ids=[f"{l.split('phases/')[1]}/{x['name']}" for l, x in XML])
def test_xml_artifact_parses(lesson, xml):
    assert xml["ok"], f"{xml['rel']} is not well-formed XML"


def test_every_build_lesson_has_evidence_or_says_so():
    """A Build lesson with no code must show Spec only; it may never show a green check."""
    for rel, rec in RECORDS.items():
        if rec["state"] in lesson_status.GREEN:
            assert rec["scripts"] or rec["xml"], rel
