from core import choices


def test_choices():
    class MadeUp(choices.Choices):
        A = "a"
        B = "b"
        C = "c"

    expected_choices = (("A", "a"), ("B", "b"), ("C", "c"))
    expected_names = ("A", "B", "C")
    expected_values = ("A", "B", "C")
    expected_labels = ("a", "b", "c")
    expected_options = ({"value": "A", "text": "a"}, {"value": "B", "text": "b"}, {"value": "C", "text": "c"})
    expected_mapping = {"A": "a", "B": "b", "C": "c"}
    assert MadeUp.choices == expected_choices
    assert MadeUp.names == expected_names
    assert MadeUp.values == expected_values
    assert MadeUp.labels == expected_labels
    assert MadeUp.options == expected_options
    assert MadeUp.mapping == expected_mapping
