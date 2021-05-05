#!/usr/bin/env python3

from pnr.hola import adaptagrams as ag

router = ag.Router(ag.PolyLineRouting)
p1 = ag.Point(20, 35)
p2 = ag.Point(40, 12)
rect1 = ag.AvoidRectangle(p1, p2)


shaperef = ag.ShapeRef(router, rect1)
position = shaperef.position()
print("x: {}, y: {}".format(position.x, position.y))

graph = ag.Graph()
print(graph)


node1 = graph.addNode(5, 5)
node2 = graph.addNode(5, 5)
node3 = graph.addNode(5, 5)
node4 = graph.addNode(5, 5)

print("Printing Positions:")


print(node1.id())
bb = node1.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node2.id())
bb = node2.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node3.id())
bb = node3.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node4.id())
bb = node4.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)

edge1 = graph.addEdge(node1.id(), node2.id())


edge2 = graph.addEdge(node3, node4)

edge3 = graph.addEdge(node2, node3)

print(edge2)
# print(edge2.id)

print("isTREE ?: ", graph.isTree())
print("#nodes: ", graph.getNumNodes())
print("#edges: ", graph.getNumEdges())

# acalayout = ag.ACALayout(graph)

# acalayout.layout()

ag.doHOLA(graph)


print(node1.id())
bb = node1.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node2.id())
bb = node2.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node3.id())
bb = node3.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
print(node4.id())
bb = node4.getBoundingBox()
print(bb.x, bb.y, bb.X, bb.Y)
