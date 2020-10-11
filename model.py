import utils.easy_shaders as es
import utils.transformations as tr
import utils.scene_graph as sg
import utils.basic_shapes as bs
import utils.transformations2 as tr2

from OpenGL.GL import *
from OpenGL.GL import glClearColor
import random
from typing import List
import time
import numpy as np

class Snake(object):
    def __init__(self):
        self.piezas = [(0,0),(0,-1),(0,-2)]
        self.maxLength = 20
        self.nodo = es.toGPUShape(bs.createColorQuad(0,0,0)) 
        self.direccion = (0,1)
        self.grafo = sg.SceneGraphNode('snake')
        self.speed=3
        self.muerto = False
        
        

        # cuerpo = sg.SceneGraphNode('cuerpo')
        # body.transform = tr.uniformScale(1)
        # body.childs = self.piezas

        # snake = sg.SceneGraphNode('snake')
        # snake.transform = tr.matmul([tr.uniformScale(2.0/45.0)])

        # snake.childs = [body]
        # transform_snake = sg.SceneGraphNode('snakeTR')
        # transform_snake.childs = [snake]


    def drawFondo(self, pipeline):
        if not self.muerto:
            fondo = sg.SceneGraphNode('fondo')
            fondo.transform = tr.uniformScale(2-(2*4)/45)
            fondoQuad = es.toGPUShape(bs.createColorQuad(1,1,1))
            fondo.childs = [fondoQuad]
            #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, fondo.transform)
            sg.drawSceneGraphNode(fondo,pipeline,"transform")
    
    def draw(self, pipeline, pipelineTexturas):
        if self.muerto:
            glUseProgram(pipelineTexturas.shaderProgram)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # gameOver = sg.SceneGraphNode('gameOver')
            # gameOver.transform = tr.identity()
            pantalla = es.toGPUShape(bs.createTextureQuad('gameOver.jpg',1,1),GL_CLAMP_TO_EDGE,GL_LINEAR)
            pantallaTransform = tr2.matmul([tr.uniformScale(2.5),tr2.rotationZ(0.25)])
            # gameOver.childs = [pantalla]
            # pipeline = es.SimpleTextureTransformShaderProgram()
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 1, GL_TRUE, pantallaTransform)
            # pipelineTexturas.drawShape(pantalla)
            pantalla_node = sg.SceneGraphNode('pantalla')
            pantalla_node.transform = pantallaTransform
            pantalla_node.childs = [pantalla]
            sg.drawSceneGraphNode(pantalla_node,pipelineTexturas,"transform")
            
            #self.grafo.childs = [gameOver]
            
            return
        
        for pieza in self.piezas:
            nodo = sg.SceneGraphNode('nodo')
            nodo.transform = tr.matmul([tr.uniformScale(2/45),tr.translate(pieza[0]+(1/45),pieza[1]+(1/45),0)])
            nodo.childs = [self.nodo]
            #self.grafo.childs += [nodo]
            sg.drawSceneGraphNode(nodo, pipeline, "transform")
        

    def move(self):
        time.sleep(1/self.speed)
        print(self.piezas)
        cabeza = self.piezas[0]
        cola = self.piezas[-1]
        nueva_cabeza = (cabeza[0]+self.direccion[0],cabeza[1]+self.direccion[1])
        if nueva_cabeza in self.piezas:
            self.muerto =True
            return
        elif nueva_cabeza[0] > 20 or nueva_cabeza[0] < -20 or nueva_cabeza[1] > 20 or  nueva_cabeza[1] < -20: 
            self.muerto = True
        self.piezas.insert(0,nueva_cabeza)
        if len(self.piezas) > self.maxLength:
            
            del self.piezas[-1]

    def change_direction(self,direccion):
        if direccion != (-self.direccion[0],self.direccion[1]) and direccion != (self.direccion[0],-self.direccion[1]):
            self.direccion = direccion
        print(self.direccion)
            
        

    
class Apple(object):
    pass

class AppleCreator(object):
    pass