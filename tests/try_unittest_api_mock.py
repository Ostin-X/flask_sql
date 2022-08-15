# import json
from unittest.mock import Mock

json = Mock()
json.dumps({'a': 1})
# json.dumps({'a': 1})
# print(dir(json))
# print(json.dumps.call_args)
# print(json.dumps.call_count)
# print(json.method_calls)
# print(json.dumps.called)
#
# print(json.dumps.assert_called())
# print(json.dumps.assert_called_once())
# print(json.dumps.assert_called_with({'a': 1}))


def func(dict):
    for k, v in dict.items():
        print(f'print key = {k}, value = {v}')



json.dumps.side_effect = func

json.dumps({'a': 1})
