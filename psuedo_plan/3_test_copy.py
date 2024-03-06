#!/usr/bin/env python
from __future__ import annotations
import cairo
import math
import re
import argparse
import os

class Image():

    def __init__(self, name: str, width: int, height: int, margins):
        
        #generate white background for size
        self.fontsize = 20
        self.surface = cairo.SVGSurface(f'{name}.svg', width, height)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.set_source_rgba(1, 1, 1, 1)
        self.context.rectangle(0, 0, width, height)
        self.context.fill()
        self.context.set_font_size(self.fontsize)
        self.context.select_font_face("Arial",
                                    cairo.FONT_SLANT_NORMAL,
                                    cairo.FONT_WEIGHT_NORMAL)
        #initial coordinates to start at (lines) these shouldnt be hard coded but are for now.

        self.x0 = margins
        self.y0 = margins
        self.x1 = width-margins
        self.y1 = height-margins

    
    def generate_legend(self, height, scale: float):
        '''Generate the bottom backbone legend showing base pair length. all these numbers could be variables in future.'''
        self.context.set_line_width(8)
        self.context.set_source_rgb(0,0,0)
        round_length = int(self.x1 *scale)
        half_max = round_length/2
        #starting_point
        self.context.move_to(self.x0,self.y1) 
        #end point
        self.context.line_to(self.x1,self.y1)
        #self.context.stroke()
        #legend ticks
        tick_offset = 25
        text_offset = 20
        #left
        self.context.move_to(self.x0+4,self.y1)
        self.context.line_to(self.x0+4,self.y1-tick_offset)
        self.context.move_to(self.x0,self.y1+text_offset)
        self.context.show_text("0")
        #middle
        tickx = (self.x1+100)/2
        self.context.move_to(tickx+4,self.y1)
        self.context.line_to(tickx+4,self.y1-tick_offset)
        self.context.move_to(tickx-15,self.y1+text_offset)
        self.context.show_text(f'{half_max}')
        self.context.move_to(tickx-45,self.y1+40)
        self.context.show_text("Base Pair (BP)")
        #right      
        self.context.move_to(self.x1-4,self.y1)
        self.context.line_to(self.x1-4,self.y1-tick_offset)
        self.context.move_to(self.x1-25,self.y1+text_offset)
        self.context.show_text(f'{round_length}')
        
        self.context.stroke()
        
        #reset just in case

        self.x0 = margins
        self.y0 = margins
        self.x1 = width-margins
        self.y1 = height-margins

    def write_png(self, name: str):
        self.surface.write_to_png(name)    
        #max(person_list, key=attrgetter('age'))
    
        
class Transcript():
    '''This class is composed of introns exons and motifs. It facilitates the drawing of all those structures on the image class'''
    def __init__(self, name: str, sequence: str, other: Image, figure_scale, total_scale, nucleotide_dict, patterns,y_space):

        
        #self.motifs = Motifs(self)
        self.name = name
        self.sequence = sequence
        self.length = len(sequence)
        #starting coords
        self.x0 = 100
        self.y0 = 100
        #ending position coordinates (image)
        self.x1 = self.length
        self.y1 = y_space
        #data structures for regex pattern matching
        self.dict = nucleotide_dict
        self.patterns = patterns

        #generate introns exons and motifs
        self.introns = Introns(self.x1, other, y_space, total_scale, width, margins)
        self.exons = Exons(self.sequence, other, y_space, figure_scale)
        self.motifs = Motifs(transcript, other, self.dict, self.patterns, self.introns.y1)
        self.labels = Labels(self.name, self.x0, other, self.patterns, self.motifs.color_dict, y_space)
    
    def __len__(self):
        #delete and see if still works.
        return self.length
    

class Introns():
    def __init__(self,length, other: Image, y_space, scale: float, width, margins):
        '''generates DNA backbone y coordinate based on number of i. this takes the entire lenght, but exons will lie on top of this backbone. '''
        self.y1 = y_space
        scaled_length = length/scale 
        other.context.set_line_width(10)
        other.context.set_source_rgb(0,0,0)
        other.context.move_to(margins,self.y1)
        other.context.line_to(scaled_length+((other.x0/other.x1)*((width-margins)-scaled_length)),self.y1)
        other.context.stroke()


