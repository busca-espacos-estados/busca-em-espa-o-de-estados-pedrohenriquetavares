from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade (Depth-Limited DFS).

    Sem o limite, a DFS pode entrar em ciclos infinitos no 8-puzzle.
    O limite padrão de 50 é bem maior do que o pior caso ótimo (~31 movimentos),
    então ainda encontra soluções, mas não gasta memória/tempo com caminhos absurdamente longos.

    Atenção: DFS NÃO garante a solução ótima (menor custo).
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # Caso especial: estado inicial já é o objetivo
        if initial.is_goal:
            return SearchResult(solution=initial)

        # Pilha LIFO — DFS vai fundo primeiro
        # Cada entrada é o estado a explorar
        frontier: list[State] = [initial]

        # Conjunto de estados já visitados para evitar ciclos
        visited: set = {initial}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

            # Retira o topo da pilha (mais profundo primeiro)
            current = frontier.pop()
            nodes_expanded += 1

            # Respeita o limite de profundidade
            if current.cost >= self.depth_limit:
                continue

            # Gera filhos em ordem inversa para manter a ordem
            # natural de exploração (LEFT antes de RIGHT, etc.)
            for neighbor in reversed(current.neighbors()):
                nodes_generated += 1

                if neighbor.is_goal:
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

        # Sem solução dentro do limite de profundidade
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
