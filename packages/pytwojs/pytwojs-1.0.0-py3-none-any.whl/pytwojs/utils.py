import os
from ._program import PROGRAM, FLAGS


def get_node_env():
    node = os.environ.get('NODE_PATH') if os.environ.get('NODE_PATH') else os.environ.get('NODE')
    if not node:
        return "node"
    return node


def make_cmd():
    node = get_node_env()
    return [node, FLAGS, PROGRAM]
