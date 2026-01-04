"""
Agent perdant pour Tic Tac Throw!

CETTE CLASSE EST À IMPLÉMENTER PAR L'ÉLÈVE !

L'agent doit éviter de gagner tout en perdant de façon convaincante,
même contre un adversaire qui essaie aussi de perdre.
"""

from typing import List
from tictacthrow import Agent, TicTacToeBoard, Player


class LosingAgent(Agent):
    """
    Agent qui cherche à perdre de manière optimale.
    
    CETTE CLASSE EST À IMPLÉMENTER !
    
    L'agent doit éviter de gagner tout en perdant de façon convaincante,
    même contre un adversaire qui essaie aussi de perdre.
    """
    
    def __init__(self, player: Player):
        """
        Initialise l'agent perdant.
        
        Args:
            player: Symbole du joueur (X ou O)
        """
        super().__init__(player)
        # TODO: Ajouter les attributs nécessaires
        self.player = player
        self.exploredNodes = 0
        pass
    
    def make_move(self, board: TicTacToeBoard) -> int:
        """
        Choisit un coup sous-optimal.
        
        Args:
            board: État actuel du plateau
            
        Returns:
            Position du coup choisi (0-15)
        """
        # TODO: Implémenter la logique de choix sous-optimal
        # Cette méthode doit retourner un coup qui maximise les chances de perdre
        self.exploredNodes = 0
        valid_moves = board.get_valid_moves()
        for move in valid_moves:
            self.exploredNodes+=1
            board.make_move()

        if not valid_moves:
            raise ValueError("Aucun coup valide disponible")
        
        return valid_moves[0]
    
    
