import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_repo_files_exist():
    for p in ["app.py","utils.py","requirements.txt","widget.html","rebuild_index_v3.py"]:
        assert (ROOT/p).exists(), f"Missing {p}"

def test_data_contract_present():
    assert (ROOT/"data"/"README_DATA.md").exists()
    assert (ROOT/"data"/".gitkeep").exists()

def test_gitignore_safety():
    gi = (ROOT/".gitignore").read_text(encoding="utf-8")
    assert re.search(r"^\.env(\b|$)", gi, re.M)
    assert re.search(r"^data/\*", gi, re.M)
    assert re.search(r"^clm_index\*\.index", gi, re.M)
    assert re.search(r"^clm_metadata\*\.json", gi, re.M)

def test_widget_has_iframe_hint():
    html = (ROOT/"widget.html").read_text(encoding="utf-8")
    assert "iframe" in html.lower()
