#!/usr/bin/env python

import cairo
import re
import argparse

'''The purpose of this code is to find motifs given two input files. The first file should be a fasta file and the 
second file should be .txt file listin motifs by row. the image is scaled appropriately to the number of overlapping
motifs and fastas. max motifs is 5 and max length of motif is 10 as designated in assignment. If this ever needs
to change the key will be the main thing to change in order to accommodate more morifs in the space provided. If more motifs than 5
are given or length greater than 10 given it will still work but the key will be messy. '''

class Image():
    '''This class is used to generate the image and hold dimensional attributes'''
    def __init__(self, name: str, width: int, height: int, margins):
        
        #generate white background for size
        self.fontsize = 20
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
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
        self.width = width
        self.height = height
        self.margins = margins
        self.x0 = margins
        self.y0 = margins
        self.x1 = width-margins
        self.y1 = height-margins

    def resize_height(self, new_height):
        '''used to resize image to appropriate height due to earlier design flaws.'''
        # Create a new surface with the new height
        new_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, new_height)
        
        # Create a new context for the new surface
        new_context = cairo.Context(new_surface)
        
        # Copy content from the current surface to the new one
        new_context.set_source_surface(self.surface)
        new_context.paint()
        
        # Update attributes with the new height
        self.height = new_height
        self.surface = new_surface
        self.context = new_context
        self.y1 = new_height-margins 

    def generate_legend(self, height, scale: float):
        '''Generate the bottom backbone legend showing base pair length. all these numbers could be variables in future.'''
        self.context.set_line_width(8)
        self.context.set_source_rgb(0,0,0)
        round_length = int(self.x1 *scale)
        half_max = round_length/2
        self.context.set_font_size(20)
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
    def __init__(self, name: str, sequence: str, other: Image, figure_scale, total_scale, nucleotide_dict, patterns, y_space):

        
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
        self.introns = Introns(self.x1, other, self.y1, total_scale, width, margins)
        self.exons = Exons(self.sequence, other, self.y1, figure_scale)
        self.motifs = Motifs(sequence, other, self.dict, self.patterns, self.y1)
        self.labels = Labels(self.name, self.x0, other, self.patterns, self.motifs.color_dict, self.y1)

        self.max_overlaps = self.motifs.maximum_overlaps(other)
    def __len__(self):
        #delete and see if still works.
        return self.length
    

class Introns():
    def __init__(self,length: int, other: Image, y_space: float, scale: float, width: float, margins: float):
        '''generates DNA backbone y coordinate based on number of i. this takes the entire lenght, but exons will lie on top of this backbone. '''
        self.y1 = y_space
        scaled_length = length/scale 
        other.context.set_line_width(10)
        other.context.set_source_rgb(0,0,0)
        other.context.move_to(margins,self.y1)
        #scaling to max length
        other.context.line_to(scaled_length+((other.x0/other.x1)*((width-margins)-scaled_length)),self.y1)
        other.context.stroke()


class Exons():
    def __init__(self, sequence: str, other: Image, y_space, figure_scale: float):
        '''Generate exons and draw rectangle on context based on capital leters'''
        self.y0 = y_space
        self.exons= []
        #find exons
        for match in re.finditer(r'[A-Z]+', sequence):
            self.exon = match.group(0)
            start = match.start()
            end = match.end()
            self.exons.append((start,end))
   
        #draw exons using start and ending positons. positions are scaled to image  
        for exon in self.exons:
            start = (exon[0]/figurescale)+other.x0
            end = (exon[1]-exon[0])/figurescale
            other.context.set_source_rgb(.5,.5,.5)
            other.context.rectangle(start,y_space-15,end,30)        #(x0,y0,x1,y1)
            other.context.fill()


class Motifs():
    def __init__(self, sequence: str, other: Image, nucleotide_notation: dict, patterns: list, y_position: float):
        '''Class generates all subsequences matching patterns from transcript provided '''
        #list of motif patterns

        #add colors but only need max 5 for this
        self.color_values = [(0, 0.095, 0.58, 1),
            (0.329, 0.788, 0.031, 1),
            (0.788, 0.235, 0.235, 1),
            (0.91, 0.318, 0.961, 1),
            (1,1,0,1)]
        self.color_keys = ["Blue",
            "Green",
            "Red",
            "pink",
            "yellow"]
        
        self.color_dict = {}
        for i in range(len(patterns)):
            self.color_dict[self.color_keys[i]]=self.color_values[i]

        #generate a max_y position.
        self.max_y = y_position

        #find motifs using regex for nucleotide notations and get start and ending positions
        self.motifs = []
        for pattern in patterns:
            regex_pattern = pattern_to_regex(pattern, nucleotide_notation)
            for match in re.finditer(f'(?=({regex_pattern}))',sequence):
                start = match.start()
                end = start + len(pattern)
                self.motifs.append((pattern, match.group(1), start, end))

        #assign motif colors
        self.motif_color = {}
        for i, pattern in enumerate(patterns):
            if pattern not in self.motif_color:
                
                self.motif_color[pattern] = self.color_dict[self.color_keys[i]]
                i+=1

        
        #sort motifs by position. lambda is inline function and x[3] extracts motif position
        sorted_motifs = sorted(self.motifs, key=lambda x: x[3])
        
        #find overlaps from sorted motifs. this could be changed to a class function.
        process_overlaps(sorted_motifs,self.motif_color,other, self.max_y)

    def maximum_overlaps(self, other: Image):
        '''find maximum number of overlaps to scale the spacing between transcripts.'''
        # Initialize variables to store the maximum number of overlaps
        max_overlaps = 0
        current_overlaps = 0
        end_prev = 0
        # Sort motifs by their start position
        sorted_motifs = sorted(self.motifs, key=lambda x: x[2])
        
        # find motifs starting and ending positons. positions scaled to iumage
        for motif in sorted_motifs:
            start = (motif[2] / figurescale) + other.x0
            end = (motif[3] - motif[2]) / figurescale
            
            # Check if the current motif overlaps with the previous motif
            if start < end_prev:
                current_overlaps += 1
            else:
                # Update the maximum number of overlaps if needed
                max_overlaps = max(max_overlaps, current_overlaps)
                current_overlaps = 1  # Reset current overlaps count
            
            # Update the previous end position
            end_prev = start + end
        
        # Update the maximum number of overlaps if needed (for the last motif)
        max_overlaps = max(max_overlaps, current_overlaps)

        return max_overlaps           
            
            
