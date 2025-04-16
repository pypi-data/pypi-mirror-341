"""Basic tests for the Argus package."""

import pytest
from argus.core import WiFiMonitor


def test_argus_init():
    """Test that the WiFiMonitor class can be initialized."""
    monitor = WiFiMonitor()
    assert monitor.check_interval == 300
    assert monitor.log_file == "argus.csv"
    assert monitor.output_file == "argus_report.png"

    # Test with custom parameters
    custom_monitor = WiFiMonitor(
        check_interval=600, log_file="custom_log.csv", output_file="custom_report.png"
    )
    assert custom_monitor.check_interval == 600
    assert custom_monitor.log_file == "custom_log.csv"
    assert custom_monitor.output_file == "custom_report.png"
