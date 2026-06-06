def test_search_intent():
    parser = IntentParser()

    intent, arg = parser.parse(
        "search airbus a350"
    )

    assert intent == "search"
    assert arg == "airbus a350"
  
def test_youtube_intent():
    parser = IntentParser()

    intent, arg = parser.parse(
        "youtube cockpit landing"
    )

    assert intent == "youtube"

def test_weather_intent():
    parser = IntentParser()

    intent, arg = parser.parse(
        "weather doha"
    )

    assert intent == "weather"
    assert arg == "doha"
