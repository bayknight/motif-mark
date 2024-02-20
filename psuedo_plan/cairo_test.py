#!/usr/bin/env python
from __future__ import annotations
import cairo
import math

width, height = 2000, 2000

#create the coordinates to display your graphic, desginate output

surface = cairo.PDFSurface("example.pdf",width, height)

#create the coordinates you will be drawing on (like a transparency) - you can create a transformation matrix
context = cairo.Context(surface)

#draw a rectangle
""" context.rectangle(100,100,1800,100)        #(x0,y0,x1,y1)
context.fill()

#draw this spaces shows what spacing looks like at this scale
context.rectangle(0,300,1900,100)        #(x0,y0,x1,y1)
context.fill() """

#line
""" context.set_line_width(10)
context.set_source_rgb(.3,.3,.3)
context.move_to(50,150)        #(x,y)
context.line_to(1950,150)
context.stroke() """


#Fasta to one line
#Names in fasta
#lengths of sequences
    
        
class DNA_figure():
    '''This is a skeleton of a class to draw a DNA figure it takes name and length
    that will be parsed from a fasta file in order to draw shapes. It will need
    a way to handle motifs.'''
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length
        
        #starting position coordinates
        self.x0 = 100
        self.y0 = 100
        self.x1 = 1800
        self.y1 = 100

    def positional_increment(self, dna_figure: DNA_figure):
        self.y0 = dna_figure.y0 + 400
        self.y1 = dna_figure.y1 + 400
        return self.y0, self.y1
        
    def seq_draw_line(self):
        context.set_line_width(10)
        context.set_source_rgb(.3,.3,.3)
        context.move_to(self.x0,self.y0)        #(x,y)
        context.line_to(self.x1,self.y1)
        context.stroke()



class Motif():
    ''' will need sequence and length and position will be determined in
    DNA_figure. Still need to normalize sizing'''
    def __init__(self, sequence: str, start: int, end: int, dna_figure: DNA_figure):
        
        self.sequence = sequence
        self.x0 = start #normalize
        self.x1 = end
        self.y0 = dna_figure.y0 #normalize
        self.y1 = dna_figure.y1  #normalize

        context.rectangle(self.x0,self.y0,self.x1,self.y1)        #(x0,y0,x1,y1)
        context.fill()
        


#add if name = main
testfigure = DNA_figure("SWAG", 1000)
testfigure2 = DNA_figure("SWAG", 1000)

testfigure.seq_draw_line()
testfigure2.positional_increment(testfigure)
testfigure2.seq_draw_line()
testmotif1 = Motif("YGGY", 100, 120, testfigure)


#first create a DNA_figure for each sequence in the FASTA
#make a dictionary of motif sequences
#loop through sequences of them all and if a motif is hit generate a motif object
