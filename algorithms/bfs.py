from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (Breadth-First Search).

    Garante encontrar a solução com o menor número de movimentos,
    pois expande os nós nível a nível (custo uniforme = 1 por passo).
    """

    def search(self, initial: State) -> SearchResult:
        # Caso especial: estado inicial já é o objetivo
        if initial.is_goal:
            return SearchResult(solution=initial)

        # Fila FIFO — BFS expande nível por nível
        frontier: deque[State] = deque([initial])

        # Conjunto de estados já visitados (evita ciclos)
        visited: set = {initial}

        nodes_expanded = 0
        nodes_generated = 1          # o estado inicial já foi gerado
        max_frontier_size = 1

        while frontier:
            # Atualiza o tamanho máximo da fronteira
            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

            # Retira o próximo estado a expandir (FIFO → nível mais raso primeiro)
            current = frontier.popleft()
            nodes_expanded += 1

            # Gera todos os filhos do estado atual
            for neighbor in current.neighbors():
                nodes_generated += 1

                if neighbor.is_goal:
                    # Encontrou a solução — retorna imediatamente
                    return SearchResult(
                        solution=neighbor,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=neighbor.cost,
                    )

                if neighbor not in visited:
                    visited.add(neighbor)
                    frontier.append(neighbor)

        # Fronteira esgotada sem encontrar solução
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
