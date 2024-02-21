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

class Image():

    def __init__(self, name: str, width: int, height: int):
        
        #generate white background for size

        self.surface = cairo.SVGSurface(name, width, height)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.rectangle(0, 0, width, height)
        self.context.fill()
        #initial coordinates to start at (lines)
        self.x0 = 100
        self.y0 = 100
        self.max_length = 0

        #allows multiple sequences
        self.multiple_sequences = False
    
    """ def seq_draw_line(self, other: DNA):
        self.context.set_line_width(10)
        self.context.set_source_rgb(.3,.3,.3)
        self.context.move_to(100,100)    #(x,y)
        self.context.line_to(1000,100)
        self.context.stroke()
        self.surface.write_to_png('test.png') """    
    def draw_backbone(self, other: DNA):
        self.context.set_line_width(10)
        self.context.set_source_rgb(.3,.3,.3)
        if self.multiple_sequences == True:
            self.y0 = self.y0 + 200
            self.context.move_to(100,self.y0)    #(x,y)
            self.context.line_to(1000,self.y0)
        else:
            self.context.move_to(self.x0,100)    #(x,y)
            self.context.line_to(1000,100)
            self.multiple_sequences = True   #(x,y)
        stroke = self.context.stroke()
    def generate_legend(self):
        self.context.set_line_width(10)
        self.context.set_source_rgb(.3,.3,.3)
        if self.multiple_sequences == True:
            self.y0 = self.y0 + 200
            self.context.move_to(100,self.y0)    #(x,y)
            self.context.line_to(1000,self.y0)
        else:
            self.context.move_to(self.x0,100)    #(x,y)
            self.context.line_to(1000,100)
            self.multiple_sequences = True        

    def write_png(self):
        self.surface.write_to_png('test.png')

    def _max_length(self, dna_dict: dict):
        '''takes list of DNA objects and generates legend based on max length
        return rounded up '''
        seqprev=''
        for key in dna_dict:
            seqcurrent = dna_dict[key]
            if len(seqcurrent) > len(seqprev):
                seqprev=seqcurrent    
        self.max_length = round(len(seqcurrent), -2)
        return self.max_length

        
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
        self.x0 = 100
        self.y0 = 100
        self.x1 = 1000
        self.y1 = 100
    
    def __len__(self):
        #delete and see if still works.
        return self.length
    
    def positional_increment(self, other: DNA):
        self.y0 = other.y0 + 400
        self.y1 = other.y1 + 400
        return self.y0, self.y1


def fasta_to_tuple(fileread):
    ''''''
    fasta_tuple = []
    seq=''
    header =''
    with open(fileread, 'r') as fhr:
        for line in fhr:
            line = line.strip()
            if line.startswith('>'):
                if seq == '':
                    header = line
                else:
                    fasta_tuple.append((header, seq))
                    seq = ''
                    header = line 
            else:
                seq += line
        fasta_tuple.append((header,seq))
    return fasta_tuple


        
fasta_tuple = fasta_to_tuple("/Users/bailey/bioinfo/Bi625/motif-mark/psuedo_plan/Figure_1.fasta")


#make multiple DNA objects for each record in fasta file using tupe froma above.
dna_obj_dict = {}
dna_keys = []
for element in fasta_tuple:
    dna_obj_dict[element[0]] = DNA(element[0], element[1])
    dna_keys.append(element[0])




#for value in dna_obj_dict:
    

filename = "test.svg"

width, height = 1100, 1100


output_image = Image(filename, width, height)
output_image.draw_backbone(dna_obj_dict[dna_keys[0]])
output_image.draw_backbone(dna_obj_dict[dna_keys[1]])
output_image.draw_backbone(dna_obj_dict[dna_keys[2]])
output_image._generate_legend(dna_obj_dict)
output_image.write_png()
#add if name = main
#first create a DNA_figure for each sequence in the FASTA
#make a dictionary of motif sequences
#loop through sequences of them all and if a motif is hit generate a motif object
