#!/usr/bin/env python
from __future__ import annotations
import cairo
import math
import re

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

    def __init__(self, name: str, width: int, height: int, margins):
        
        #generate white background for size

        self.surface = cairo.SVGSurface(name, width, height)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.rectangle(0, 0, width, height)
        self.context.fill()
        self.context.set_font_size(20)
        self.context.select_font_face("Arial",
                                    cairo.FONT_SLANT_NORMAL,
                                    cairo.FONT_WEIGHT_NORMAL)
        #initial coordinates to start at (lines) these shouldnt be hard coded but are for now.

        self.x0 = margins
        self.y0 = margins
        self.x1 = width-margins
        self.y1 = height-margins

    
    def generate_legend(self, transcript_datastructure: dict|list|tuple, scale: float):
        '''needs a data structure with length'''
        self.context.set_line_width(8)
        self.context.set_source_rgb(0,0,0)
        round_length = int(self.x1 *scale)
        half_max = round_length/2
        #starting_point
        n = len(transcript_datastructure)
        self.y0 = 200 + (n*100)
        self.context.move_to(self.x0,self.y0) 
        #end point
        self.context.line_to(self.x1,self.y0)
        #self.context.stroke()
        #legend ticks
        tick_offset = 25
        text_offset = 20
        #left
        self.context.move_to(self.x0+4,self.y0)
        self.context.line_to(self.x0+4,self.y0-tick_offset)
        self.context.move_to(self.x0,self.y0+text_offset)
        self.context.show_text("0")
        #middle
        tickx = (self.x1+100)/2
        self.context.move_to(tickx+4,self.y0)
        self.context.line_to(tickx+4,self.y0-tick_offset)
        self.context.move_to(tickx-15,self.y0+text_offset)
        self.context.show_text(f'{half_max}')
        self.context.move_to(tickx-45,self.y0+40)
        self.context.show_text("Base Pair (BP)")
        #right      
        self.context.move_to(self.x1-4,self.y0)
        self.context.line_to(self.x1-4,self.y0-tick_offset)
        self.context.move_to(self.x1-25,self.y0+text_offset)
        self.context.show_text(f'{round_length}')
        
        self.context.stroke()
        #reset just in case

        self.x0 = margins
        self.y0 = margins
        self.x1 = width-margins
        self.y1 = height-margins

    def write_png(self):
        self.surface.write_to_png('test.png')

        
        #max(person_list, key=attrgetter('age'))
      
        
class Transcript():
    '''This is a skeleton of a class to draw a DNA figure it takes name and length
    that will be parsed from a fasta file in order to draw shapes. It will need
    a way to handle motifs.'''
    def __init__(self, name: str, sequence: str):
        self.name = name
        self.sequence = sequence
        self.length = len(sequence)
        #starting coords
        self.x0 = 100
        self.y0 = 100
        #ending position coordinates (image)
        self.x1 = self.length
        self.y1 = 100
    
    def __len__(self):
        #delete and see if still works.
        return self.length
    
    def gen_backbone(self, other: Image, y_space, scale: float):
            '''generates DNA backbone y coordinate based on number of i. '''
            self.y1 = y_space
            scaled_length = self.x1/scale
            print(self.x1,scaled_length)
            other.context.set_line_width(6)
            other.context.set_source_rgb(0,0,0)
            other.context.move_to(self.x0,self.y1)
            other.context.line_to(scaled_length+((other.x0/other.x1)*(1000-scaled_length)),self.y1)
            other.context.stroke()

class Exons():
    def __init__(self, transcript: Transcript):
        
        
        sequence = transcript.sequence
        self.exons= []
        for match in re.finditer(r'[A-Z]+', sequence):
            self.exon = match.group(0)
            start = match.start()
            end = match.end()
            self.exons.append((start,end))
    def gen_exons(self, other: Image, y_space, figurescale: float):
            '''generates exons y coordinate based on number of i. '''
            
            for exon in self.exons:
                start = (exon[0]/figurescale)+other.x0
                end = (exon[1]-exon[0])/figurescale
                other.context.set_source_rgb(.5,.5,.5)
                other.context.rectangle(start,y_space,end,20)        #(x0,y0,x1,y1)
                other.context.fill()


class Motif():
    def __init__(self, sequence: str):

        self.sequence = sequence
        self.length = len(sequence)
        
        #ending (length) position coordinates
        self.x0 = 100 + (self.length/900)*900
        self.y0 = 100

    def __len__(self):
        return self.length
##ADD REPR
def transcript_scaling(transcript_dict: dict, image: Image):
    seqprev=''
    for key in transcript_dict:
        seqcurrent = transcript_dict[key]
        print(len(seqcurrent))
        if len(seqcurrent) > len(seqprev):
            seqprev=seqcurrent
    scale = len(seqprev)/image.x1
    figurescale = len(seqprev)/(image.x1-image.x0)
    return scale, figurescale
#def find_exons():    
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
transcript_obj_dict = {}
transcript_keys = []
transcript_values = []
for element in fasta_tuple:
    transcript_obj_dict[element[0]] = Transcript(element[0], element[1])
    transcript_keys.append(element[0])
    transcript_values.append(transcript_obj_dict[element[0]])


filename = "test.svg"
width, height, margins = 1100, 1300, 100
#outimage###########################################

output_image = Image(filename, width, height, margins)

#generate all backbones#############################
#scale first
scale, figurescale = transcript_scaling(transcript_obj_dict, output_image)
print(figurescale)
y_space=100
for transcript in transcript_obj_dict.values():
    transcript.gen_backbone(output_image, y_space, scale)
    exons = Exons(transcript)
    exons.gen_exons(output_image, y_space, figurescale)
    y_space+=100
####################################################
    
#scale and generate image#######################################
#scaled_image = output_image.image_scaling(transcript_obj_dict)
output_image.generate_legend(transcript_obj_dict, scale)
output_image.write_png()
################################################################
