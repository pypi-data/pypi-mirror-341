from socketnest_python.socketnest import Socketnest
from unittest.mock import patch, MagicMock


def test_trigger_success():
    client = Socketnest(app_id="test_app", secret="test_secret")
    channel = "test-channel"
    event = "test-event"
    data = {"foo": "bar"}
    expected_url = "https://api.socketnest.com/trigger"
    expected_headers = {
        "x-app-id": "test_app",
        "x-secret": "test_secret",
        "Content-Type": "application/json"
    }
    expected_payload = {
        "channel": channel,
        "event": event,
        "data": data
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}

    with patch("requests.post", return_value=mock_response) as mock_post:
        response = client.trigger(channel, event, data)
        assert response.status_code == 200
        assert response.json() == {"success": True}
        mock_post.assert_called_once_with(
            expected_url, json=expected_payload, headers=expected_headers
        )
