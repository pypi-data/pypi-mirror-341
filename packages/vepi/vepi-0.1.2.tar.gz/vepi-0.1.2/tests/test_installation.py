"""
Test script to verify the installation and basic functionality of the vepi package.
"""

from vepi import VenaETL
import pandas as pd

try:
    from test_config import TEST_CONFIG, TEST_DATA
    USE_TEST_CONFIG = True
except ImportError:
    print("No test_config.py found. Using dummy values.")
    USE_TEST_CONFIG = False
    TEST_CONFIG = {
        'hub': 'test.venasolutions.com',
        'api_user': 'test_user',
        'api_key': 'test_key_123',
        'template_id': 'template_123'
    }
    TEST_DATA = {
        'model_id': 'test-model',
        'period': '2024-01',
        'value': 100
    }

def test_installation():
    """Test basic package installation and class instantiation."""
    try:
        etl = VenaETL(
            hub=TEST_CONFIG['hub'],
            api_user=TEST_CONFIG['api_user'],
            api_key=TEST_CONFIG['api_key'],
            template_id=TEST_CONFIG['template_id']
        )
        print("✓ VenaETL instantiated successfully!")
        return etl
    except Exception as e:
        print(f"✗ Error instantiating VenaETL: {e}")
        return None

def test_data_upload(etl):
    """Test the data upload functionality."""
    if etl is None:
        print("✗ Skipping data upload test (VenaETL not initialized)")
        return

    # Create a sample DataFrame
    df = pd.DataFrame({
        "ModelId": [TEST_DATA['model_id']],
        "Value": [TEST_DATA['value']],
        "Period": [TEST_DATA['period']]
    })

    print("\nTesting start_with_data method:")
    try:
        etl.start_with_data(df)
        print("✓ start_with_data ran successfully!")
    except Exception as e:
        print(f"✗ Error running start_with_data: {e}")

if __name__ == "__main__":
    print("Running Vepi Installation Tests")
    print("=" * 30)
    print(f"Using {'actual' if USE_TEST_CONFIG else 'dummy'} configuration")
    print("-" * 30)
    
    etl = test_installation()
    test_data_upload(etl)
    
    print("\nTest completed!")