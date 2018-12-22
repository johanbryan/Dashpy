"""this import hairball plugins"""

from hairball.plugins import HairballPlugin
from collections import Counter
import kurt

class Dialogos(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Dialogos, self).__init__()
        self.color = ""
        self.comentario = "" 
        self.dialogos = 0

    def analyze(self,scratch):
        """cuenta los bloques say"""
        file_blocks = Counter()
        self.dialogos = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("say"):
                   self.dialogos += 1  
        print ('cantidad de dialogos registrados',self.dialogos)
        return 

    def finalize(self):
        if self.dialogos >= 3:
            self.color = "dark green"
            self.comentario = "Excelente"
        elif self.dialogos == 2:
            self.color = "light green"
            self.comentario = "Muy Bien"
        elif self.dialogos == 1:
            self.color = "yellow"
            self.comentario = "Bien"
        else:        
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color,self.comentario)    


class Eventos(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos eventos bloques de when
        retorna color amarillo si consigue un bloque when
        retorna color verde claro si consigue dos bloques when
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Eventos, self).__init__()
        self.color = ""
        self.comentario = "" 


    def analyze(self,scratch):
        """cuenta los bloques when"""
        file_blocks = Counter()
        eventos = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("when"):
                   eventos += 1  
        print ('cantidad de eventos registrados',eventos)
        return eventos

class Puntuacion(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Puntuacion, self).__init__()
        self.color = ""
        self.comentario = "" 


    def analyze(self,scratch):
        """cuenta los bloques change by"""
        file_blocks = Counter()
        puntuacion = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("change"):
                   puntuacion += 1  
        print ('cantidad de puntuacion registrados',puntuacion)
        if puntuacion > 0:
            print("si existe puntuacion entonces el criterio aplica")
        return puntuacion

class Acciones(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Acciones, self).__init__()
        self.color = ""
        self.comentario = "" 


    def analyze(self,scratch):
        """cuenta los bloques move"""
        file_blocks = Counter()
        acciones = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("move"):
                   acciones += 1  
        print ('cantidad de acciones registrados',acciones)
        return acciones

