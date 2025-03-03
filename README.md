# Computational Programming - project - game
Randomized board game
# Rules
1. `k` players compete on a board with `N` fields (the smallest possible number of fields is 30).
2. When a board with more than 200 fields has been selected, you may choose an octagonal or hexagonal die. Otherwise, a hexagonal die is set by default.
3. To start from the starting field, players must roll an even number of dots, then they can roll the dice again and the result of the roll determines how many fields they will move.
4. The board has special fields that are randomly placed on the board:
   * Acceleration field - the player standing on this field moves 3 fields forward. Acceleration fields constitute 5% of all fields (rounded up).
   * Trap field - the player standing on this field moves back 2 fields. Trap fields are in play 7% of all fields (rounded up).
   * Return to start fields - a player who stands on this field must return to the starting field. Depending on the number N of fields that make up the board in the game, there are:
   * 2 return to start fields (when N > 200)
   * 1 return to start field (when N > 100)
   * 0 return to start fields (when N =< 100)
5. When a player draws the maximum number of points, they can throw again.
6. A player who stands on a field occupied by another player captures that player. The captured player must return to the starting field.
7. If, before reaching the start, a player rolls a number of points higher than the number needed to reach the finish line, the player moves back the number of points by which the finish line would be crossed.
8. The game is won by the player who reaches the finish line first.
9. The code runs the game 500 times and records the game results. It also calculates and reports which player won the most times and which player won the least times. The average number of turns it takes each player to reach the finish line is counted.
