from scripts.asthetics.map import Map
import pandas as pd

test_map = Map()


def test_load_map():
    # Arrange
    map_path = "data/maps/test.txt"

    # Act
    map_loaded = test_map.load_map(map_path)

    # Assert
    assert map_loaded != []


def test_prepare_map():
    # Arrange
    map_path = "data/maps/test.txt"

    # Act
    test_map.prepare_map(map_path=map_path)

    # Assert
    assert len(test_map.tiles) == 9
    assert isinstance(test_map.tiles, pd.DataFrame)
