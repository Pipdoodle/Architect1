import pygame
import math
from Point import Point
from Vector import Vector
#Note: sorta followed following tutorials:http://petercollingridge.appspot.com/3D-tutorial,https://gamedevelopment.tutsplus.com/tutorials/lets-build-a-3d-graphics-engine-points-vectors-and-basic-concepts--gamedev-8143

def rotate2D(a,b,theta,ca,cb):
    #rotates around center declared by ca and cb
    if ca>0 and cb>0:
        da=a-ca
        db=b-cb
        a=(da*math.cos(theta)-db*math.sin(theta))+ca
        b=(db*math.cos(theta)+da*math.sin(theta))+cb
    if ca<0 and cb<0:
        da=a+ca
        db=b+cb
        a=(da*math.cos(theta)-db*math.sin(theta))-ca
        b=(db*math.cos(theta)+da*math.sin(theta))-cb
    if ca>0 and cb<0:
        da=a-ca
        db=b+cb
        a=(da*math.cos(theta)-db*math.sin(theta))+ca
        b=(db*math.cos(theta)+da*math.sin(theta))-cb
    if ca<0 and cb>0:
        da=a+ca
        db=b-cb
        a=(da*math.cos(theta)-db*math.sin(theta))-ca
        b=(db*math.cos(theta)+da*math.sin(theta))+cb
    return a,b
    
class ThreeDObject(object):
    def __init__(self,nodes,edges,faces,color,cx,cy,cz):
        self.nodes=nodes
        self.edges=edges
        self.color=color
        self.depthfactor=100
        self.cy=cy
        self.cz=cz
        self.cx=cx
        
    
    def drawObject(self,screen,camx,camy,camz,rotx,roty,rotz,cx,cy,cz,color=None):
        self.depthfactor=100
        listValues=[]
        prcnodes=self.procesNodes(camx,camy,camz,rotx,roty,rotz,cx,cy,cz)
        if color!="None" and color!=None:
            for face in self.faces:
                listValues=[]
                n1=prcnodes[self.edges[face[0]][0]].x
                n2=prcnodes[self.edges[face[0]][0]].y
                listValues.append((n1,n2))
                for i in range(1,len(face)):
                    if self.edges[face[i]][0]!=self.edges[face[i-1]][1]:
                        self.edges[face[i]][0],self.edges[face[i]][1]=self.edges[face[i]][1],self.edges[face[i]][0]
                    n1=prcnodes[self.edges[face[i]][0]].x
                    n2=prcnodes[self.edges[face[i]][0]].y
                    listValues.append((n1,n2))
                pygame.draw.polygon(screen,color,listValues)
        for edge in self.edges:
            n0=prcnodes[edge[0]].x
            n1=prcnodes[edge[0]].y
            n2=prcnodes[edge[1]].x
            n3=prcnodes[edge[1]].y
            try:
                pygame.draw.line(screen,(100,100,100),(n0,n1),(n2,n3),1)
            except:
                print("Bad")
            
    def procesNodes(self,camx,camy,camz,rotx,roty,rotz,cx,cy,cz):
     
        newnodes=[]
        for nodes in self.nodes:
            n1=nodes.x+camx
            n2=nodes.y+camy
            n3=nodes.z+camz
            newnodes.append(Point(n1,n2,n3))
        self.rotateZ3D(newnodes,rotz,cx,cy)
        self.rotateY3D(newnodes,roty,cx,cz)
        self.rotateX3D(newnodes,rotx,cy,cz)
        return newnodes
              
    def rotateZ3D(self,newnodes,theta,ca,cb):
        for i in range(len(newnodes)):
            newnodes[i].x,newnodes[i].y=rotate2D(newnodes[i].x,newnodes[i].y,theta,ca,cb)
   
    def rotateX3D(self,newnodes,theta,ca,cb):       
        for i in range(len(newnodes)):           
            newnodes[i].y,newnodes[i].z=rotate2D(newnodes[i].y,newnodes[i].z,theta,ca,cb)

    def rotateY3D(self,newnodes,theta,ca,cb): 
        for i in range(len(newnodes)):
            newnodes[i].x,newnodes[i].z=rotate2D(newnodes[i].x,newnodes[i].z,theta,ca,cb)
            
    def translate(self,x,y,z):
        for i in range(len(self.nodes)):
            node=self.nodes[i]
            xN=x+node.x
            yN=y+node.y
            zN=z+node.z
            node.x=xN
            node.y=yN
            node.z=zN
            self.nodes[i]=node
            
    def scale(self,x,y,z):
        for i in range(len(self.nodes)):
            node=self.nodes[i]
            xN=x*node[0]
            yN=y*node[1]
            zN=z*node[2]
            node[0]=xN
            node[1]=yN
            node[2]=zN
            self.nodes[i]=node

   

