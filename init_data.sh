#!/usr/bin/env bash


COMMAND='./cli/main.py -u root -p password add'


$COMMAND \
'book=Harry Potter;1997;JK Rowling;Bloomsbury;978-3-16-148410-0' \
'book=Harry Potter 2;1998;JK Rowling;Bloomsbury;978-3-15-148410-1' \
'book=Dune;1984;Frank Herbert;randomred;978-5-16-148410-2'
