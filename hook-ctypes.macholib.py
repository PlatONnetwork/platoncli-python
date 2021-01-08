from PyInstaller.utils.hooks import copy_metadata,collect_submodules
datas = copy_metadata('platon_keyfile')
hiddenimports = collect_submodules('eth_hash.backends')
