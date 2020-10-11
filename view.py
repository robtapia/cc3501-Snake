import glfw
from OpenGL.GL import *
import sys

from model import *
from controller import Controller

if __name__ == '__main__' :
    
    if not glfw.init():
        sys.exit()
    
    width = 800
    height = 800

    window = glfw.create_window(width,height, 'Snake', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    
    controlador = Controller()
    glfw.set_key_callback(window, controlador.on_key)

    pipeline = es.SimpleTransformShaderProgram()
    pipelineTexturas = es.SimpleTextureTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    glClearColor(0, 0.85, 0, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    snake =Snake()

    controlador.set_snake(snake)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        snake.drawFondo(pipeline)
        snake.draw(pipeline,pipelineTexturas)
        snake.move()
        glfw.swap_buffers(window)

    glfw.terminate()


