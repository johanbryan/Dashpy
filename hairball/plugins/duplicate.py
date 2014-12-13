"""This module provides plugins for basic duplicate code detection."""

from hairball.plugins import HairballPlugin

class DuplicateScripts(HairballPlugin):

    """Plugin that keeps track of which scripts have been 
    used more than once whithin a project."""

    def __init__(self):
        super(DuplicateScripts, self).__init__()
        self.total_duplicate = 0
        self.list_duplicate = []

    def finalize(self):
        """Output the duplicate scripts detected."""
        if self.total_duplicate > 0:
            print("%d duplicate scripts found" % self.total_duplicate)
            for duplicate in self.list_duplicate:
                print duplicate

    def analyze(self, scratch):
        """Run and return the results from the DuplicateScripts plugin.
        Only takes into account scripts with more than 5 blocks"""
        scripts_set = set()
        for script in self.iter_scripts(scratch):
            #Scripts defined by user are not considered
            if script[0].type.text != 'define %s':  
                blocks_list = []
                for name, _, _ in self.iter_blocks(script.blocks):
                    blocks_list.append(name)
                blocks_tuple = tuple(blocks_list)
                if blocks_tuple in scripts_set:
                    if len(blocks_list)>5:
                        self.total_duplicate += 1
                        self.list_duplicate.append(blocks_list)
                else:
                    scripts_set.add(blocks_tuple)