class Cube(ThreeDObject):
    edge0=[0,1]
    edge1=[1,5]
    edge2=[5,4]
    edge3=[4,0]
    edge4=[0,2]
    edge5=[2,3]
    edge6=[3,7]
    edge7=[7,6]
    edge8=[6,2]
    edge9=[6,4]
    edge10=[7,5]
    edge11=[3,1]
    edges=[edge0,edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11]
    face1=[0,11,5,4]
    face2=[0,1,2,3]
    face3=[1,10,6,11]
    face4=[2,9,7,10]
    face5=[7,6,5,8]
    face6=[8,9,3,4]
    faces=[face1,face2,face3,face4,face5,face6]
   
    color=(220,220,220)
    
    def __init__(self,x,y,z,w,h,d):
        self.nodes=[Point(x,y,z),
        Point(x,y,z+d),
        Point(x,y+h,z),
        Point(x,y+h,z+d),
        Point(x+w,y,z),
        Point(x+w,y,z+d),
        Point(x+w,y+h,z),
        Point(x+w,y+h,z+d),
        ]
        self.cx=x+w//2
        self.cy=y+h//2
        self.cz=z+d//2
        super(Cube,self).__init__(self.nodes,Cube.edges,Cube.faces,Cube.color,self.cx,self.cy,self.cz)

class pyramid(ThreeDObject):
    color=[100,200,255]
    edge0=[0,1]
    edge1=[1,2]
    edge2=[2,4]
    edge3=[4,3]
    edge4=[3,1]
    edge5=[0,2]
    edge6=[0,3]
    edge7=[0,4]
    face1=[1,2,3,4]
    face2=[0,1,5]
    face3=[0,4,6]
    face4=[7,3,6]
    face5=[7,2,5]
    faces=[face1,face2,face3,face4,face5]    
    edges=[edge0,edge1,edge2,edge3,edge4,edge5,edge6,edge7]
    def __init__(self,x,y,z,w,h,d):
        self.nodes=[Point(x,y+h,z),Point(x,y,z+d),Point(x+w,y,z),Point(x-w,y,z),Point(x,y,z-d)]        
        super(pyramid,self).__init__(self.nodes,pyramid.edges,pyramid.faces,pyramid.color)
    
    
class Cylinder(ThreeDObject):
    color=(100,200,300)
    node0=[100,0,-100]
    node1=[0,100,-100]
    node2=[-100,0,-100]
    node3=[0,-100,-100]
    node4=[100,0,100]
    node5=[-100,0,100]
    node6=[0,100,100]
    node7=[0,-100,100]
    nodes=[node0,node1,node2,node3,node4,node5,node6,node7]
    edge1=[0,4]
    edge2=[1,6]
    edge3=[2,5]
    edge4=[3,7]
    edge5=[0,1,2,3]
    edge6=[4,5,6,7]
    edges=[edge1,edge2,edge3,edge4,edge5,edge6]
    def __init__(self,color=(255,255,0)):
        super(Cylinder,self).__init__(Cylinder.nodes,Cylinder.edges,color)
    
    def drawObject(self,screen):
        for edge in self.edges:
            n0=self.nodes[edge[0]][0]+200
            n1=self.nodes[edge[0]][1]+200
            n2=self.nodes[edge[1]][0]+200
            n3=self.nodes[edge[1]][1]+200            
            if len(edge)==2:
                pygame.draw.line(screen,(100,255,255),(n0,n1),(n2,n3),1)
            else:
                n4=self.nodes[edge[2]][0]+200
                n5=self.nodes[edge[2]][1]+200
                n6=self.nodes[edge[3]][0]+200
                n7=self.nodes[edge[3]][1]+200
                rad=distance(n0,n1,n4,n5)//2
                pygame.draw.ellipse(screen,(100,200,200),(int(n0-rad),int(n1),n4+rad,n5))
                                
def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

   