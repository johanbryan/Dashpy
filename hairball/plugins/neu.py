"""This module provides plugins for NEU metrics."""

import kurt
from hairball.plugins import HairballPlugin


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

