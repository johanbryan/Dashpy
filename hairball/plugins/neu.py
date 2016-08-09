"""This module provides plugins for NEU metrics."""

import kurt
from hairball.plugins import HairballPlugin
from PIL import Image
import os


class Variables(HairballPlugin):

    """Plugin that counts the number of variables in a project."""

    def __init__(self):
        super(Variables, self).__init__()
        self.total = 0

    def finalize(self):
        """Output the number of variables in the project."""
        print("Number of variables: %i" % self.total)

    def analyze(self, scratch):
        """Run and return the results of the Variables plugin."""          
        self.total = len(scratch.variables)
        for x in scratch.sprites:
            self.total += len(x.variables)

class Lists(HairballPlugin):

    """Plugin that counts the number of lists in a project."""

    def __init__(self):
        super(Lists, self).__init__()
        self.total = 0

    def finalize(self):
        """Output the number of lists in the project."""
        print("Number of lists: %i" % self.total)

    def analyze(self, scratch):
        """Run and return the results of the Lists plugin."""
        self.total = len(scratch.lists)
        for x in scratch.sprites:
            self.total += len(x.lists)

class BlockCounts(HairballPlugin):

    """Plugin that keeps track of the number of blocks in a project."""

    def __init__(self):
        super(BlockCounts, self).__init__()
        self.blocks = 0

    def finalize(self):
        """Output the aggregate block count results."""
        print("Number of blocks %i" % self.blocks)

    def analyze(self, scratch):
        """Run and return the results from the BlockCounts plugin."""
        for script in self.iter_scripts(scratch):
            for b in self.iter_blocks(script.blocks):
                self.blocks += 1

class Colors(HairballPlugin):

    """Plugin that keeps track of the colors of the stage images."""

    def __init__(self):
        self.colors ={}

    def finalize(self):
        """Output the aggregate block count results."""
        print self.colors

    def compute_average_image_color(self, img):
        """
            Compute the most frequent color in img.
            Code adapted from 
            http://blog.zeevgilovitz.com/detecting-dominant-colours-in-python/
        """
        image = Image.open(img)
        w, h = image.size
        pixels = image.getcolors(w * h)
        most_frequent_pixel = pixels[0]
        for count, colour in pixels:
            if count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, colour)
        rgb = []
        for i in range(3):
            rgb.append (most_frequent_pixel[1][i])
        trgb = tuple(rgb)
        trgb = '#%02x%02x%02x' % trgb #Transform rgb to Hex color (HTML)
        return trgb

    def analyze(self, scratch):
        """Run and return the results from the BlockCounts plugin."""
        #ToDo: get the images from stage and characters