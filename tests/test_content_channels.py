from app.channels.content_channels import channel_status


def test_two_autonomous_channels_have_100_assistants_each():
    result = channel_status()
    assert result["total_dedicated_assistants"] == 200
    assert result["daily_long_videos"] == 2
    assert result["daily_shorts_or_reels_minimum"] == 2
    assert result["execution"] == "autonomous"


def test_publish_time_is_analytics_driven():
    result = channel_status()
    for channel in result["channels"]:
        assert channel["assistant_count"] == 100
        assert channel["daily_long_videos"] == 1
        assert channel["short_reels_per_video"] == 1
        assert channel["publish_time"]["strategy"] == "learn_from_channel_analytics"
