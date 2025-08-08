from PyInstaller.utils.hooks import collect_submodules

# The winshell module implicitly imports from pywin32, so we need to make sure
# PyInstaller finds all the necessary hidden modules for both.
hiddenimports = collect_submodules('winshell') + collect_submodules('pywin32')
