#!/bin/bash

[ -f pan-tadeusz.txt ] || wget https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt
[ -f dead-souls.txt ]  || wget https://www.gutenberg.org/cache/epub/1081/pg1081.txt -O dead-souls.txt
