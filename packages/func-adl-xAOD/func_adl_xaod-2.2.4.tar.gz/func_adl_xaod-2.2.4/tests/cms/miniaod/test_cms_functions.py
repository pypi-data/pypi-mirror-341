from func_adl_xAOD.cms.miniaod import isNonnull
from tests.cms.miniaod.utils import cms_miniaod_dataset


def test_isnonnull_call():
    r = cms_miniaod_dataset().Select(lambda e: isNonnull(e)).value()
    vs = r.QueryVisitor._gc._class_vars
    assert 1 == len(vs)
    assert "bool" == str(vs[0].cpp_type())
