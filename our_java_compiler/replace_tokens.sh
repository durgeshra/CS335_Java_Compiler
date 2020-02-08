#!/bin/bash

IFS=','
while read old new; do
    echo "$old $new"
    sed -i "s/$old/$new/g" parser.py
done < tokens.csv