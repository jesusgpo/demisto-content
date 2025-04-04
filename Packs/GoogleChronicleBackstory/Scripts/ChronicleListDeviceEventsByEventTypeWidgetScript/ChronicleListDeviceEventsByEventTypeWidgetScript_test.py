from unittest.mock import patch

import ChronicleListDeviceEventsByEventTypeWidgetScript
import demistomock as demisto

INDICATOR_DATA = {"indicator": {"CustomFields": {"chronicleassetsummary": []}}}
GENERIC_EVENT = "Generic Event"
NETWORK_HTTP = "Network HTTP"
NETWORK_CONNECTION = "Network Connection"
USER_LOGIN = "User Login"


def test_main_success(mocker):
    """
    When main function is called, extract_list_of_events_from_indicator should be called.
    """

    mocker.patch.object(demisto, "args", return_value=INDICATOR_DATA)
    mocker.patch.object(
        ChronicleListDeviceEventsByEventTypeWidgetScript, "extract_list_of_events_from_indicator", return_value=""
    )
    ChronicleListDeviceEventsByEventTypeWidgetScript.main()
    assert ChronicleListDeviceEventsByEventTypeWidgetScript.extract_list_of_events_from_indicator.called


@patch("ChronicleListDeviceEventsByEventTypeWidgetScript.return_error")
def test_main_failure(mock_return_error, capfd, mocker):
    """
    When main function gets some exception then valid message should be printed.
    """

    mocker.patch.object(demisto, "args", return_value=INDICATOR_DATA)
    mocker.patch.object(
        ChronicleListDeviceEventsByEventTypeWidgetScript, "extract_list_of_events_from_indicator", side_effect=Exception
    )
    with capfd.disabled():
        ChronicleListDeviceEventsByEventTypeWidgetScript.main()

    mock_return_error.assert_called_once_with("Could not load widget:\n")


def test_extract_list_of_events_from_indicator_when_no_events_are_fetched():
    """
    When no events are fetched, extract_list_of_events_from_indicator should return pie chart accordingly.
    """

    actual_pie_chart_entry_type = ChronicleListDeviceEventsByEventTypeWidgetScript.extract_list_of_events_from_indicator(
        INDICATOR_DATA
    )
    expected_pie_chart_entry_type = {
        "Type": 17,
        "ContentsFormat": "pie",
        "Contents": {
            "stats": [
                {"data": [0], "groups": None, "name": GENERIC_EVENT, "label": GENERIC_EVENT, "color": "green"},
                {"data": [0], "groups": None, "name": NETWORK_HTTP, "label": NETWORK_HTTP, "color": "red"},
                {"data": [0], "groups": None, "name": NETWORK_CONNECTION, "label": NETWORK_CONNECTION, "color": "blue"},
                {"data": [0], "groups": None, "name": USER_LOGIN, "label": USER_LOGIN, "color": "orange"},
                {"data": [0], "groups": None, "name": "Others", "label": "Others", "color": "grey"},
            ],
            "params": {"layout": "vertical"},
        },
    }
    assert expected_pie_chart_entry_type == actual_pie_chart_entry_type


def test_extract_list_of_events_from_indicator_when_events_are_fetched():
    """
    When some events are fetched, extract_list_of_events_from_indicator should return pie chart accordingly.
    """
    indicator_data = {
        "CustomFields": {
            "chronicleassetsummary": [
                {"eventtype": "GENERIC_EVENT"},
                {"eventtype": "GENERIC_EVENT"},
                {"eventtype": "NETWORK_HTTP"},
                {"eventtype": "NETWORK_CONNECTION"},
                {"eventtype": "NETWORK_DNS"},
                {"eventtype": "USER_LOGIN"},
            ]
        }
    }
    actual_pie_chart_entry_type = ChronicleListDeviceEventsByEventTypeWidgetScript.extract_list_of_events_from_indicator(
        indicator_data
    )
    expected_pie_chart_entry_type = {
        "Type": 17,
        "ContentsFormat": "pie",
        "Contents": {
            "stats": [
                {"data": [2], "groups": None, "name": GENERIC_EVENT, "label": GENERIC_EVENT, "color": "green"},
                {"data": [1], "groups": None, "name": NETWORK_HTTP, "label": NETWORK_HTTP, "color": "red"},
                {"data": [1], "groups": None, "name": NETWORK_CONNECTION, "label": NETWORK_CONNECTION, "color": "blue"},
                {"data": [1], "groups": None, "name": USER_LOGIN, "label": USER_LOGIN, "color": "orange"},
                {"data": [1], "groups": None, "name": "Others", "label": "Others", "color": "grey"},
            ],
            "params": {"layout": "vertical"},
        },
    }
    assert expected_pie_chart_entry_type == actual_pie_chart_entry_type
