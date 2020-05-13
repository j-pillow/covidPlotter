#!/bin/bash

py3 py/covid.py -c $1
imgcat plots/*$1.png

