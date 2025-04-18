from hatchling.plugin import hookimpl
from nuitka_hatch2.plugin import NuitkaBuildHook

@hookimpl
def hatch_register_build_hook():
    return NuitkaBuildHook