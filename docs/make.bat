@ECHO OFF
pushd %~dp0
sphinx-build -M html source _build %*
popd