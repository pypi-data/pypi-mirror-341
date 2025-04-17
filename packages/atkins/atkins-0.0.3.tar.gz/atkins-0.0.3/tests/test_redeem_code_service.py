import pytest
from datetime import datetime, UTC
from atkins.services.redeem_code import RedeemCodeService, insert_dashes


@pytest.fixture
def redeem_code_service(db):
    service = RedeemCodeService(db)
    service.create_collections()
    service.build_index()
    return service


def test_insert_dashes():
    assert insert_dashes("12345678") == "1234-5678"
    assert insert_dashes("123456789") == "1234-5678-9"
    assert insert_dashes("") == ""


def test_generate_secure_code():
    code = RedeemCodeService.generate_secure_code()
    assert len(code.replace("-", "")) == 32  # 16 bytes = 32 hex chars
    assert "-" in code
    assert len(code.split("-")) == 8  # 32 chars / 4 = 8 segments


def test_create_code(redeem_code_service):
    code = "TEST-1234-5678"
    code_type = "premium_membership"
    
    # Create code
    created_code = redeem_code_service.create_code(code, code_type)
    assert created_code == code
    
    # Verify code exists
    code_record = redeem_code_service.get_code(code)
    assert code_record is not None
    assert code_record["code"] == code
    assert code_record["code_type"] == code_type
    assert code_record["used"] is False
    assert code_record["status"] == "issued"
    assert isinstance(code_record["createdAt"], datetime)
    assert code_record["request"] is None
    assert code_record["response"] is None
    assert code_record["error"] is None


def test_create_codes(redeem_code_service):
    codes = ["TEST-1234-5678", "TEST-8765-4321", "TEST-1111-2222"]
    code_type = "premium_membership"
    
    # Create multiple codes
    created_docs = redeem_code_service.create_codes(codes, code_type)
    
    # Verify all codes were created
    assert len(created_docs) == len(codes)
    
    # Verify each code exists and has correct fields
    for code in codes:
        code_record = redeem_code_service.get_code(code)
        assert code_record is not None
        assert code_record["code"] == code
        assert code_record["code_type"] == code_type
        assert code_record["used"] is False
        assert code_record["status"] == "issued"
        assert isinstance(code_record["createdAt"], datetime)
        assert code_record["request"] is None
        assert code_record["response"] is None
        assert code_record["error"] is None


def test_create_codes_duplicate(redeem_code_service):
    codes = ["TEST-1234-5678", "TEST-1234-5678"]  # Duplicate code
    code_type = "premium_membership"
    
    # Try to create codes with duplicates
    with pytest.raises(Exception):  # Should raise duplicate key error
        redeem_code_service.create_codes(codes, code_type)


def test_create_codes_empty_list(redeem_code_service):
    code_type = "premium_membership"
    # Create empty list of codes
    created_docs = redeem_code_service.create_codes([], code_type)
    assert len(created_docs) == 0


def test_start_processing_code(redeem_code_service):
    code = "TEST-1234-5678"
    code_type = "premium_membership"
    request = {"type": "test", "value": 100}
    
    # Create code
    redeem_code_service.create_code(code, code_type)
    
    # Start processing
    assert redeem_code_service.start_processing_code(code, request) is True
    
    # Verify processing state
    code_record = redeem_code_service.get_code(code)
    assert code_record["status"] == "processing"
    assert code_record["request"] == request
    assert isinstance(code_record["updatedAt"], datetime)


def test_mark_processing_failed(redeem_code_service):
    code = "TEST-1234-5678"
    code_type = "premium_membership"
    error_msg = {"message": "Test error", "code": "TEST_ERROR"}
    
    # Create code and start processing
    redeem_code_service.create_code(code, code_type)
    redeem_code_service.start_processing_code(code, {"type": "test"})
    
    # Mark as failed
    assert redeem_code_service.mark_processing_failed(code, error_msg) is True
    
    # Verify failed state
    code_record = redeem_code_service.get_code(code)
    assert code_record["status"] == "error"
    assert code_record["error"] == error_msg
    assert isinstance(code_record["updatedAt"], datetime)


def test_mark_processing_done(redeem_code_service):
    code = "TEST-1234-5678"
    code_type = "premium_membership"
    response = {"success": True, "message": "Test completed"}
    
    # Create code and start processing
    redeem_code_service.create_code(code, code_type)
    redeem_code_service.start_processing_code(code, {"type": "test"})
    
    # Mark as done
    assert redeem_code_service.mark_processing_done(code, response) is True
    
    # Verify completed state
    code_record = redeem_code_service.get_code(code)
    assert code_record["status"] == "used"
    assert code_record["response"] == response
    assert isinstance(code_record["updatedAt"], datetime)


def test_get_nonexistent_code(redeem_code_service):
    code = "NONEXISTENT-CODE"
    code_record = redeem_code_service.get_code(code)
    assert code_record is None


def test_unique_code_constraint(redeem_code_service):
    code = "TEST-1234-5678"
    code_type = "premium_membership"
    
    # Create code
    redeem_code_service.create_code(code, code_type)
    
    # Try to create same code again
    with pytest.raises(Exception):  # Should raise duplicate key error
        redeem_code_service.create_code(code, code_type) 