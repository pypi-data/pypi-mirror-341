from jyelib.array import get_list_repeat

def test_get_list_repeat():
    assert get_list_repeat([1, 2, 3, 4, 5]) == []
    assert get_list_repeat([1, 2, 3, 4, 5, 3, 1]) == [1, 3]