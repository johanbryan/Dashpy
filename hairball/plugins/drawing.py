"""This module provides plugins for Fascinating Animate Drawing criterias 
from PRG (Progracademy) inspired on code.org challenges."""

import kurt

from collections import Counter
from hairball.plugins import HairballPlugin

class Color(HairballPlugin): 
    """Plugin that checks if a Scrath Project uses at least two colors."""

    COLOR_BLOCK = ['set pen color to %s', 
                   'change pen color by %s',
                   'set pen color to %s']

    def __init__(self):
        super(Color, self).__init__()
        self.__block_result = Counter()
        self.__argument_result = Counter()
        self.__final_result = {'color' : 0}

    def analyze(self, scratch):
        """Run and return the results from the Color plugin."""
        #Extrae los scripts del proyecto Scratch
        for script in self.iter_scripts(scratch):
            if self.script_start_type(script) != self.NO_HAT:
                #Extrae los bloques de cada script del proyecto
                for name, _, block in self.iter_blocks(script.blocks):
                    #Valida si uno de los bloques coincide con los almacenados en COLOR_BLOCK. 
                    #Si coincide almacena el bloque en block_results y los parametros del bloque en argument_results
                    for color in self.COLOR_BLOCK:
                        if color in name:
                            self.__block_result[name] += 1
                            if isinstance(block.args[0], kurt.Color):
                                self.__argument_result[block.args[0].stringify()] += 1
                            else:
                                self.__argument_result[True] += 1
        #Evalua si el proyecto cumple el criterio Color
        if self.__block_result:
            if len(self.__argument_result.items()) == 1:
                self.__final_result['color'] = 1
            if len(self.__argument_result.items()) >= 2:
                self.__final_result['color'] = 2
        
    def finalize(self):
        print self.__final_result, self.__block_result, self.__argument_result
        
        