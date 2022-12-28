from util import Graph,Vertex,StackFrontier,QueueFrontier,Node
import pandas as pd

g = Graph() #建立图类
#从excel中导入图数据
df1 = pd.read_excel('Vertex.xlsx')
df2 = pd.read_excel('Connection.xlsx')
vertex_dict = df1.set_index('Vertex')['StraightLine'].to_dict()
# 创造端点
for i,j in vertex_dict.items():
  g.add_vertex(i,j)
# 建立连接
connect_iter = zip(df2['Vertex'],df2['Connection'],df2['Cost'])

for i,j,k in connect_iter:
  g.add_edge(i,j,k)

#print(g.verList) 尝试打印一下看看连对了吗

def not_in_graph(graph,place):
  '''便于判断没在图里的点'''
  if place not in graph.get_vertices():
    return True
  return False
#print(not_in_graph(g,'Arad'))

def DepthFirstSearch(graph,from_place,to_place):
  '''深度优先算法'''
  if not_in_graph(graph,from_place) or not_in_graph(graph,to_place):
    raise Exception("undefined place")
  '''建立第一个点'''
  node = Node(from_place,from_place,0)
  '''如果这个点是目的地就直接返回'''
  if node.state == to_place:
    return node
  '''建立边缘队列frontier，堆栈形式'''
  frontier = StackFrontier()
  frontier.push(node)
  '''创建探索集'''
  explore = StackFrontier()
  '''当边缘队列有结点时循环'''
  while frontier.size() != 0:
    print("开始时前沿队列",frontier.show())
    print("探索集:",explore.show())
    '''弹出栈顶的结点'''
    newnode = frontier.pop()
    
    print("弹出",newnode.state)
    '''放入探索集合'''
    explore.push(newnode)
  
    if newnode.state == to_place:
      print("Get it!")
      return newnode
    '''对当前结点生成后继结点'''
    for verNext in graph.verList[newnode.state].get_connections():#添加后继结点每一个元素都是vertex类
      name = verNext.get_id()
      '''对既不在边缘队列，又不在探索集合的端点生成结点类,加入边缘队列。防止无限循环'''
      '''加入边缘队列的方式决定了探索的顺序，深度优先就是堆栈，广度优先就是队列'''
      '''一致代价搜索是队列，但是队列的顺序按cost升序'''
      '''贪心最佳优先也是队列，顺序按启发函数(这里使用的是直线距离)升序'''
      '''A*也是队列，顺序按启发函数+直线距离升序'''
      if (not frontier.already_contain(name)) and (not explore.already_contain(name)):
        nodeNext = Node(name,[newnode.parent]+[name],newnode.cost + graph.get_weight(newnode.state,verNext))
        frontier.push(nodeNext)
        print("压入",nodeNext.state)
      
      if nodeNext.state == to_place:
        break
  if frontier.size() == 0:
    print("Cannot Find")
    return False
  return nodeNext
  



    
def BreadthFirstSearch(graph,from_place,to_place):
  '''广度优先搜索'''
  if not_in_graph(graph,from_place) or not_in_graph(graph,to_place):
    raise Exception("undefined place")

  node = Node(from_place,from_place,0)
  if node.state == to_place:
    return node
  frontier = QueueFrontier()
  frontier.push(node)
  explore = StackFrontier()
  
  while frontier.size() != 0:
    print("开始时前沿队列",frontier.show())
    print("探索集:",explore.show())
    newnode = frontier.dequeue()
    print("弹出",newnode.state)
    explore.push(newnode)
    if newnode.state == to_place:
      print("Get it!")
      return newnode
    
    for verNext in graph.verList[newnode.state].get_connections():#添加后继结点每一个元素都是vertex类
      name = verNext.get_id()
      if (not frontier.already_contain(name)) and (not explore.already_contain(name)):
        nodeNext = Node(name,[newnode.parent]+[name],newnode.cost + graph.get_weight(newnode.state,verNext))
        frontier.enqueue(nodeNext)
        print("压入",nodeNext.state)

      if nodeNext.state == to_place:
        break
  if frontier.size() == 0:
    print("Cannot Find")
    return False
  return nodeNext
  


