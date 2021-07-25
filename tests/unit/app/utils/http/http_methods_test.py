from src.app.utils.http.http_methods import get_methods_list, POST, GET, PUT, DELETE, HEAD, CONNECT, OPTIONS, TRACE, \
    PATCH


def test_get_methods_list_return_list_with_all_defined_http_methods():
    actual = get_methods_list()
    assert len(actual) == 9
    assert POST in actual
    assert GET in actual
    assert PUT in actual
    assert DELETE in actual
    assert HEAD in actual
    assert CONNECT in actual
    assert OPTIONS in actual
    assert TRACE in actual
    assert PATCH in actual
