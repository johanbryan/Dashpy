from collections import Counter
import kurt
from hairball.plugins import HairballPlugin

class Drawing(HairballPlugin):
    """This class provides plugins for Fascinating Animate Drawing criterias
    from PRG (Progracademy) inspired on code.org challenges."""

    COLOR_BLOCK = ['set pen color to %s',
                   'change pen color by %s',
                   'set pen color to %s']

    POSITION_BLOCK = ['move %s steps',
                      'go to x:%s y:%s',
                      'go to %s',
                      'glide %s secs to x:%s y:%s',
                      'change x by %s',
                      'set x to %s',
                      'change y by %s',
                      'set y to %s']

    ORIENTATION_BLOCK = ['turn @turnRight %s degrees',
                         'turn @turnLeft %s degrees',
                         'point in direction %s',
                         'point towards %s']

    MOTION_BLOCK = POSITION_BLOCK + ORIENTATION_BLOCK

    LOOP_BLOCK = ['repeat until %s%s',
                  'repeat %s%s',
                  'forever%s']

    GEOMETRIC_LOOP_PATTERN = ['repeat until %s%s',
                              'repeat %s%s']

    GEOMETRIC_POSITION_PATTERN = ['move %s steps']

    GEOMETRIC_ORIENTATION_PATTERN = ['turn @turnRight %s degrees',
                                     'turn @turnLeft %s degrees',
                                     'point in direction %s']

    GEOMETRIC_BLOCK = GEOMETRIC_LOOP_PATTERN + GEOMETRIC_POSITION_PATTERN + GEOMETRIC_ORIENTATION_PATTERN
    GEOMETRIC_ANGLE_PATTERN = 360

    def __init__(self):
        """Construct method"""
        super(Drawing, self).__init__()
        self.__final_result = {}

    def analyze(self, scratch, **kwargs):
        """Run and return the results from the Drawing plugins."""
        #Variable
        block_list = {}
        script_number = 0
        #Extrae los scripts del proyecto Scratch
        for script in self.iter_scripts(scratch):
            script_number += 1
            block_list[script_number] = []
            if self.script_start_type(script) != self.NO_HAT:
                #Extrae los bloques de cada script del proyecto
                for name, _, block in self.iter_blocks(script.blocks):
                    block_list[script_number].append((name, block))
        #Run plugins
        if block_list:
            self.__final_result['Use Of Color'] = self.__analyzeUseOfColor(block_list)
            self.__final_result['Move Of Artist'] = self.__analyzeMoveOfArtist(block_list)
            self.__final_result['Nested Loop'] = self.__analyzeNestedLoop(block_list)
            self.__final_result['Geometric Figure'] = self.__analyzeGeometricFigure(block_list)

    def finalize(self):
        """Print in command prompt the final results"""
        if self.__final_result:
            #Variable
            score = reduce(lambda a, b: a+b, self.__final_result.values())
            #Evalutes the range score of Scratch project
            self.__final_result['Score'] = score
            self.__final_result['Error'] = 'None'
        else:
            self.__final_result['Score'] = 0
            self.__final_result['Error'] = 'File does not exist or contain a Scratch project'

        self.__final_result['Max Score'] = 12
        
        #Print final result
        print self.__final_result

    #_____________PRIVATE METHODS_____________#
    def __analyzeUseOfColor(self, block_list):
        """Plugin that checks if a Scrath project uses at least two colors."""
        #Variable
        argument_result = Counter()
        #Valida si uno de los bloques coincide con los de COLOR_BLOCK.
        #Si coincide almacena los parametros del bloque en argument_results
        for row in block_list.keys():
            for name, block in block_list[row]:
                for target in self.COLOR_BLOCK:
                    if target in name:
                        argument_result[str(block.args)] += 1
        #Evalua si el proyecto cumple el criterio Color
        if len(argument_result) > 3:
            return 3
        return len(argument_result)

    def __analyzeMoveOfArtist(self, block_list):
        """Plugin that checks if a Scratch project contains motion blocks with different arguments"""
        #Variables
        block_result = Counter()
        argument_result = {}
        #Set argument_result
        for block in self.MOTION_BLOCK:
            argument_result[block] = Counter()
        #Valida si uno de los bloques coincide con los de MOVE_BLOCK.
        #Si coincide almacena el bloque en block_result y los parametros en argument_result
        for row in block_list.keys():
            for name, block in block_list[row]:
                for target in self.MOTION_BLOCK:
                    if target in name:
                        block_result[name] += 1
                        argument_result[name][str(block.args)] += 1
        #Evalua si el proyecto cumple el criterio Movimiento
        if(block_result):
            if set(block_result.keys()) & set(self.POSITION_BLOCK) and set(block_result.keys()) & set(self.ORIENTATION_BLOCK):
                if self.__differentArgument(argument_result):
                    return 3
                return 2
            return 1
        return 0

    def __differentArgument(self, argument_result):
        """Check number of different arguments per motion block.
        If at least two motion blocks contains two or more different arguments
        then return True, else return False."""
        block_number = 0
        for key_block in argument_result.keys():
            if len(argument_result[key_block]) > 1:
                block_number += 1
        return (block_number > 1)

    def __analyzeNestedLoop(self, block_list):
        """Plugin that checks if a Scratch project contain nested loops"""
        #Variable
        contain_loop = False
        nested_loop_number = 0
        #Valida si uno de los bloques coincide con los de LOOP_BLOCK.
        #Si coincide busca en los argumentos del bloque otra coincidencia o
        #un CustomBlockType que contenga otra coincidencia
        for row in block_list.keys():
            for name, block in block_list[row]:
                for target in self.LOOP_BLOCK:
                    if target in name:
                        contain_loop = True
                        nested_loop_number += self.__containNormalLoop(block_list, block.args)
        #Evalua si el proyecto cumple el criterio Bucle Anidado
        if contain_loop:
            if nested_loop_number > 2:
                return 3
            return nested_loop_number + 1
        return 0

    def __containNormalLoop(self, block_list, argument_list):
        """Check if a loop contain loops"""
        try:
            for argument in argument_list[1]:
                if hasattr(argument, '__getitem__'):
                    argument_list = argument
                    argument = argument[0]
                if isinstance(argument, kurt.Block):
                    if argument.type.text in self.LOOP_BLOCK:
                        return 1
                    if isinstance(argument.type, kurt.CustomBlockType):
                        result = self.__containCustomLoop(block_list, argument.type.text.replace(' %s', ''))
                        #If doesn't find a loop inside then continue iterating
                        if result == 1:
                            return result
        except TypeError:
            self.__final_result['Warning'] = 'Scratch project contain empty loops'
        return 0

    def __containCustomLoop(self, block_list, target):
        """Check if a CustomBlockType contain loops"""
        for row in block_list.keys():
            #Check if first block of script row match with the target block
            if target in block_list[row][0][1].stringify():
                for name, block in block_list[row]:
                    for loop_block in self.LOOP_BLOCK:
                        if loop_block in name:
                            return 1
                    if isinstance(block.type, kurt.CustomBlockType) and target != block.type.text.replace(' %s', ''):
                        result = self.__containCustomLoop(block_list, block.type.text.replace(' %s', ''))
                        #If doesn't find a loop inside then continue iterating
                        if result == 1:
                            return result
        return 0

    def __analyzeGeometricFigure(self, block_list):
        """Check if a Scratch project contain basic geometric figures"""
        #Variable
        contain_geometric_block = False
        geometric_figure_number = 0
        #Search geometric figure patterns trough loops
        for row in block_list.keys():
            for name, block in block_list[row]:
                for target in self.GEOMETRIC_LOOP_PATTERN:
                    if target in name:
                        geometric_figure_number += self.__containGeometricFigurePattern(block_list, block.args)
                if not contain_geometric_block:
                    for target in self.GEOMETRIC_BLOCK:
                        if target in name:
                            contain_geometric_block = True
                            break
        #Evalua si el proyecto cumple el criterio Figura Geometrica
        if contain_geometric_block:
            if geometric_figure_number > 2:
                return 3
            return geometric_figure_number + 1
        return 0

    def __containGeometricFigurePattern(self, block_list, argument_list):
        """Search geometric figure patterns trough loops"""
        #Variable
        pattern = {'loop_angle' : 0,
                   'angle' : 0,
                   'orientation' : False,
                   'position' : False}
        try:
        #Check argument of loop
            if isinstance(argument_list[0], int):
                pattern['loop_angle'] = argument_list[0]
            #Iteration
            for argument in argument_list[1]:
                if isinstance(argument, kurt.Block):
                    if argument.type.text in self.GEOMETRIC_POSITION_PATTERN:
                        pattern['position'] = True
                    if argument.type.text in self.GEOMETRIC_ORIENTATION_PATTERN:
                        pattern['orientation'] = True
                        if pattern['loop_angle'] and isinstance(argument.args[0], int):
                            pattern['angle'] += argument.args[0]
                    if isinstance(argument.type, kurt.CustomBlockType):
                        pattern = self.__containCustomGeometricFigurePattern(block_list, pattern, argument.type.text.replace(' %s', ''))
            if pattern['orientation'] and pattern['position']:
                if not pattern['loop_angle'] or pattern['loop_angle'] * pattern['angle'] >= self.GEOMETRIC_ANGLE_PATTERN:
                    return 1
        except TypeError:
            self.__final_result['Warning'] = 'Scratch project contain empty loops'
        return 0

    def __containCustomGeometricFigurePattern(self, block_list, pattern, target):
        """Search geometric figure patterns trough CustomBlockType"""
        for row in block_list.keys():
            #Check if first bock of script row match with the target block
            if target in block_list[row][0][1].stringify():
                for name, block in block_list[row]:
                    for position_block in self.GEOMETRIC_POSITION_PATTERN:
                        if position_block in name:
                            pattern['position'] = True
                    for orientation_block in self.GEOMETRIC_ORIENTATION_PATTERN:
                        if orientation_block in name:
                            pattern['orientation'] = True
                            if pattern['loop_angle'] and isinstance(block.args[0], int):
                                pattern['angle'] += block.args[0]
                    if isinstance(block.type, kurt.CustomBlockType) and target != block.type.text.replace(' %s', ''):
                        pattern = self.__containCustomGeometricFigurePattern(block_list, pattern, block.type.text.replace(' %s', ''))
        return pattern
