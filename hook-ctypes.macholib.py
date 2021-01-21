from PyInstaller.utils.hooks import copy_metadata, collect_submodules
hiddenimports = collect_submodules('eth_hash.backends')
