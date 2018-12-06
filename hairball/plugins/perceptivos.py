"""this import hairball plugins"""

from hairball.plugins import HairballPlugin

class MecanicaExplicativa(HairballPlugin):
    """
        Este  plugin verifica y cuenta cuantos textos de dialogo informativo existe al inicio de el videojuego
        retorna color amarillo si consigue uno
        retorna color verde claro si consigue dos
        retorna color verde oscuro si consigue 3 o más


        this plugin checks and counts how many blocks of informative texts at the start of the videogame
        returns color yellow if it finds one
        returns color light green if it finds two
        returns color dark green if it finds three or more

    """

    def __contartextos(self):


    def __retornarcolor(self):


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


    def __contardialogossay(self,scratch):
        if (file_blocks ["when %s"])
            print "consegui un valor"
        else   
            print "no consegui un dialogo"

    def __contardialogosbroadcast(self):

    def __retornarcolor(self):        