#!/usr/bin/env python
from __future__ import annotations
import cairo
import math

#width, height = 1100, 1100

#create the coordinates to display your graphic, desginate output

#surface = cairo.SVGSurface("example.svg",width, height)

#create the coordinates you will be drawing on (like a transparency) - you can create a transformation matrix
""" context = cairo.Context(surface)
context.set_source_rgba(1, 1, 1, 1)
context.rectangle(0, 0, 1100, 1100)
context.fill() """
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

#parse fasta

class Image():

    def __init__(self, width: int, height: int):
        
        #generate white background for size

        surface = cairo.SVGSurface(name, width, height)

        self.context = cairo.Context(surface)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.rectangle(0, 0, width, height)
        self.context.fill()
    
    """ def seq_draw_line(self):
        self.context.set_line_width(10)
        self.context.set_source_rgb(.3,.3,.3)
        self.context.move_to(self.x0,self.y0)        #(x,y)
        self.context.line_to(self.x1,self.y1)
        self.context.stroke() """


    def _generate_legend(self, DNA_list: list):
        '''takes list of DNA objects and generates legend based on max length'''
        return max(DNA_list, key=lambda x: x.length)
        #max(person_list, key=attrgetter('age'))
      
        
class DNA():
    '''This is a skeleton of a class to draw a DNA figure it takes name and length
    that will be parsed from a fasta file in order to draw shapes. It will need
    a way to handle motifs.'''
    def __init__(self, name: str, sequence: str):
        self.name = name
        self.sequence = sequence
        self.length = len(sequence)
        
        #starting position coordinates
        """ self.x0 = 100
        self.y0 = 100
        self.x1 = 1000
        self.y1 = 100 """
    
    def __len__(self):
        #delete and see if still works.
        return self.length
    
    def positional_increment(self, other: DNA):
        self.y0 = other.y0 + 400
        self.y1 = other.y1 + 400
        return self.y0, self.y1


        

    
    


width, height = 1100, 1100

output_image = Image(width, height)
#add if name = main
        

testfigure = DNA_figure("SWAG", 1000)
testfigure2 = DNA_figure("SWAG", 1000)

testfigure.seq_draw_line()
testfigure2.positional_increment(testfigure)
testfigure2.seq_draw_line()
testmotif1 = Motif("YGGY", 100, 120, testfigure)



surface.write_to_png('geek.png')
#first create a DNA_figure for each sequence in the FASTA
#make a dictionary of motif sequences
#loop through sequences of them all and if a motif is hit generate a motif object
