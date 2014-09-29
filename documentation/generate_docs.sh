#!/bin/bash
for i in *.txt; do ditaa $i -o ${i%%.*}.png ; done
