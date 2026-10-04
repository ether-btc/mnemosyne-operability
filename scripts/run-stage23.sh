#!/bin/bash
cd /c/Users/kranl/bekko/bekko-decider
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" /c/Users/kranl/bekko/bekko-system-one/.venv/Scripts/python.exe -m bekko_system_one.training --config configs/stage23-17m-cpu.yaml > run-stage23.log 2>&1
echo STAGE23_DONE >> run-stage23.log
echo rc=$? >> run-stage23.log
