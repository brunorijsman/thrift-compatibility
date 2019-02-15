#!/bin/bash

if [[ -z "${VIRTUAL_ENV}" ]]; then
  echo "Virtual environment not activated"
  exit 1
fi

echo ""
echo "***** Generate Python code for model *****"
thrift --out . --gen py model.thrift

echo ""
echo "***** Run Python compatibility test *****"
python compatibility.py 

echo ""
echo "***** Generate C++ code for model *****"
thrift --out . --gen cpp model.thrift

echo ""
echo "***** Compile C++ compatibility test *****"
clang++ \
  -std=c++11 \
  compatibility.cpp \
  model_types.cpp \
  -l thrift \
  -o compatibility

echo ""
echo "***** Run C++ compatibility test *****"
./compatibility
