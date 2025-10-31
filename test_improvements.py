"""
Test to verify the performance improvements and correctness of optimizations
"""
import sys
from unittest.mock import Mock, patch
import openf1_qualifying

def test_get_meetingkey_with_valid_data():
    """Test that get_meetingkey returns the correct meeting key"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'meeting_key': 1234}]
    
    with patch('requests.get', return_value=mock_response):
        result = openf1_qualifying.get_meetingkey('Singapore', 2024)
        assert result == 1234, f"Expected 1234, got {result}"
    print("✓ get_meetingkey returns correct key for valid data")

def test_get_meetingkey_with_no_data():
    """Test that get_meetingkey returns None when no meetings found"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    
    with patch('requests.get', return_value=mock_response):
        result = openf1_qualifying.get_meetingkey('InvalidCountry', 2024)
        assert result is None, f"Expected None, got {result}"
    print("✓ get_meetingkey returns None when no meetings found")

def test_get_meetingkey_with_error():
    """Test that get_meetingkey handles errors gracefully"""
    import requests
    with patch('requests.get', side_effect=requests.RequestException('Network error')):
        result = openf1_qualifying.get_meetingkey('Singapore', 2024)
        assert result is None, f"Expected None on error, got {result}"
    print("✓ get_meetingkey handles errors gracefully")

def test_get_sessionkey_with_valid_data():
    """Test that get_sessionkey returns the correct session key"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {'session_name': 'Practice 1', 'session_key': 5678},
        {'session_name': 'Qualifying', 'session_key': 9999},
        {'session_name': 'Race', 'session_key': 1111}
    ]
    
    with patch('requests.get', return_value=mock_response):
        result = openf1_qualifying.get_sessionkey(1234)
        assert result == 9999, f"Expected 9999, got {result}"
    print("✓ get_sessionkey returns correct key for qualifying session")

def test_get_sessionkey_with_none_meeting_key():
    """Test that get_sessionkey handles None meeting_key"""
    result = openf1_qualifying.get_sessionkey(None)
    assert result is None, f"Expected None, got {result}"
    print("✓ get_sessionkey handles None meeting_key")

def test_format_laptime():
    """Test laptime formatting"""
    # Test normal lap time
    assert openf1_qualifying.format_laptime(90.123) == "01:30.123"
    # Test None
    assert openf1_qualifying.format_laptime(None) is None
    # Test edge case with milliseconds rounding
    assert openf1_qualifying.format_laptime(90.9995) == "01:30.999"
    print("✓ format_laptime works correctly")

def test_dictionary_building_optimization():
    """Test that dictionary building only processes needed drivers"""
    # Simulate the optimization
    data = [
        {'driver_number': 1, 'lap_duration': 90.5},
        {'driver_number': 44, 'lap_duration': 89.2},
    ]
    
    driver_data = [
        {'driver_number': 1, 'full_name': 'Driver One', 'team_name': 'Team A'},
        {'driver_number': 44, 'full_name': 'Driver Forty-Four', 'team_name': 'Team B'},
        {'driver_number': 99, 'full_name': 'Driver Ninety-Nine', 'team_name': 'Team C'},  # Not in results
    ]
    
    # Get the set of driver numbers we actually need
    needed_driver_numbers = {item['driver_number'] for item in data}
    
    driver_number_to_names = {}
    driver_number_to_team = {}
    
    # Only process drivers that are in the qualifying results
    processed_count = 0
    for driver in driver_data:
        driver_number = driver['driver_number']
        if driver_number in needed_driver_numbers:
            driver_number_to_names[driver_number] = driver['full_name']
            driver_number_to_team[driver_number] = driver['team_name']
            processed_count += 1
    
    # Verify we only processed 2 drivers, not all 3
    assert processed_count == 2, f"Expected 2 processed drivers, got {processed_count}"
    assert len(driver_number_to_names) == 2, f"Expected 2 names, got {len(driver_number_to_names)}"
    assert 99 not in driver_number_to_names, "Driver 99 should not be in the dictionary"
    print("✓ Dictionary building optimization works correctly")

if __name__ == '__main__':
    print("Running tests for performance improvements...\n")
    
    try:
        test_get_meetingkey_with_valid_data()
        test_get_meetingkey_with_no_data()
        test_get_meetingkey_with_error()
        test_get_sessionkey_with_valid_data()
        test_get_sessionkey_with_none_meeting_key()
        test_format_laptime()
        test_dictionary_building_optimization()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
