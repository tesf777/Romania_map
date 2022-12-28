
class Node:
  def __init__(self,state,parent,cost,straight=0):
    self.state = state
    self.parent = parent
    self.cost = cost
    self.straight = straight
  def __repr__(self):
    return self.state

class Vertex:
  def __init__(self,key,straight=0):
    '''初始化需要地名和目的地直线距离'''
    self.id = key
    self.connectedTo = {}
    self.straight = straight
  
  def add_neighbour(self,nbr,weight=0):
    '''添加相邻下一检查点和距离到字典'''
    self.connectedTo[nbr] = weight
  
  def __repr__(self):
    return str(self.id) + ' -> ' + str([x.id for x in self.connectedTo])
  
  def get_connections(self):
    '''返回该端点的所有下一检查点的id'''
    return self.connectedTo.keys()
  
  def get_id(self):
    return self.id


class Graph:
  def __init__(self):
    '''初始化图'''
    self.verList = {}
    self.numVertices = 0
  
  def add_vertex(self,key,straight=0):
    '''在图里新建端点类，加入端点列表'''
    self.numVertices += 1
    newVertex = Vertex(key,straight)
    self.verList[key] = newVertex
  
  def get_vertex(self,key):
    '''从图里寻找地名，返回端点类,没有返回none'''
    if key in self.verList:
      return self.verList[key]
    else:
      return None
  
  def __contains__(self,n):
    '''magic方法 定义in语句的作用'''
    return n in self.verList
  
  def add_edge(self,from_place,to_place,cost=0):
    '''端点与端点连线'''
    if from_place not in self.verList:
      raise Exception("undefined from_place")
    if to_place not in self.verList:
      raise Exception("undefined to_place")
    self.verList[from_place].add_neighbour(self.verList[to_place],cost)
    self.verList[to_place].add_neighbour(self.verList[from_place],cost) 
    
  def get_vertices(self):
    return self.verList.keys()
  
  def get_weight(self,nbr,ver):
    '''返回与下一检查点的距离'''
    return ver.connectedTo[self.get_vertex(nbr)]

  def __iter__(self):
    return iter(self.verList.values())

class StackFrontier:
  
  def __init__(self):
    self.frontier = [] 

  def push(self,node):
    self.frontier.append(node)

  def pop(self):
    if self.size() == 0:
      raise Exception("Empty Frontier")
    else:
      node = self.frontier[-1]
      self.frontier = self.frontier[:-1]
      return node

  def size(self):
    return len(self.frontier)

  def already_contain(self,state):
    return any(node.state == state for node in self.frontier)
  
  def show(self):
    return self.frontier

class QueueFrontier(StackFrontier):
  def enqueue(self,node):
    super().push(node)

  def dequeue(self):
    if self.size() == 0:
      raise Exception("Empty Frontier")
    else:
      node = self.frontier[0]
      self.frontier = self.frontier[1:]
      return node

  def cost_sort(self):
    return self.frontier.sort(key=lambda x:x.cost)

  def heuristic_sort(self):
    return self.frontier.sort(key=lambda x:x.straight)

  def heuristic_plus_sort(self):
    return self.frontier.sort(key=lambda x:(x.cost + x.straight))



# g = Graph()
# g.add_vertex('Arad')
# g.add_vertex('Bucharest')
# g.add_vertex('Craiova')
# g.add_vertex('Sibiu')
# print(g.verList)
# g.add_edge('Arad','Sibiu',140)
# g.add_edge('Arad','Bucharest',100)
# print(g.get_weight(g.get_vertex('Sibiu'),'Arad'))
#print(g.get_vertex('Sibiu').connectedTo[g.get_vertex('Arad')])
# for v in g:
#   for w in v.get_connections():
#     print("(%s , %s)" %(v.get_id(),w.get_id()))
# a = Node('Arad',None,100,None)
# b = Node('Sibiu',None,150,'a')
# c = Node('Demo',None,103,'b')
# d = Node('Cal',None,130,'c')
# e = Node('Esl',None,177,'d')
# print(a.action)
# print(b.action)
# print(c.action)
# l = QueueFrontier()
# l.frontier = [a,b,c,d,e]
# print(l.show())
# l.sort()
# print(l.show())
#print(a==b)
