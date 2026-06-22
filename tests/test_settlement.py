import pytest
from settlement import SettlementOperator, SettlementMessage

def test_send_settlement_message():
    operator = SettlementOperator("example_network")
    message = SettlementMessage(amount=100.0, recipient="example_recipient")
    result = operator.send_settlement_message(message)
    assert result

def test_trigger_settlement_success():
    operator = SettlementOperator("example_network")
    message = SettlementMessage(amount=100.0, recipient="example_recipient")
    result = operator.trigger_settlement(message)
    assert result["status"] == "success"
    assert "acknowledgement" in result

def test_trigger_settlement_failure():
    operator = SettlementOperator("example_network")
    operator.send_settlement_message = lambda x: False
    message = SettlementMessage(amount=100.0, recipient="example_recipient")
    result = operator.trigger_settlement(message)
    assert result["status"] == "failed"

def test_trigger_settlement_retry():
    operator = SettlementOperator("example_network")
    operator.send_settlement_message = lambda x: False
    operator.max_retries = 1
    message = SettlementMessage(amount=100.0, recipient="example_recipient")
    result = operator.trigger_settlement(message)
    assert result["status"] == "failed"

def test_get_acknowledgement():
    operator = SettlementOperator("example_network")
    acknowledgement = operator.get_acknowledgement()
    assert acknowledgement == "Acknowledgement received"
