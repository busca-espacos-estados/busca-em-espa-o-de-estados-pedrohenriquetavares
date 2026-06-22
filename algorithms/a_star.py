import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

# Posição objetivo de cada peça no tabuleiro resolvido:
#   GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
#   Índices:  0  1  2  3  4  5  6  7  8
#
# Para calcular a distância de Manhattan precisamos saber onde
# cada peça DEVERIA estar.  Pré-computamos isso uma vez:
#   peça 1 → linha 0, coluna 0
#   peça 2 → linha 0, coluna 1
#   ...
#   peça 0 → linha 2, coluna 2  (não usamos o espaço vazio na heurística)

GOAL_POSITION = {}
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
for idx, val in enumerate(GOAL_STATE):
    GOAL_POSITION[val] = (idx // 3, idx % 3)   # (linha, coluna)


class AStar(BaseSearch):
    """Busca A* com heurística da distância de Manhattan.

    A distância de Manhattan é ADMISSÍVEL porque nunca superestima o custo real:
    cada peça precisa de pelo menos |Δlinha| + |Δcoluna| movimentos para chegar
    à sua posição objetivo, mesmo sem obstáculos.

    Por ser admissível, A* garante encontrar a solução ÓTIMA.
    """

    def heuristic(self, state: State) -> int:
        """Soma das distâncias de Manhattan de cada peça até sua posição objetivo."""
        total = 0
        for idx, val in enumerate(state.tiles):
            if val == 0:
                continue   # o espaço vazio não conta
            goal_row, goal_col = GOAL_POSITION[val]
            curr_row, curr_col = idx // 3, idx % 3
            total += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        # f(n) = g(n) + h(n)
        #   g(n) = custo acumulado até n (= número de movimentos = state.cost)
        #   h(n) = estimativa heurística até o objetivo
        #
        # O heap armazena tuplas (f, contador, state) — o contador é um
        # desempate para evitar comparação direta entre State quando f é igual.

        if initial.is_goal:
            return SearchResult(solution=initial)

        h0 = self.heuristic(initial)
        counter = 0   # desempate único e crescente

        # (f, contador, estado)
        frontier: list = []
        heapq.heappush(frontier, (h0, counter, initial))

        # Mapa: estado → menor f já registrado (para evitar reprocessar estados piores)
        best_f: dict[State, int] = {initial: h0}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

            f, _, current = heapq.heappop(frontier)
            nodes_expanded += 1

            # Se encontramos o objetivo, reconstruímos o caminho
            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            # Ignora se já encontramos um caminho melhor para este estado
            if f > best_f.get(current, float("inf")):
                continue

            for neighbor in current.neighbors():
                nodes_generated += 1
                g = neighbor.cost
                h = self.heuristic(neighbor)
                f_new = g + h

                if f_new < best_f.get(neighbor, float("inf")):
                    best_f[neighbor] = f_new
                    counter += 1
                    heapq.heappush(frontier, (f_new, counter, neighbor))

        # Sem solução
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
