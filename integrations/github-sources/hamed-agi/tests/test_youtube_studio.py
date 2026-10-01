from app.youtube_studio import youtube_studio


def test_three_channels_are_configured():
    channels = youtube_studio.channels()
    assert len(channels) == 3
    assert {c["channel_id"] for c in channels} == {"kids", "islamic_english", "lumíkids"}


def test_lumikids_channel_url_and_plan():
    channel = next(c for c in youtube_studio.channels() if c["channel_id"] == "lumíkids")
    assert channel["name"] == "LumiKids"
    assert channel["url"] == "https://www.youtube.com/@LumiKidsTV-b3e"
    plan = youtube_studio.create_daily_plan("lumíkids", "Colors", target_words=["red", "blue", "yellow"])
    assert plan.channel_id == "lumíkids"
    assert "red" in plan.target_words
    assert "trend_and_competitor_research" in plan.production_steps


def test_kids_daily_plan():
    plan = youtube_studio.create_daily_plan("kids", "Animals", target_words=["dog", "cat", "bird"])
    assert plan.channel_id == "kids"
    assert "dog" in plan.target_words
    assert "trend_and_competitor_research" in plan.production_steps


def test_islamic_channel_requires_source_verification_workflow():
    plan = youtube_studio.create_daily_plan("islamic_english", "What is the Quran?")
    assert "source_or_lyrics_verification" in plan.production_steps
    assert "primary sources" in plan.story_outline[1]


def test_invalid_channel_rejected():
    try:
        youtube_studio.create_daily_plan("unknown", "test")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown channel must be rejected")