class Exons():
    def __init__(self, sequence, other: Image, y_space, figure_scale):
        '''Generate exons and draw rectangle on context based on capital leters'''
        self.y0 = y_space
        self.exons= []
        for match in re.finditer(r'[A-Z]+', sequence):
            self.exon = match.group(0)
            start = match.start()
            end = match.end()
            self.exons.append((start,end))
   
            
        for exon in self.exons:
            start = (exon[0]/figurescale)+other.x0
            end = (exon[1]-exon[0])/figurescale
            other.context.set_source_rgb(.5,.5,.5)
            other.context.rectangle(start,y_space-15,end,30)        #(x0,y0,x1,y1)
            other.context.fill()


class Motifs():
    def __init__(self, sequence, other: Image, nucleotide_notation: dict, patterns: list, y_position: float):
        '''Class generates all subsequences matching patterns from transcript provided '''
        #list of motif patterns

        #add colors but only need max 5 for this
        self.color_dict = {
            "Blue": (0, 0.095, 0.58, 1),
            "Green": (0.329, 0.788, 0.031, 1),
            "Red": (0.788, 0.235, 0.235, 1),
            "pink": (0.91, 0.318, 0.961, 1),
            "yellow": (1,1,0,1),
        }
        self.color_keys = list(self.color_dict.keys())

        self.max_y = y_position
        #find motifs using regex for nucleotide notations
        self.motifs = []
        for pattern in patterns:
            regex_pattern = pattern_to_regex(pattern, nucleotide_notation)
            for match in re.finditer(f'(?=({regex_pattern}))',sequence):
                start = match.start()
                end = start + len(pattern)
                self.motifs.append((pattern, match.group(1), start, end))
               

    
        

        #assign mortif colors
        self.motif_color = {}
        for i, pattern in enumerate(patterns):
            if pattern not in self.motif_color:
                
                self.motif_color[pattern] = self.color_dict[self.color_keys[i]]
                i+=1

        
        #sort motifs by position. lambda is inline function and x[3] extracts motif position
        sorted_motifs = sorted(self.motifs, key=lambda x: x[3])
        
        process_overlaps(sorted_motifs,self.motif_color,other, self.max_y)

           
            
            
class Labels():
    def __init__(self,name, x0, other, patterns, color_dict, y_space):

        #make new memory point for list
        self.patterns = patterns[:]
        self.patterns.append('Exon')
        self.patterns.append('Intron')
        color_dict['grey'] = (.5,.5,.5,1)
        color_dict['black'] = (0,0,0,1)
        
        color_keys = list(color_dict.keys())
        height = 10
        other.context.set_source_rgba(0,0,0,1)
        other.context.move_to(x0, y_space - 175)
        other.context.show_text(f'{name}')
        for i, pattern in enumerate(self.patterns):
            #set motif color key equal to motif colors
            R,G,B,A = color_dict[color_keys[i]]
            other.context.set_source_rgba(R,G,B,A)
            #position key
            other.context.move_to(x0+50, y_space - 150)
            other.context.show_text(f'{pattern}')
            y_space+=22
            other.context.rectangle(x0, y_space-182, x0*.1, height )
            other.context.fill()
            
    

def transcript_scaling(transcript_dict: dict, image: Image):
    seqprev=''
    for key in transcript_dict:
        seqcurrent = transcript_dict[key]

        if len(seqcurrent) > len(seqprev):
            seqprev=seqcurrent
    scale = len(seqprev)/image.x1
    figurescale = len(seqprev)/(image.x1-image.x0)
    return scale, figurescale
 
def fasta_to_tuple(fileread):
    '''makes list of tuples from fasta file. (name, sequence)'''
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

