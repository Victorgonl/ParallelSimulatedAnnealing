from typing import List

from .item import Item


class Mochila:
    def __init__(self, capacidade: int):
        self.capacidade = capacidade
        self.itens: List[Item] = []


    def adicionar_item(self, item: Item) -> None:
        for item_mochila in self.itens:
            if item_mochila.id == item.id:
                return False
        if item.peso + self.peso() <= self.capacidade:
            self.itens.append(item)
            return True
        return False


    def remover_item(self, item: Item) -> None:
        self.itens.remove(item)


    def peso(self) -> float:
        return sum([item.peso for item in self.itens])
