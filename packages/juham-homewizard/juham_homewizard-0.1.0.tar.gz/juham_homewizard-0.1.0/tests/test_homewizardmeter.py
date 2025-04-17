import unittest
from unittest.mock import MagicMock, patch
import json
from typing import Any, Dict
from masterpiece.mqtt import MqttMsg

from juham_homewizard.homewizardwatermeter import HomeWizardWaterMeter
from juham_homewizard.homewizardwatermeter import HomeWizardWaterMeterThread


class TestHomeWizardWaterMeterThread(unittest.TestCase):

    @patch("masterpiece.Mqtt")
    @patch("juham_homewizard.homewizardwatermeter.timestamp", return_value=1234567890)
    def test_process_data(self, mock_timestamp: float, mock_mqtt) -> None:
        client = mock_mqtt.return_value
        thread = HomeWizardWaterMeterThread(client)
        thread.init("test/topic", "http://test.url", 60)

        mock_data = MagicMock()
        mock_data.json.return_value = {"active_liter_lpm": "5.5", "total_liter": "1000"}

        thread.process_data(mock_data)
        expected_payload = json.dumps(
            {"active_liter_lpm": 5.5, "total_liter": 1000.0, "ts": 1234567890}
        )

        client.publish.assert_called_once_with("test/topic", expected_payload, 0, False)


class TestHomeWizardWaterMeter(unittest.TestCase):

    @patch("masterpiece.MasterPiece.instantiate")
    def test_run(self, mock_instantiate) -> None:
        mock_worker = MagicMock()
        mock_instantiate.return_value = mock_worker  # Mock the thread object

        sensor = HomeWizardWaterMeter("sensor", "/watermeter", "http://test.url", 30)
        sensor.run()  # Triggers the superclass run() method

        print("instantiate() calls:", mock_instantiate.call_args_list)
        print("start() call count:", mock_worker.start.call_count)  # Instead of run()

        assert mock_worker.start.call_count == 1

    def test_to_dict(self) -> None:
        sensor = HomeWizardWaterMeter("sensor", "test/topic", "http://test.url", 30)
        expected_dict = {
            "_class": "HomeWizardWaterMeter",
            "_version": 0,
            "_object": {
                "name": "sensor",
                "payload": None,
            },
            "_base": {},
            "_homewizardwatermeter": {
                "topic": "/watermeter",
                "url": "http://test.url",
                "interval": 30,
            },
        }

        actual_dict: Dict[str, Any] = sensor.to_dict()
        self.assertEqual(actual_dict, expected_dict)

    def test_from_dict(self) -> None:
        sensor = HomeWizardWaterMeter()
        data = {
            "_class": "HomeWizardWaterMeter",
            "_version": 0,
            "_object": {"name": "sensor", "payload": None},
            "_base": {},
            "_homewizardwatermeter": {
                "topic": "/watermeter",
                "url": "http://test.url",
                "interval": 30,
            },
        }
        sensor.from_dict(data)
        self.assertEqual(sensor.sensor_topic, "/watermeter")
        self.assertEqual(sensor.url, "http://test.url")
        self.assertEqual(sensor.update_interval, 30)

    def test_on_message(self) -> None:
        sensor = HomeWizardWaterMeter("sensor", "test/topic", "http://test.url", 30)
        with patch.object(sensor, "on_sensor", MagicMock()) as mock_on_sensor:
            # Use a mock object instead of directly instantiating MqttMsg
            mock_msg = MagicMock(spec=MqttMsg)
            mock_msg.topic = "/watermeter"
            mock_msg.payload = json.dumps({"test": "data"}).encode()

            sensor.on_message(None, None, mock_msg)
            mock_on_sensor.assert_called_once_with({"test": "data"})


if __name__ == "__main__":
    unittest.main()
