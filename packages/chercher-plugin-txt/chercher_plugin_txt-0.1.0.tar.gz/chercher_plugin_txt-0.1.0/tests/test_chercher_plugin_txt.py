from chercher_plugin_txt import ingest
from chercher import Document

CONTENT = "Hello, world"


def test_valid_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT

    uri = p.as_uri()
    documents = ingest(uri=uri)
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.uri == uri
        assert doc.body == CONTENT
