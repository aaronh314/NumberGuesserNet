import pygame
import numpy as np
from tensorflow.keras.models import load_model
from pygame.locals import *
from csv import writer


class Grid:
    def __init__(self, width, height, p_width, p_height):
        self.width = width
        self.height = height
        self.p_width = p_width
        self.p_height = p_height
        self.pixels = []
        self.init_grid_array()

    def init_grid_array(self):
        self.pixels = []
        num_cols = self.width // self.p_width
        num_rows = self.height // self.p_height
        for i in range(num_rows):
            self.pixels.append([])
            for j in range(num_cols):
                self.pixels[i].append(0)

    def clicked(self, x, y):
        row = y // self.p_height
        col = x // self.p_width
        neighbors = self.get_neighbors(row, col)
        for r, c in neighbors:
            self.pixels[r][c] = 1

    def get_neighbors(self, row, col):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                neighbor_row = row + i
                neighbor_col = col + j
                if 0 <= neighbor_row < len(self.pixels) and 0 <= neighbor_col < len(self.pixels[row]):
                    neighbors.append((neighbor_row, neighbor_col))

        return neighbors


def redraw_grid():
    win.fill((255, 255, 255))
    for row in range(len(grid.pixels)):
        for col in range(len(grid.pixels[row])):
            c = 255 - grid.pixels[row][col] * 255
            pygame.draw.rect(win, (c, c, c),
                             (col * pixel_height, row * pixel_width, pixel_height, pixel_width))
    pygame.display.update()


def add_data(image, label):
    with open("images.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        flattened = list(np.concatenate(image).flat)
        csv_writer.writerow(flattened)

    with open("labels.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        label_cat = [0] * 10
        label_cat[label] = 1
        csv_writer.writerow(label_cat)


def clear_grid():
    grid.init_grid_array()
    redraw_grid()

def predict_class():
    image = np.asarray(grid.pixels)
    image = np.concatenate(image)
    image = image.reshape(1,28,28,1)
    pygame.display.set_caption("I predict a ... " + str(model.predict_classes(image)[0]))

def main():
    run = True
    drag = False
    while run:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                drag = True
            elif event.type == MOUSEBUTTONUP:
                drag = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and not training:
                    predict_class()
                if event.key == K_c:
                    print("c")
                    clear_grid()
                if event.key in num_keys and training:
                    to_add = np.asarray(grid.pixels)
                    add_data(to_add, num_keys.index(event.key))
                    clear_grid()

        if drag:
            x, y = pygame.mouse.get_pos()
            grid.clicked(x, y)
            redraw_grid()


training = False
model = load_model("model")


num_keys = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]

pixel_width = 20
pixel_height = 20
width = pixel_width * 28
height = pixel_height * 28

pygame.init()
win = pygame.display.set_mode((width, height))
win.fill((255, 255, 255))

pygame.display.set_caption("Drawing Number: " + ("Training" if training else "Predicting"))

grid = Grid(width, height, pixel_width, pixel_height)
redraw_grid()
main()
pygame.quit()
quit()
