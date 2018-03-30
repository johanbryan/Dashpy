from collections import Counter

import kurt
from hairball.plugins import HairballPlugin

class Drawing(HairballPlugin): 
    """This class provides plugins for Fascinating Animate Drawing criterias 
    from PRG (Progracademy) inspired on code.org challenges."""

    MAX_USEOFCOLOR_SCORE = 2
    MAX_MOVEOFARTIST_SCORE = 6
    MAX_NESTEDLOOP_SCORE = 6
    MAX_GEOMETRICFIGURE_SCORE = 6

    MAX_SCORE = MAX_USEOFCOLOR_SCORE + MAX_MOVEOFARTIST_SCORE + MAX_NESTEDLOOP_SCORE + MAX_GEOMETRICFIGURE_SCORE

    RANGE_NAME = ['Basic', 'Developing', 'Proficiency']

    DIFFICULTY = 0.5 #0 = Easy, 0.5 = Normal, 1 = Hard
    LEVEL_RANGE = float(MAX_SCORE)/len(RANGE_NAME)


    COLOR_BLOCK = ['set pen color to %s', 
                   'change pen color by %s',
                   'set pen color to %s']

    def __init__(self):
        """Construct method"""
        super(Drawing, self).__init__()
        self.__final_result = {}

    def analyze(self, scratch):
        """Run and return the results from the Drawing plugins."""
        self.__final_result['Use Of Color'] = self.__analyzeUseOfColor(scratch)
        #self.__final_result['Move Of Artist'] = self.__analyzeMoveOfArtist(scratch)
        #self.__final_result['Nested Loop'] = self.__analyzeNestedLoop(scratch)
        #self.__final_result['Geometric Figure'] = self.__analyzeGeomtricFigure(scratch)

    def finalize(self):
        """Print in command prompt the final results"""
        #Variables
        score = reduce(lambda a,b: a+b, self.__final_result.values())
        #Evalutes the range score of Scratch project
        self.__final_result['Score'] = score
        self.__final_result['Max Score'] = self.MAX_SCORE
        self.__final_result['Range'] = self.RANGE_NAME[int(score / self.LEVEL_RANGE + self.DIFFICULTY - 1)]
        print self.__final_result
    
    #_____________PRIVATE METHODS_____________#
    def __analyzeUseOfColor(self, scratch):
        """Plugin that checks if a Scrath Project uses at least two colors."""
        #Variables
        block_result = Counter()
        argument_result = Counter()
        #Extrae los scripts del proyecto Scratch
        for script in self.iter_scripts(scratch):
            if self.script_start_type(script) != self.NO_HAT:
                #Extrae los bloques de cada script del proyecto
                for name, _, block in self.iter_blocks(script.blocks):
                    #Valida si uno de los bloques coincide con los almacenados en COLOR_BLOCK. 
                    #Si coincide almacena el bloque en block_results y los parametros del bloque en argument_results
                    for color in self.COLOR_BLOCK:
                        if color in name:
                            block_result[name] += 1
                            if isinstance(block.args[0], kurt.Color):
                                argument_result[block.args[0].stringify()] += 1
                            else:
                                argument_result[True] += 1
        #Evalua si el proyecto cumple el criterio Color
        if block_result:
            if len(argument_result) == 1:
                return self.MAX_USEOFCOLOR_SCORE / 2
            else:
                return self.MAX_USEOFCOLOR_SCORE
        else:
            return 0