def get_patterns(fileread) -> list:
    '''get patterns in strings from file'''
    patterns = []
    with open(fileread, 'r') as fhr:
        for line in fhr:
            line = line.strip()
            patterns.append(line)
    return patterns

def pattern_to_regex(pattern, nucelotide_notation):
    '''convert pattern to regex format for nucleotide notation'''
    regex_pattern = ""
    for char in pattern:
        regex_pattern += nucelotide_notation[char]
    return regex_pattern

def process_overlaps(sorted_motifs,motif_color, other: Image, max_y):
    # Initialize a list to store motifs that overlap with the previous motif
    current_overlapping = []
    end_prev = 0
    # Loop through the sorted motifs
    for motif in sorted_motifs:
        # Calculate start and end positions of the current motif
        start = (motif[2] / figurescale) + other.x0
        end = (motif[3] - motif[2]) / figurescale
        
        # Check if the current motif overlaps with the previous motif
        if start <= end_prev:
            current_overlapping.append(motif)
        else:
            # Draw the non-overlapping motif
            R, G, B, A = motif_color[motif[0]]
            other.context.set_source_rgba(R, G, B, A)
            # Draw
            other.context.rectangle(start, max_y, end, 30)
            other.context.fill()

            # Update the previous end position
            end_prev = start + end

    # If there are motifs overlapping with the previous motif, process them
    if current_overlapping:
        max_y += 32
        process_overlaps(current_overlapping, motif_color, other, max_y)

# Initialize the previous end position
end_prev = 0

def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input file name
        -m motif file name'''
    parser = argparse.ArgumentParser(description="A program to generate binned contig length.")
    parser.add_argument("-f", "--filename", help="Your filename", type=str)
    parser.add_argument("-m", "--motif", help="motif file name", type=str)
    return parser.parse_args()      

            


args = get_args()
filename = args.filename
fileout = filename.split('.')
fileout = fileout[0]
motifs = args.motif
#fasta file        
fasta_tuple = fasta_to_tuple(filename)

#motif patterns
patterns = get_patterns(motifs)

#generate dict of regex patterns
nucleotide_notations = {
    'W': '[ATW]',
    'S': '[CGS]',
    'M': '[ACM]',
    'K': '[GTK]',
    'R': '[AGR]',
    'Y': '[CTY]',
    'B': '[CGTB]',
    'D': '[AGTD]',
    'H': '[ACTH]',
    'V': '[ACGV]',
    'N': '[ACGTN]',
    'G': '[G]',
    'C': '[C]',
    'A': '[A]',
    'T': '[T]',
    'U': '[U]',
    'w': '[atw]',
    's': '[cgs]',
    'm': '[acm]',
    'k': '[gtk]',
    'r': '[agr]',
    'y': '[cty]',
    'b': '[cgtb]',
    'd': '[agtd]',
    'h': '[acth]',
    'v': '[acgv]',
    'n': '[acgtn]',
    'g': '[g]',
    'c': '[c]',
    'a': '[a]',
    't': '[t]',
    'u': '[u]',
}

width,margins = 1920, 100
height = len(fasta_tuple)*700 +7*margins


output_image = Image(fileout, width, height, margins)

#generate all backbones#############################
#scale first

#make multiple DNA objects for each record in fasta file using tupe froma above.
transcript_obj_dict = {}
for element in fasta_tuple:
    transcript_obj_dict[element[0]] = (element[1])

scale, figurescale = transcript_scaling(transcript_obj_dict, output_image)

#outimage###########################################



y_space = 400
max_y = 100
transcripts = []
prevy = 300
for i, transcript in enumerate(transcript_obj_dict.values()):
    name = fasta_tuple[i][0]
    transcript = Transcript(name, transcript,output_image,figurescale, scale, nucleotide_notations, patterns, y_space)
    transcripts.append(transcript)
    max_y = transcript.motifs.max_y
    diffy = max_y-prevy
    y_space= 700+y_space
####################################################
    
#scale and generate image#######################################
output_image.generate_legend(y_space, scale)
output_image.write_png(f'{fileout}.png')
################################################################
