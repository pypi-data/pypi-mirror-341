
from typing import Dict, Callable, Any, Union, List, Tuple


# Tipos genéricos para os nós (suportando diferentes retornos)
NodeFunction = Callable[[Dict[str, Any]], Union[Dict[str, Any], List, Tuple[str, Any]]]


class JesusGraphCORE:
    """
    Framework para orquestração de fluxos baseado em grafos.
    
    O JesusGraph permite criar fluxos de processamento conectando nós
    que representam tarefas. Cada nó recebe um estado (blessing) e produz atualizações
    dessa blessing para cada funçao (que pode ser um agente IA, por exemplo).

    """

    def __init__(self):
        """
            (Esse é o construtor - Ele vai Inicializa um novo grafo de processamento.
            
            Cria um grafo vazio com nós.
            O grafo mantém um dicionário [Dict] de estado (as blessing) que será passado entre os nós
            durante a execução.
            
            Attributes:
                nodes: Mapeamento de nomes para funções de processamento

        """
        self.nodes: Dict[str, NodeFunction] = {}

    def add_node(self, name: str, function: NodeFunction):
        """
        Adiciona um nó ao grafo.

        Args:
            name (str): Nome do nó.
            function (NodeFunction): Função que sera executado no orquestrador - que representa o nó.

        """
        self.nodes[name] = function

    def connect(self, node_source: str, node_target: str):
        """
        Conecta dois nós no grafo.

        Args:
            node_source (str): Nome do nó de origem.
            node_target (str): Nome do nó de destino.

        """
        return self