class Labels():
    def __init__(self,name: str, x0: float, other: Image, patterns: list, color_dict: dict, y_space: float):

        #make new memory point for list to add exon and intron colors.
        self.patterns = patterns[:]
        self.patterns.append('Exon')
        self.patterns.append('Intron')
        color_dict['grey'] = (.5,.5,.5,1)
        color_dict['black'] = (0,0,0,1)
        
        #set color keys and label names
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
    '''Function to generate a multiplier for both scaling the legend to the image
    and the transcripts to the legend.'''
    seqprev=''
    for key in transcript_dict:
        seqcurrent = transcript_dict[key]

        if len(seqcurrent) > len(seqprev):
            seqprev=seqcurrent
    scale = len(seqprev)/image.x1
    figurescale = len(seqprev)/(image.x1-image.x0)
    return scale, figurescale
 
def fasta_to_tuple(fileread: str) ->list:
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

def get_patterns(fileread: str) -> list:
    '''get patterns in strings from file'''
    patterns = []
    with open(fileread, 'r') as fhr:
        for line in fhr:
            line = line.strip()
            patterns.append(line)
    return patterns

def pattern_to_regex(pattern: str, nucelotide_notation: dict) ->str:
    '''convert pattern to regex format for nucleotide notation'''
    regex_pattern = ""
    for char in pattern:
        regex_pattern += nucelotide_notation[char]
    return regex_pattern

def process_overlaps(sorted_motifs: list,motif_color: dict, other: Image, max_y: float|int):
    '''look for overlaps recursively to maximize motifs on each increment of y.'''
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
            other.context.rectangle(start, max_y, end, 30)
            other.context.fill()

            # Update the previous end position
            end_prev = start + end

    # If there are motifs in current overlapping list recursively call process overlaps until current overlapping list is empty.
    if current_overlapping:
        #increment y position for overlap viewing
        max_y += 32
        process_overlaps(current_overlapping, motif_color, other, max_y)

def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input file name
        -m motif file name'''
    parser = argparse.ArgumentParser(description="A program to generate binned contig length.")
    parser.add_argument("-f", "--filename", help="Your filename", type=str)
    parser.add_argument("-m", "--motif", help="motif file name", type=str)
    return parser.parse_args()      

            

if __name__ == "__main__":

    # get argumetns and set them to variables
    args = get_args()

    #split filenames to get basename for output png
    filename = args.filename
    fileout = filename.split('.')
    fileout = fileout[0]

    #get motifs file too
    motifs = args.motif
    
    #fasta file parsing        
    fasta_tuple = fasta_to_tuple(filename)

    #get motif patterns
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

    #set dimensions of initial image
    width,margins = 1920, 100
    height = len(fasta_tuple)*700 +4*margins


    output_image = Image(fileout, width, height, margins)

    #make multiple DNA objects for each record in fasta file using tupe froma above.
    transcript_obj_dict = {}
    for element in fasta_tuple:
        transcript_obj_dict[element[0]] = (element[1])


    #calculate the multipliers for scaling legend and transcripts
    scale, figurescale = transcript_scaling(transcript_obj_dict, output_image)

    # set initial y transcript starting position and max_y and empty transcript list
    y_space = 300
    max_y = 100
    transcripts = []

    #instantiate transcript objects (they generate the images too)
    for i, sequence in enumerate(transcript_obj_dict.values()):
        name = fasta_tuple[i][0]
        transcript = Transcript(name, sequence ,output_image,figurescale, scale, nucleotide_notations, patterns,y_space)
        transcripts.append(transcript)
        y_space= y_space + 32*transcript.max_overlaps +400

        
    #resize, make legend and outputt image#
    output_image.resize_height(y_space)
    output_image.generate_legend(y_space, scale)
    output_image.write_png(f'{fileout}.png')