class Objetivo(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """

    def __init__(self):
        super(Objetivo, self).__init__()
        self.total = 0

    def finalize(self):
        """Output whether the project seems to end or not."""
        if self.total > 0:
            print "El juego persigue un Objetivo que lo finaliza"
        else:
            print "El juego no tiene un Objetivo claro que lo culmina"

    def analyze(self, scratch):
        """Run and return the results of the Ending plugin."""          
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == "stop %s":
                    self.total 
                    all_scripts = list(self.iter_scripts(scratch))

class Mecanica(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color dark green if it finds three or more characters with say
    """

    def __init__(self):
        super(Mecanica, self).__init__()
        self.backdropWhenGreenFlag = 0
        self.spritesHidden = []
        self.spritesShown = 0
        self.actions = []

    def finalize(self):
        """Output whether the project seems to have Mecanica instructions"""
        if (self.backdropWhenGreenFlag > 0 
            and len (self.spritesHidden) > 0
            and self.spritesShown >0
            and len(self.actions) > 0):
            print "El juego parace tener instruciones al comienzo"
        else:
            print "El juego no parece tener instruciones al comienzo"

    def backdropGreenFlag (self, all_scripts):
        """
            Check if a specific backdrop is displayed when green flag
        """
        backdropWhenGreenFlag = 0
        for script in all_scripts:
            if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                for name, _, block in self.iter_blocks(script.blocks):
                    if name == 'switch backdrop to %s':
                        backdropWhenGreenFlag = block.args[0].lower()
                        break
            if backdropWhenGreenFlag != 0:
                break
        return backdropWhenGreenFlag

    def getHiddenSprites (self, scratch):
        """
            Check if there are sprites that are hidden when green flag
        """
        spritesHidden = []
        for sprite in scratch.sprites:
            hide = 0
            wait = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                        for name, _, _ in self.iter_blocks(script.blocks):
                            if name == 'hide':
                                spritesHidden.append(sprite)
                                hide = 1
                            elif name == 'wait %s secs' and hide == 1:
                                wait = 1
                            elif name == 'show' and hide == 1 and wait == 1:
                                spritesHidden.remove(sprite)
        return spritesHidden

    def getActions (self, scratch):
        """
            Find messages sent or backdrops displayed or variables modified
            right after an user action (press key or mouse click)
        """
        actions = []
        for sprite in scratch.sprites:
            if sprite not in self.spritesHidden: 
                for script in sprite.scripts:
                    if (self.script_start_type(script) == self.HAT_MOUSE
                        or self.script_start_type(script) == self.HAT_KEY):
                        for name, _, block in self.iter_blocks(script.blocks):
                            if (name == 'switch backdrop to %s' 
                                or name == 'switch backdrop to %s and wait' 
                                or name == 'change %s by %s' 
                                or name == 'set %s to %s' 
                                #or name == 'when %s key pressed' 
                                or name == 'broadcast %s' 
                                or name == 'broadcast %s and wait'):
                                    actions.append(block.args[0].lower())
                    ### para aniadir vars modificadas tras un "si tecla x pulsada"
        for script in scratch.stage.scripts:
            if (self.script_start_type(script) == self.HAT_MOUSE
                or self.script_start_type(script) == self.HAT_KEY):
                for name, _, block in self.iter_blocks(script.blocks):
                    if (name == 'switch backdrop to %s' 
                        or name == 'switch backdrop to %s and wait'
                        or name == 'change %s by %s' 
                        or name == 'set %s to %s' 
                        #or name == 'when %s key pressed' 
                        or name == 'broadcast %s' 
                        or name == 'broadcast %s and wait'):
                            actions.append(block.args[0].lower())
                    elif name =='next backdrop' and self.backdropWhenGreenFlag != 0:
                        backs = []
                        for back in scratch.stage.backgrounds:
                            backs.append(back.name.lower())
                        #print backs
                        if (backs.index(self.backdropWhenGreenFlag) + 1 < len (backs)):
                            actions.append(backs[backs.index(self.backdropWhenGreenFlag) + 1])
                        elif len(backs) > 0:
                            actions.append(backs[0])
        #ToDo: En ocasiones en lugar de "al presionar" se usa un "esperar hasta que tecla x pulsada"
        #ToDo: En ocasiones en lugar de "al hacer click sobre este objeto" se usa un "tocando mouse"
        return actions

    def getShownSprites (self, scratch):
        """
            Check if there are sprites that are shown after one of the actions
        """
        spritesShown = 0
        for sprite in scratch.sprites:
            if sprite in self.spritesHidden:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        if (self.script_start_type(script) == self.HAT_BACKDROP 
                            or self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE
                            or self.script_start_type(script) == self.HAT_KEY):
                            if script.blocks[0].args[0].lower() in self.actions:
                                for name, _, _ in self.iter_blocks(script.blocks):
                                    if name == 'show':
                                        spritesShown += 1
                                        break
                        #ToDo: comprobar que el show esta despues que la variable
                        elif self.script_start_type(script) == self.HAT_GREEN_FLAG:
                            variableAction = 0
                            show = 0
                            for name, _, block in self.iter_blocks(script.blocks):
                                if name == '%s' and block.args[0].lower() in self.actions:
                                    variableAction += 1
                                    break
                                elif name == 'show':
                                    spritesShown += 1
                            if variableAction > 0 and show > 0:
                                spritesShown += 1
                        #ToDo: check if clones are created after action, and clones are in turn shown
        return spritesShown

    def analyze(self, scratch):
        """Run and return the results of the Mecanica plugin."""          
        all_scripts = list(self.iter_scripts(scratch))
        self.backdropWhenGreenFlag = self.backdropGreenFlag(all_scripts)
        self.spritesHidden = self.getHiddenSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are hidden when launched
        self.actions = self.getActions(scratch)
        self.spritesShown = self.getShownSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are shown after actions

#class Personajes(HairballPlugin):
