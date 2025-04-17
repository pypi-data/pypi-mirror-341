from . import _pywrap_coral

def get_runtime_version():
    return _pywrap_coral.GetRuntimeVersion()
