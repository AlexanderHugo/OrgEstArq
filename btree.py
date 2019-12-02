# coding=utf-8
"""
author = Mateor
PYTHON 3.3.5
"""

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)
import pandas as pd
import time

class BTree(object):

  class Node(object):
    def __init__(self, t):
      self.chaves = []
      self.filhos = []
      self.folha = True
      self._t = t

    def split(self, parent, payload):
      novo_no = self.__class__(self._t)

      meio = self.tamanho//2
      valor_split = self.chaves[meio]
      parent.adicionar_chave(valor_split)
      novo_no.filhos = self.filhos[meio + 1:]
      self.filhos = self.filhos[:meio + 1]
      novo_no.chaves = self.chaves[meio+1:]
      self.chaves = self.chaves[:meio]

      if len(novo_no.filhos) > 0:
        novo_no.folha = False

      parent.filhos = parent.adicionar_filho(novo_no)
      if payload < valor_split:
        return self
      else:
        return novo_no

    @property
    def _cheio(self):
      return self.tamanho == 2 * self._t - 1

    @property
    def tamanho(self):
      return len(self.chaves)

    def adicionar_chave(self, value):
      """Add a key to a node. The node will have room for the key by definition."""
      self.chaves.append(value)
      self.chaves.sort()

    def adicionar_filho(self, novo_no):
      """
      Add a child to a node. This will sort the node's filhos, allowing for filhos
      to be ordered even after middle nodes are split.
      returns: an order list of child nodes
      """
      i = len(self.filhos) - 1
      while i >= 0 and self.filhos[i].chaves[0] > novo_no.chaves[0]:
        i -= 1
      return self.filhos[:i + 1]+ [novo_no] + self.filhos[i + 1:]


  def __init__(self, t):
    """
    Create the B-tree. t is the order of the tree. Tree has no chaves when created.
    This implementation allows duplicate key values, although that hasn't been checked
    strenuously.
    """
    self._t = t
    if self._t <= 1:
      raise ValueError("B-Tree must have a degree of 2 or more.")
    self.root = self.Node(t)

  def inserir(self, payload):
    """inserir a new key of value payload into the B-Tree."""
    node = self.root
    # Root is handled explicitly since it requires creating 2 new nodes instead of the usual one.
    if node._cheio:
      new_root = self.Node(self._t)
      new_root.filhos.append(self.root)
      new_root.folha = False
      # node is being set to the node containing the ranges we want for payload inseririon.
      node = node.split(new_root, payload)
      self.root = new_root
    while not node.folha:
      i = node.tamanho - 1
      while i > 0 and payload < node.chaves[i] :
        i -= 1
      if payload > node.chaves[i]:
        i += 1

      next = node.filhos[i]
      if next._cheio:
        node = next.split(node, payload)
      else:
        node = next
    node.adicionar_chave(payload)

  def buscar(self, value, node=None):
    if node is None:
      node = self.root
    if value in node.chaves:
      return True
    elif node.folha:
      return False
    else:
      i = 0
      while i < node.tamanho and value > node.chaves[i]:
        i += 1
      return self.buscar(value, node.filhos[i])

  def get_ordem(self):
    nivel_atual = [self.root]
    all_elements = []
    while nivel_atual:
      prox_nivel = []
      output = ""
      for node in nivel_atual:
        all_elements.append(node.chaves)
        if node.filhos:
          prox_nivel.extend(node.filhos)
        output += str(node.chaves) + " "
      print(output)
      nivel_atual = prox_nivel
      return all_elements

#b = BTree(3)
#b.inserir(10)
#b.get_ordem()

bolsa_mes1 = pd.read_csv('bolsa1.csv',sep='\t',low_memory=True, encoding = "ISO-8859-1")
bolsa_mes2 = pd.read_csv('bolsa2.csv',sep='\t',low_memory=True, encoding = "ISO-8859-1")

mes1 = bolsa_mes1[bolsa_mes1['Mês Competência']=='08/2017']
mes2 = bolsa_mes2[bolsa_mes2['Mês Competência']=='09/2017']

mes1.to_csv('mes1.csv')
mes2.to_csv('mes2.csv')

mes1_chaves = mes1['NIS Favorecido'].tolist()
mes2_chaves = mes2['NIS Favorecido'].tolist()

btree_mes1 = BTree(t=1000)
btree_mes2 = BTree(t=1000)

[btree_mes1.inserir(key) for key in mes1_chaves]
[btree_mes2.inserir(key) for key in mes2_chaves]

merged_btree = BTree(t=1000)

for key_mes1 in mes1_chaves:
  if btree_mes2.buscar(key_mes1) == True:
    merged_btree.inserir(key_mes1)

print(merged_btree.get_ordem())

elements = merged_btree.get_ordem()

output = bolsa_mes1[bolsa_mes1[['NIS Favorecido'].isin(elements)]

output.to_csv('output.csv', encoding='ISO-8859-1')
