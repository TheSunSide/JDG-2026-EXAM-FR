"""
Code de base pour l'algorithme de navigation dans les labyrinthes oniriques
AlgoriaLabs - Q1

Ce fichier contient la structure de base et les fonctions utilitaires.
Complétez les parties marquées TODO pour implémenter votre algorithme de recherche de chemin.
"""

import heapq
import time
import os
import re
from typing import List, Tuple, Optional

class Cell:
    def __init__(self):
      # Parent cell's row index
        self.parent_i = 0
    # Parent cell's column index
        self.parent_j = 0
 # Total cost of the cell (g + h)
        self.f = float('inf')
    # Cost from start to this cell
        self.g = float('inf')
    # Heuristic cost from this cell to destination
        self.h = 0

class DreamMaze:
    """Classe pour gérer le labyrinthe onirique et ses propriétés spéciales."""
    
    # Coûts de terrain
    TERRAIN_COSTS = {
        '.': 1.0,    # Terrain normal
        'S': 1.0,    # Point de départ
        'E': 1.0,    # Point d'arrivée
        '>': 0.3,    # Zone d'accélération
        '<': 3.0,    # Champ de ralentissement
        'P': 0.1,    # Portail de téléportation
        '#': float('inf')  # Mur temporal (infranchissable)
    }
    
    # Directions de déplacement (8-directionnelles)
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    def __init__(self, maze_file: str):
        """Initialise le labyrinthe à partir d'un fichier."""
        self.grid = []
        self.start = None
        self.end = None
        self.portals = {}  # Dict: position -> destination
        self.width = 0
        self.height = 0
        
        self.load_maze(maze_file)
    
    def load_maze(self, maze_file: str):
        """Charge le labyrinthe depuis un fichier."""
        try:
            with open(maze_file, 'r') as f:
                lines = f.readlines()
            
            # Première ligne contient les informations sur les portails
            portal_info = lines[0].strip()
            if portal_info.startswith("PORTALS:"):
                portal_data = portal_info[8:].strip()
                if portal_data:
                    # Format: (x1,y1)->(x2,y2) or multiple: (x1,y1)->(x2,y2),(x3,y3)->(x4,y4)
                    portal_pattern = r'\((\d+),(\d+)\)->\((\d+),(\d+)\)'
                    matches = re.findall(portal_pattern, portal_data)
                    for match in matches:
                        src_x, src_y, dst_x, dst_y = map(int, match)
                        self.portals[(src_x, src_y)] = (dst_x, dst_y)
            
            # Reste des lignes contient la grille
            grid_lines = lines[1:]
            self.grid = []
            
            for y, line in enumerate(grid_lines):
                row = list(line.strip())
                self.grid.append(row)
                
                for x, cell in enumerate(row):
                    if cell == 'S':
                        self.start = (x, y)
                    elif cell == 'E':
                        self.end = (x, y)
            
            self.height = len(self.grid)
            self.width = len(self.grid[0]) if self.grid else 0
            
        except FileNotFoundError:
            print(f"Erreur: Fichier {maze_file} non trouvé.")
            raise
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Vérifie si une position est valide dans la grille."""
        return 0 <= x < self.width and 0 <= y < self.height

    # Check if a cell is unblocked
    def is_unblocked(self, grid, row, col):
        return grid[row][col] == 1

    # Check if a cell is the destination
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    def get_terrain_cost(self, x: int, y: int) -> float:
        """Retourne le coût de déplacement pour une position donnée."""
        if not self.is_valid_position(x, y):
            return float('inf')
        
        cell = self.grid[y][x]
        return self.TERRAIN_COSTS.get(cell, 1.0)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """
        Retourne les voisins accessibles et leur coût de déplacement.
        
        Args:
            pos: Position actuelle (x, y)
            
        Returns:
            Liste de tuples (position_voisine, coût_déplacement)
        """
        x, y = pos
        neighbors = []
        
        if(self.grid[x,y] == 'P'):
            x, y = self.portals.get(x,y)

        for direction in self.DIRECTIONS:
            newPos = (direction[0]+x, direction[1]+y)
            neighbors.append((newPos, self.get_terrain_cost(newPos)))

        # TODO: Implémentez la logique pour gérer les portails et les coûts de terrain
        # Si vous ne pensez pas avoir besoin de cette fonction, vous pouvez l'ignorer.
        
        return neighbors
    
    def print_path_on_grid(self, path: List[Tuple[int, int]]):
        """Affiche la grille avec le chemin trouvé."""
        if not path:
            print("Aucun chemin à afficher.")
            return
        
        # Créer une copie de la grille
        display_grid = [row[:] for row in self.grid]
        
        # Marquer le chemin (sauf start et end)
        for i, (x, y) in enumerate(path):
            if (x, y) != self.start and (x, y) != self.end:
                display_grid[y][x] = '*'
        
        # Afficher la grille avec des espaces autour de chaque caractère
        print("\nGrille avec le chemin trouvé (* = chemin):")
        for row in display_grid:
            print(' '.join(row))


class PathfindingAlgorithm:
    """Classe principale pour l'algorithme de recherche de chemin."""
    
    def __init__(self, maze: DreamMaze):
        self.maze = maze

    def trace_path(self, cell_details, dest):
        print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
        print()
        return path

    
    def find_path(self) -> Tuple[Optional[List[Tuple[int, int]]], float]:
        """
        Trouve le chemin optimal du point de départ à l'arrivée.
        
        Returns:
            Tuple (chemin, coût_total) où:
            - chemin: Liste des coordonnées (x,y) du chemin optimal, ou None si aucun chemin
            - coût_total: Coût total du chemin trouvé
        """
        
        if not self.maze.start or not self.maze.end:
            print("Erreur: Point de départ ou d'arrivée non défini.")
            return None, float('inf')
        
        # TODO: Implémentez votre algorithme ici
        
        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.maze.width)] for _ in range(self.maze.height)]

        # Initialize the start cell details
        i = self.maze.start[0]
        j = self.maze.start[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            if(self.maze.grid[i][j] == 'P'):
                i, j = self.maze.portals.get(i,j)
            closed_list[i][j] = True

        
            for dir in self.maze.DIRECTIONS:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self.maze.is_valid_position(new_i, new_j) \
                    and not closed_list[new_i][new_j]:

                    # If the successor is the destination
                    if(self.maze.grid[new_i][new_j] == "E"):
                        print()

                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + self.maze.get_terrain_cost(new_i, new_j)
                    h_new = self.maze.calculate_h_value(new_i, new_j, self.maze.end)
                    f_new = g_new + h_new

                    if self.maze.is_destination(new_i, new_j, self.maze.end):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and print the path from source to destination
                        path = self.trace_path(cell_details, self.maze.end)
                        found_dest = True
                        return path, f_new
                    else:
                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            # Aucun chemin trouvé
            return None, float('inf')


def main():
    """Fonction principale pour tester l'algorithme."""
    try:
        # Charger le labyrinthe
        # TODO: Vous pouvez changer le nom du fichier pour tester d'autres labyrinthes
        script_dir = os.path.dirname(os.path.abspath(__file__))
        maze_file = os.path.join(script_dir, './dream_maze/dream_maze_20x20.txt')
        maze = DreamMaze(maze_file)
        
        print(f"Labyrinthe chargé: {maze.width}x{maze.height}")
        print(f"Départ: {maze.start}, Arrivée: {maze.end}")
        print(f"Portails: {maze.portals}")
        
        # Créer l'algorithme de recherche
        pathfinder = PathfindingAlgorithm(maze)
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        path, total_cost = pathfinder.find_path()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Afficher les résultats
        if path:
            print(f"\n=== SOLUTION TROUVÉE ===")
            print(f"Chemin: {path}")
            print(f"Coût total: {total_cost:.2f}")
            print(f"Nombre d'étapes: {len(path) - 1}")
            print(f"Temps d'exécution: {execution_time:.3f} secondes")
            
            # Afficher la grille avec le chemin
            maze.print_path_on_grid(path)
            
            # Validation du temps limite
            if execution_time > 10.0:
                print("⚠️ ATTENTION: Dépassement de la limite de temps (10 secondes)")
        else:
            print("❌ ÉCHEC: Aucun chemin trouvé")
    
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")


if __name__ == "__main__":
    main()