#!/usr/bin/env python
from __future__ import annotations
import cairo
import math
import re

class Image():

    def __init__(self, name: str, width: int, height: int, margins):
        
        #generate white background for size
        self.fontsize = 20
        self.surface = cairo.SVGSurface(name, width, height)
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

    
    def generate_legend(self, transcript_datastructure: dict|list|tuple, scale: float):
        '''Generate the bottom backbone legend showing base pair length. all these numbers could be variables in future.'''
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

    def gen_key(self,other: Motifs):
        '''generates motif labels with colors. in the future flip this and draw the box around the lables instead.'''
        #position
        offsetx = self.x1 - (self.x1*.15)
        offsety = self.y1 - (self.y1*.11)
        length = self.x1 *.14
        height = self.y1 *.11
        #draw rectangle for labels to live in
        self.context.set_source_rgb(0,0,0)
        self.context.rectangle(offsetx,offsety, length, height)
        self.context.set_line_width(4)
        self.context.stroke()

        #generate motif names
        fontsize  = self.fontsize*0.75
        self.context.set_font_size(fontsize)
        offsety += offsety *(.015*2)

        #copying datastructure to manipulate for key
        color_dict = other.color_dict
        color_keys = other.color_keys
        patterns = other.patterns

        patterns.append('Exon')
        patterns.append('Intron')
        color_dict['grey'] = (.5,.5,.5,1)
        color_dict['black'] = (0,0,0,1)
        color_keys.append('grey')
        color_keys.append('black')
        for i, pattern in enumerate(patterns):
            #set motif color key equal to motif colors
            color_key = color_keys[i]
            print(color_key)
            R,G,B,A = color_dict[color_key]
            self.context.set_source_rgba(R,G,B,A)
            #position key
            self.context.move_to(offsetx+ offsetx*0.025,offsety-12)
            self.context.show_text(f'{pattern}')
            
            self.context.rectangle(offsetx + offsetx*.01, offsety-offsety/50, offsetx/100,offsety/90)
            self.context.fill()
            offsety += offsety *.015

        #reset font size
        self.context.set_font_size(self.fontsize)

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
    
    def gen_backbone(self, other: Image, y_space, scale: float, width, margins):
            '''generates DNA backbone y coordinate based on number of i. '''
            self.y1 = y_space
            scaled_length = self.x1/scale
            
            other.context.set_line_width(6)
            other.context.set_source_rgb(0,0,0)
            other.context.move_to(self.x0,self.y1)
            other.context.line_to(scaled_length+((other.x0/other.x1)*((width-margins)-scaled_length)),self.y1)
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
                other.context.rectangle(start,y_space-10,end,20)        #(x0,y0,x1,y1)
                other.context.fill()


class Motifs():
    def __init__(self, transcript: Transcript, nucleotide_notation: dict, patterns: list):
        '''Class generates all subsequences matching patterns from transcript provided '''
        #list of motif patterns
        self.patterns = patterns

        #add colors but only need max 5 for this
        self.color_dict = {
            "Blue": (0, 0.095, 0.58, 1),
            "Green": (0.329, 0.788, 0.031, 1),
            "Red": (0.788, 0.235, 0.235, 1),
            "pink": (0.91, 0.318, 0.961, 1),
            "yellow": (1,1,0,1),
        }
        self.color_keys = list(self.color_dict.keys())

        #find motifs using regex for nucleotide notations
        self.motifs = []
        for pattern in self.patterns:
            regex_pattern = pattern_to_regex(pattern, nucleotide_notation)
            for match in re.finditer(f'(?=({regex_pattern}))', transcript.sequence):
                start = match.start()
                end = start + len(pattern)
                self.motifs.append((pattern, match.group(1), start, end))
               

    def gen_motifs(self, other: Image, y_space, figurescale: float):
        
        ending_position = 0

        #assign mortif colors
        motif_color = {}
        for i, pattern in enumerate(self.patterns):
            if pattern not in motif_color:
                
                motif_color[pattern] = self.color_dict[self.color_keys[i]]
                i+=1

        
        #sort motifs by position. lambda is inline function and x[3] extracts motif position
        sorted_motifs = sorted(self.motifs, key=lambda x: x[2])
        
        for match in sorted_motifs:
            
            #calculate motif start position and end(how long rectangle will be)
            start = (match[2]/figurescale) +other.x0
            end = (match[3]-match[2])/figurescale

            if start <= ending_position:
                y_space += 10
            else:
                y_space = transcript.y1

            ending_position = start+end
            #set color of motif
            R,G,B,A = motif_color[match[0]]
            other.context.set_source_rgba(R,G,B,A)

            #draw
            other.context.rectangle(start,y_space,end,20)
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

def get_patterns(fileread) -> list:
    patterns = []
    with open(fileread, 'r') as fhr:
        for line in fhr:
            line = line.strip()
            patterns.append(line)
    return patterns

def pattern_to_regex(pattern, nucelotide_notation):
            regex_pattern = ""
            for char in pattern:
                regex_pattern += nucelotide_notation[char]
            return regex_pattern

#fasta file        
fasta_tuple = fasta_to_tuple("/Users/bailey/bioinfo/Bi625/motif-mark/psuedo_plan/Figure_1.fasta")

#motif patterns
patterns = get_patterns("/Users/bailey/bioinfo/Bi625/motif-mark/psuedo_plan/Fig_1_motifs.txt")

#generate dict of regex patterns
nucleotide_notations = {
    'W': '[AT]',
    'S': '[CG]',
    'M': '[AC]',
    'K': '[GT]',
    'R': '[AG]',
    'Y': '[CT]',
    'B': '[CGT]',
    'D': '[AGT]',
    'H': '[ACT]',
    'V': '[ACG]',
    'N': '[ACGT]',
    'G': '[G]',
    'C': '[C]',
    'A': '[A]',
    'T': '[T]',
    'U': '[U]',
    'w': '[at]',
    's': '[cg]',
    'm': '[ac]',
    'k': '[gt]',
    'r': '[ag]',
    'y': '[ct]',
    'b': '[cgt]',
    'd': '[agt]',
    'h': '[act]',
    'v': '[acg]',
    'n': '[acgt]',
    'g': '[g]',
    'c': '[c]',
    'a': '[a]',
    't': '[t]',
    'u': '[u]',
}

#make multiple DNA objects for each record in fasta file using tupe froma above.
transcript_obj_dict = {}
transcript_keys = []
transcript_values = []
for element in fasta_tuple:
    transcript_obj_dict[element[0]] = Transcript(element[0], element[1])
    transcript_keys.append(element[0])
    transcript_values.append(transcript_obj_dict[element[0]])


filename = "test.svg"
width, height, margins = 1800, 1300, 100
#outimage###########################################

output_image = Image(filename, width, height, margins)

#generate all backbones#############################
#scale first
scale, figurescale = transcript_scaling(transcript_obj_dict, output_image)

y_space=100
for transcript in transcript_obj_dict.values():
    transcript.gen_backbone(output_image, y_space, scale, width, margins)
    exons = Exons(transcript)
    exons.gen_exons(output_image, y_space, figurescale)
    motifs = Motifs(transcript, nucleotide_notations, patterns)
    motifs.gen_motifs(output_image,y_space, figurescale)
    y_space+=100
####################################################
    
#scale and generate image#######################################
#scaled_image = output_image.image_scaling(transcript_obj_dict)
output_image.generate_legend(transcript_obj_dict, scale)
output_image.gen_key(motifs)
output_image.write_png()
################################################################
