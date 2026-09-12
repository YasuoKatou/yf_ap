#!/bin/bash
source ./env.sh
dist_path=~/storage/downloads/yfinance/chart/
rm -rf $dist_path
mkdir $dist_path
mv ${graph_path}/*.png $dist_path
