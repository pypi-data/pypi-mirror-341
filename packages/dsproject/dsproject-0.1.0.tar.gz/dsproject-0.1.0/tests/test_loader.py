from dsproject.data_loader import load_data

def test_data_loader():
    df = load_data()
    assert df is not None
    assert not df.empty
