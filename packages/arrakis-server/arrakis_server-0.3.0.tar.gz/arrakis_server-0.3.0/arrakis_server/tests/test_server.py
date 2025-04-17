import pytest
from arrakis.constants import DEFAULT_MATCH
from arrakis.flight import RequestType, RequestValidator, create_command
from pyarrow import flight

from .. import constants, schemas
from ..server import parse_url


@pytest.fixture(scope="module")
def validator():
    return RequestValidator()


def test_parse_url():
    assert parse_url(None) is None
    assert parse_url("0") is None
    assert parse_url("-") is None
    assert parse_url("grpc://0.0.0.0:0") == ("0.0.0.0", 0)  # noqa S104
    assert parse_url("//0.0.0.0:0") == ("0.0.0.0", 0)  # noqa S104
    assert parse_url("0.0.0.0:0") == ("0.0.0.0", 0)  # noqa S104
    assert parse_url(("0.0.0.0", 0)) == ("0.0.0.0", 0)  # noqa S104
    assert parse_url(("12.234.434.3", 0)) == ("12.234.434.3", 0)
    assert parse_url(("12.234.434.3", 340)) == ("12.234.434.3", 340)
    assert parse_url("12.234.434.3:340") == ("12.234.434.3", 340)
    assert parse_url("//12.234.434.3:340") == ("12.234.434.3", 340)
    assert parse_url("grpc://12.234.434.3:340") == ("12.234.434.3", 340)
    # FIXME: would be nice to handle string port specifiers as well
    # assert parse_url(("12.234.434.3", "340")) == ("12.234.434.3", 340)


def test_count_flight_info(mock_server, validator):
    cmd = create_command(
        RequestType.Count,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
        validator=validator,
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.count()


def test_find_flight_info(mock_server, validator):
    cmd = create_command(
        RequestType.Find,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
        validator=validator,
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.find()


def test_describe_flight_info(mock_server, mock_channels, validator):
    channels = list(mock_channels.keys())
    cmd = create_command(RequestType.Describe, channels=channels, validator=validator)

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.describe()


def test_stream_flight_info(mock_server, mock_channels, validator):
    channels = list(mock_channels.keys())
    cmd = create_command(
        RequestType.Stream,
        channels=channels,
        start=None,
        end=None,
        validator=validator,
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.stream(list(mock_channels.values()))


def test_get_count(mock_server, validator):
    cmd = create_command(
        RequestType.Count,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
        validator=validator,
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(None, endpoint.ticket)


def test_get_find(mock_server, validator):
    cmd = create_command(
        RequestType.Find,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
        validator=validator,
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(None, endpoint.ticket)


def test_get_describe(mock_server, mock_channels, validator):
    channels = list(mock_channels.keys())
    cmd = create_command(RequestType.Describe, channels=channels, validator=validator)
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(None, endpoint.ticket)


def test_get_stream(mock_server, mock_channels, validator):
    channels = list(mock_channels.keys())
    cmd = create_command(
        RequestType.Stream,
        channels=channels,
        start=1187000000,
        end=1187001000,
        validator=validator,
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(None, endpoint.ticket)