def UniformCostSearch(graph,from_place,to_place):
  '''一致代价搜索'''
  if not_in_graph(graph,from_place) or not_in_graph(graph,to_place):
    raise Exception("undefined place")

  node = Node(from_place,from_place,0)
  if node.state == to_place:
    return node
  frontier = QueueFrontier()
  frontier.push(node)
  explore = StackFrontier()
  
  while frontier.size() != 0:
    print("开始时前沿队列",frontier.show())
    print("处理前沿队列，使其按cost升序")
    frontier.cost_sort()
    print("排序后前沿队列",frontier.show())
    print("探索集:",explore.show())
    newnode = frontier.dequeue()
    print("弹出",newnode.state)
    explore.push(newnode)
    if newnode.state == to_place:
      print("Get it!")
      return newnode
  
    
    for verNext in graph.verList[newnode.state].get_connections():#添加后继结点每一个元素都是vertex类
      name = verNext.get_id()
      if (not frontier.already_contain(name)) and (not explore.already_contain(name)):
        nodeNext = Node(name,[newnode.parent]+[name],newnode.cost + graph.get_weight(newnode.state,verNext))
        frontier.enqueue(nodeNext)
        print("压入",nodeNext.state)
      if nodeNext.state == to_place:
        break
  if frontier.size() == 0:
    print("Cannot Find")
    return False
  return nodeNext




def GreedyBestFirstSearch(graph,from_place,to_place):
  '''贪心最佳优先搜索'''
  if not_in_graph(graph,from_place) or not_in_graph(graph,to_place):
    raise Exception("undefined place")

  node = Node(from_place,from_place,0,graph.verList[from_place].straight)
  if node.state == to_place:
    return node
  frontier = QueueFrontier()
  frontier.push(node)
  explore = StackFrontier()
  
  while frontier.size() != 0:
    print("开始时前沿队列",frontier.show())
    print("处理前沿队列，使其按直线距离(启发函数)升序")
    frontier.heuristic_sort()
    print("排序后前沿队列",frontier.show())
    print("探索集:",explore.show())
    newnode = frontier.dequeue()
    print("弹出",newnode.state)
    explore.push(newnode)
    if newnode.state == to_place:
      print("Get it!")
      return newnode
    
    for verNext in graph.verList[newnode.state].get_connections():#添加后继结点每一个元素都是vertex类
      name = verNext.get_id()
      staright = verNext.straight
      if (not frontier.already_contain(name)) and (not explore.already_contain(name)):
        nodeNext = Node(name,[newnode.parent]+[name],newnode.cost + graph.get_weight(newnode.state,verNext),staright)
        frontier.enqueue(nodeNext)
        print("压入",nodeNext.state)
      if nodeNext.state == to_place:
        break
  if frontier.size() == 0:
    print("Cannot Find")
    return False
  return nodeNext



def A_StarSearch(graph,from_place,to_place):
  '''A*搜索'''
  if not_in_graph(graph,from_place) or not_in_graph(graph,to_place):
    raise Exception("undefined place")

  node = Node(from_place,from_place,0,graph.verList[from_place].straight)
  if node.state == to_place:
    return node
  frontier = QueueFrontier()
  frontier.push(node)
  explore = StackFrontier()
  
  while frontier.size() != 0:
    print("开始时前沿队列",frontier.show())
    print("处理前沿队列，使其按直线距离(启发函数)与cost之和升序")
    frontier.heuristic_plus_sort()
    print("排序后前沿队列",frontier.show())
    print("探索集:",explore.show())
    newnode = frontier.dequeue()
    print("弹出",newnode.state)
    explore.push(newnode)
    if newnode.state == to_place:
      print("Get it!")
      return newnode
    
    for verNext in graph.verList[newnode.state].get_connections():#添加后继结点每一个元素都是vertex类
      name = verNext.get_id()
      staright = verNext.straight
      if (not frontier.already_contain(name)) and (not explore.already_contain(name)):
        nodeNext = Node(name,[newnode.parent]+[name],newnode.cost + graph.get_weight(newnode.state,verNext),staright)
        frontier.enqueue(nodeNext)
        print("压入",nodeNext.state)
      if nodeNext.state == to_place:
        break
  if frontier.size() == 0:
    print("Cannot Find")
    return False
  return nodeNext


#finalnode = BreadthFirstSearch(g,'Zerind','Bucharest')

#finalnode = DepthFirstSearch(g,'Zerind','Bucharest')

#finalnode = UniformCostSearch(g,'Zerind','Bucharest')

#finalnode = GreedyBestFirstSearch(g,'Zerind','Bucharest')

finalnode = A_StarSearch(g,'Zerind','Bucharest')

print("该搜索选择的路径是：",finalnode.parent)
print("该搜索花费的代价是：",finalnode.cost)