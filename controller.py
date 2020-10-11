from model import Snake
import glfw
import sys

class Controller(object):

    def __init__( self ):
        self.snake = None

    def set_snake(self,snake):
        self.snake = snake

    def on_key( self, window, key, scancode, action, mods ):
        print(key)
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
            self.snake.change_direction((-1,0))

        elif (key == glfw.KEY_RIGHT or key==glfw.KEY_D) and action == glfw.PRESS:
            self.snake.change_direction((1,0))

        elif (key == glfw.KEY_UP or key==glfw.KEY_W) and action == glfw.PRESS:
            self.snake.change_direction((0,1))

        elif (key == glfw.KEY_DOWN or key==glfw.KEY_S) and action == glfw.PRESS:
            self.snake.change_direction((0,-1))

        else:
            print('Unkown key')