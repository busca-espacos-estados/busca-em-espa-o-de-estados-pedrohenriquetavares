from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Movimentos possíveis: (nome_da_ação, deslocamento_no_índice)
# O tabuleiro é uma lista de 9 posições:
#   0 1 2
#   3 4 5
#   6 7 8
#
# Mover a peça para CIMA significa que o espaço vazio (0) sobe,
# ou seja, a peça de baixo dele desce para onde o 0 estava.
# Convenção: a ação descreve para onde o ESPAÇO VAZIO se move.

MOVES = {
    "UP":    -3,   # espaço sobe (troca com a peça que está 3 posições antes)
    "DOWN":  +3,   # espaço desce
    "LEFT":  -1,   # espaço vai para a esquerda
    "RIGHT": +1,   # espaço vai para a direita
}

# Restrições de borda: evita "saltar" de uma coluna para outra
# LEFT não é permitido se o espaço está na coluna 0 (índices 0, 3, 6)
# RIGHT não é permitido se o espaço está na coluna 2 (índices 2, 5, 8)
LEFT_BORDER  = {0, 3, 6}
RIGHT_BORDER = {2, 5, 8}


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(
        self,
        tiles: Tuple[int, ...],
        parent: Optional["State"] = None,
        action: Optional[str] = None,
        cost: int = 0,
    ):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    # ------------------------------------------------------------------
    # Propriedades básicas
    # ------------------------------------------------------------------

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    # ------------------------------------------------------------------
    # TODO implementados
    # ------------------------------------------------------------------

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        children = []
        blank = self.blank_index

        for action, delta in MOVES.items():
            # Verificação de borda para movimentos laterais
            if action == "LEFT" and blank in LEFT_BORDER:
                continue
            if action == "RIGHT" and blank in RIGHT_BORDER:
                continue

            new_blank = blank + delta

            # Verificação de limites do tabuleiro (para UP/DOWN)
            if new_blank < 0 or new_blank > 8:
                continue

            # Troca o espaço vazio com a peça vizinha
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_blank] = new_tiles[new_blank], new_tiles[blank]

            children.append(
                State(
                    tiles=tuple(new_tiles),
                    parent=self,
                    action=action,
                    cost=self.cost + 1,
                )
            )

        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        states = []
        current = self
        while current is not None:
            states.append(current)
            current = current.parent
        states.reverse()   # do inicial até o atual
        return states

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        # O estado inicial não tem ação; pulamos o primeiro elemento
        return [state.action for state in self.path() if state.action is not None]

    # ------------------------------------------------------------------
    # Comparação / hash / representação
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
