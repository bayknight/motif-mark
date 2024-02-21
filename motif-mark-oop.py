#!/usr/bin/env python
from __future__ import annotations
import cairo
import math
import argparse





def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input file name
        -m motif file name'''
    parser = argparse.ArgumentParser(description="A program to generate binned contig length.")
    parser.add_argument("-f", "--filename", help="Your filename", type=str)
    parser.add_argument("-m", "--motif", help="motif file name", type=str)
    return parser.parse_args()





































if __name__ == "main":

    width, height = 1100, 1100

    #create the coordinates to display your graphic, desginate output
    surface = cairo.SVGSurface("example.svg",width, height)
    
    #create the coordinates you will be drawing on and makes it white
    context = cairo.Context(surface)
    context.set_source_rgba(1, 1, 1, 1)
    context.rectangle(0, 0, width, height)
    context.fill()














    surface.write_to_png('output.png')
