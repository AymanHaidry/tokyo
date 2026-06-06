def test_google_search_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_search("airbus a350")

assert len(opened) == 1
assert "google.com/search" in opened[0]
assert "airbus" in opened[0]
