from data_gen.generator import DataGenerator

def test_generator():

    data = DataGenerator()
    record = data.generate_data()

    assert "user_id" in record
    assert "item_id" in record
    assert record["interaction_type"] in ['click', 'view', 'purchase']