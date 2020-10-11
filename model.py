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
from random import randint

class Snake(object):
    def __init__(self):
        self.piezas = [(0,0)]
        self.maxLength = 2
        self.nodo = es.toGPUShape(bs.createColorQuad(0,0,0))
        self.snakeTextura = es.toGPUShape(bs.createTextureQuad('untitled.png',1,1),GL_CLAMP_TO_EDGE,GL_LINEAR)
        self.direccion = (0,1)
        self.grafo = sg.SceneGraphNode('snake')
        self.speed=10
        self.muerto = False
        self.grilla = 10
        self.contador = 0
        self.manzana = (2,2)
        self.manzanaShape = es.toGPUShape(bs.createColorQuad(1,0,0))

        
        

        # cuerpo = sg.SceneGraphNode('cuerpo')
        # body.transform = tr.uniformScale(1)
        # body.childs = self.piezas

        # snake = sg.SceneGraphNode('snake')
        # snake.transform = tr.matmul([tr.uniformScale(2.0/45.0)])

        # snake.childs = [body]
        # transform_snake = sg.SceneGraphNode('snakeTR')
        # transform_snake.childs = [snake]


    def drawFondo(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        if not self.muerto:
            fondo = sg.SceneGraphNode('fondo')
            if self.grilla%2 != 0:
                fondo.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2-(2*4)/(self.grilla+4))])
            else :
                fondo.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2-(2*5)/(self.grilla+5))])
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
        
        # for pieza in self.piezas:
        #     nodo = sg.SceneGraphNode('nodo')
        #     #nodo.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2/(self.grilla+4)),tr.translate(pieza[0]+(1/(self.grilla+4)),pieza[1]+(1/(self.grilla+4)),0)])
        #     nodo.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2/(self.grilla+4)),tr.translate(pieza[0],pieza[1],0)])            
        #     nodo.childs = [self.nodo]
        #     #self.grafo.childs += [nodo]
        #     sg.drawSceneGraphNode(nodo, pipelineTexturas, "transform")

        for pieza in self.piezas:
            glUseProgram(pipelineTexturas.shaderProgram)
            
            # gameOver = sg.SceneGraphNode('gameOver')
            # gameOver.transform = tr.identity()
            #snake = es.toGPUShape(bs.createTextureQuad('untitle.png',1,1),GL_CLAMP_TO_EDGE,GL_LINEAR)
            if self.grilla%2 != 0:
                snakeTransform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2/(self.grilla+4)),tr.translate(pieza[0],pieza[1],0)])
            else :
                snakeTransform = tr.matmul([tr.translate(1/(self.grilla+5),1/(self.grilla+5),0),tr.uniformScale(2/(self.grilla+5)),tr.translate(pieza[0],pieza[1],0)])

            # gameOver.childs = [pantalla]
            # pipeline = es.SimpleTextureTransformShaderProgram()
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 1, GL_TRUE, snakeTransform)
            # pipelineTexturas.drawShape(pantalla)
            snake_node = sg.SceneGraphNode('nodo')
            snake_node.transform = snakeTransform
            snake_node.childs = [self.snakeTextura]
            sg.drawSceneGraphNode(snake_node,pipelineTexturas,"transform")
        
        glUseProgram(pipeline.shaderProgram)
        manzana = sg.SceneGraphNode('manzana')
        if self.grilla%2 != 0:
                manzanaTransform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(2/(self.grilla+4)),tr.translate(self.manzana[0],self.manzana[1],0)])
        else :
                manzanaTransform = tr.matmul([tr.translate(1/(self.grilla+5),1/(self.grilla+5),0),tr.uniformScale(2/(self.grilla+5)),tr.translate(self.manzana[0],self.manzana[1],0)])
        manzana.childs = [self.manzanaShape]
        manzana.transform = manzanaTransform
        sg.drawSceneGraphNode(manzana,pipeline,"transform")
        

    def move(self):
        self.contador+=1
        if self.contador %20 ==0:
            #time.sleep(1/self.speed)
            print(self.piezas)
            cabeza = self.piezas[0]
            cola = self.piezas[-1]
            nueva_cabeza = (cabeza[0]+self.direccion[0],cabeza[1]+self.direccion[1])
            if nueva_cabeza in self.piezas:
                self.muerto =True
                return
            elif nueva_cabeza[0] > (self.grilla-1)//2 or nueva_cabeza[0] < -(self.grilla-1)//2 or nueva_cabeza[1] > (self.grilla-1)//2 or  nueva_cabeza[1] < -(self.grilla-1)//2: 
                self.muerto = True
            self.piezas.insert(0,nueva_cabeza)
            if len(self.piezas) > self.maxLength:
                del self.piezas[-1]
            if nueva_cabeza == self.manzana:
                self.maxLength +=1
                while self.manzana in self.piezas:
                    self.manzana = (randint(-(self.grilla//2),(self.grilla//2)-1),randint(-(self.grilla//2),(self.grilla//2)-1))

            # if nueva_cabeza == self.manzana:
            #     self.maxLength +=1
            #     self.manzana = (randint(-(self.grilla//2),(self.grilla//2)-1),randint(-(self.grilla//2),(self.grilla//2)-1))

    def change_direction(self,direccion):
        if direccion != (-self.direccion[0],self.direccion[1]) and direccion != (self.direccion[0],-self.direccion[1]):
            self.direccion = direccion
        print(self.direccion)
            
        

    
class Apple(object):
    pass

class AppleCreator(object):
    pass