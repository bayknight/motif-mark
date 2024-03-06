The purpose of this code is to find motifs given two input files. The first file should be a fasta file and the 
second file should be .txt file listin motifs by row. the image is scaled appropriately to the number of overlapping
motifs and fastas. max motifs is 5 and max length of motif is 10 as designated in assignment. If this ever needs
to change the key will be the main thing to change in order to accommodate more morifs in the space provided. If more motifs than 5
are given or length greater than 10 given it will still work but the key will be messy.

run using:

``` ./motif-mark-oop.py -f <fastafilepath> -m <motiffilepath> ```

Output files will be outputted to folder where fastafile is held.


psuedo_plan folder contains 2 example file sets and outputs as well as a brief example of basic pycairo.


future directions:

if needed to optimize build from motif up rather than transcript down for positions. this would eliminate the need for rescaling