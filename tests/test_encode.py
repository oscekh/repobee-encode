from _repobee import plugin

from repobee_encode import encode


def test_register():
    """Just test that there is no crash"""
    plugin.register_plugins([encode])
