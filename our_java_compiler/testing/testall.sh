#!/bin/bash

a=($(ls problems))

for i in "${a[@]}"; do
    python3 ../final.py -f problems/$i 
    mv ../AST.dot output/$i.dot
    mv ../AST.png output/$i.png
    mv ../AST.txt output/$i.txt
done
    