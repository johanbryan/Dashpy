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
        for sprite in scratch.sprites:
            self.total += len(sprite.variables)

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
        for sprite in scratch.sprites:
            self.total += len(sprite.lists)

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
            for block in self.iter_blocks(script.blocks):
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

class Ending(HairballPlugin):

    """Plugin that checks if the project seems to end."""

    def __init__(self):
        super(Ending, self).__init__()
        self.total = 0

    def finalize(self):
        """Output whether the project seems to end or not."""
        if self.total > 0:
            print "The game seems to end at some point"
        else:
            print "The game seems to not ever end"

    def analyze(self, scratch):
        """Run and return the results of the Ending plugin."""          
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == "stop %s":
                    self.total
                    all_scripts = list(self.iter_scripts(scratch))

class Beginning(HairballPlugin):

    """
        Plugin that checks if the project seems to show instructions or a menu
        when the project is launched.
    """

    def __init__(self):
        super(Beginning, self).__init__()
        self.backdropWhenGreenFlag = 0
        self.spritesHidden = 0
        self.spritesShown = 0
        self.actions = []

    def finalize(self):
        """Output whether the project seems to have beginning instructions"""
        if (self.backdropWhenGreenFlag > 0 
            and self.spritesHidden > 0
            and self.spritesShown >0
            and len(self.actions) > 0):
            print "The game seems to present instructions or a menu when launched"
        else:
            print "The game seems to NOT present instructions or a menu when launched"

    def backdropGreenFlag (self, all_scripts):
        #Check if a specific backdrop is displayed when green flag
        backdropWhenGreenFlag = 0
        for script in all_scripts:
            if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                for name, _, _ in self.iter_blocks(script.blocks):
                    if name == 'switch backdrop to %s':
                        backdropWhenGreenFlag = 1
                        break
            if backdropWhenGreenFlag == 1:
                break
        return backdropWhenGreenFlag

    def analyze(self, scratch):
        """Run and return the results of the Beginning plugin."""          
        all_scripts = list(self.iter_scripts(scratch))
        self.backdropWhenGreenFlag = self.backdropGreenFlag(all_scripts)
        print self.backdropWhenGreenFlag

