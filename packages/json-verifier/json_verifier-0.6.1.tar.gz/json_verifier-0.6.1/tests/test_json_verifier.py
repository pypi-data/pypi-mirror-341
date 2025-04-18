import pytest

from json_verifier import JsonVerifier


@pytest.fixture
def verifier():
    actual = {
        "metadata": {
            "name": "sandbox",
            "tags": ["scratch", "pre-production", "experimental"],
        }
    }
    return JsonVerifier(actual)


def test_expect_pass(verifier):
    with verifier:
        verifier.verify_value("metadata.name", "sandbox")
        verifier.verify_value("metadata.tags.0", "scratch")
        verifier.verify_value("metadata.tags.1", "pre-production")


def test_key_path_types(verifier):
    with verifier:
        verifier.verify_value(("metadata", "tags", 0), "scratch")  # tuple with int
        verifier.verify_value(("metadata", "name"), "sandbox")  # tuple
        verifier.verify_value(["metadata", "name"], "sandbox")  # list


@pytest.mark.parametrize(
    ("obj", "path", "expected"),
    [
        pytest.param({True: "is true"}, True, "is true", id="bool"),
        pytest.param(["foo", "bar"], 0, "foo", id="int"),
        pytest.param({1.1: "foo"}, 1.1, "foo", id="float"),
    ],
)
def test_key_path_simple_types(obj, path, expected):
    verifier = JsonVerifier(obj)
    with verifier:
        verifier.verify_value(path, expected)


def test_expect_fail(verifier):
    def do_failed_test():
        with verifier:
            verifier.verify_value("metadata.name", "staging")
            verifier.verify_value("metadata.description", "Team sandbox")
            verifier.verify_value("metadata.tags.0", "testing")
            verifier.verify_value("metadata.tags.3", "non-production")

    with pytest.raises(AssertionError):
        do_failed_test()


def test_verify_value(verifier):
    verifier.verify_value("metadata.name", "staging")
    verifier.verify_value("metadata.description", "Team sandbox")
    verifier.verify_value("metadata.tags.0", "testing")
    verifier.verify_value("metadata.tags.3", "non-production")

    assert verifier.errors == [
        "path='metadata.name', expected='staging', actual='sandbox'",
        "path='metadata.description', expected='Team sandbox', key error: 'description'",
        "path='metadata.tags.0', expected='testing', actual='scratch'",
        "path='metadata.tags.3', expected='non-production', index error: 3",
    ]

    with pytest.raises(AssertionError):
        verifier.tally()


def test_wrong_index_type(verifier):
    verifier.verify_value("metadata.tags.foo", "scratch")
    assert verifier.errors == [
        "path='metadata.tags.foo', expected='scratch', index is not int: 'foo'",
    ]

    with pytest.raises(AssertionError):
        verifier.tally()
