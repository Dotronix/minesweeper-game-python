import pyglet
from pyglet.window import mouse
import random

rectangle = pyglet.resource.image("rectangle.png")
flag = pyglet.resource.image("rectangle_green.png")

grid_batch = pyglet.graphics.Batch()
play_grid = []

labels_batch = pyglet.graphics.Batch()
labels_grid = []


mines_flagged = 0
invisible_fields = 0

w = 7
h = 7
mines = w * h // 5
print(mines)

window = pyglet.window.Window()
window.set_size((w * 50) + 320, 30 + (h * 50))
window.set_caption("Minesweeper")

game_started = False


def add_label(field):
    labels_grid.append(pyglet.text.Label(str(field[1]),
                                         font_size=20,
                                         bold=True,
                                         x=field[0].x + 10,
                                         y=field[0].y + 10,
                                         align="center",
                                         color=(255, 255, 255, 255),
                                         batch=labels_batch))


def populate_grid(grid):
    sprite_x = 10
    sprite_y = 10

    for i in range(0, h):
        row = []
        for e in range(0, w):
            row.append([pyglet.sprite.Sprite(rectangle, sprite_x, sprite_y, batch=grid_batch), False])
            sprite_x += 60
        grid.append(row)

        sprite_y += 50
        sprite_x = 10


def add_mines(grid, mines):
    for i in range(mines):
        x = random.randrange(w)
        y = random.randrange(h)
        grid[x][y][1] = True


def remove_mines(grid):
    for i in range(0, h):
        for e in range(0, w):
            grid[i][e][1] = False


def calculate_nearby_mines(grid, x, y):
    for i in range(0, y):
        for e in range(0, x):
            if grid[i][e][1] is False:
                mines_count = 0

                for a in range(i - 1, i + 2):
                    for b in range(e - 1, e + 2):
                        if 0 <= a < y and 0 <= b < x:
                            if grid[a][b][1] is True:
                                mines_count += 1
                grid[i][e][1] = mines_count


def flood_fill(grid, x, y):
    if type(grid[x][y][1]) != int or not grid[x][y][0].visible:
        return

    grid[x][y][0].visible = False
    if grid[x][y][1] != 0:
        add_label(grid[x][y])
        return

    if x > 0:
        flood_fill(grid, x - 1, y)
    if y > 0:
        flood_fill(grid, x, y - 1)
    if x < w - 1:
        flood_fill(grid, x + 1, y)
    if y < h - 1:
        flood_fill(grid, x, y + 1)


def begin_game(grid, x, y):
    global game_started
    while True:
        add_mines(grid, mines)
        calculate_nearby_mines(grid, w, h)
        if grid[x][y][1] == 0:
            open_field(play_grid, x, y)
            game_started = True
            return
        else:
            remove_mines(play_grid)


def get_field(grid, click_x, click_y):
    for i in range(0, len(grid)):
        for e in range(0, len(grid[i])):
            field = grid[i][e]
            if field[0].x < click_x < (field[0].x + field[0].width):
                if field[0].y < click_y < (field[0].y + field[0].height):
                    return [i, e]


def toggle_flag(grid, x, y):
    global mines_flagged
    current_image = grid[x][y][0].image
    new_image = flag if current_image == rectangle else rectangle

    grid[x][y][0].image = new_image

    if grid[x][y][1] is True:
        if new_image == flag:
            mines_flagged += 1
        else:
            mines_flagged -= 1
    print(mines_flagged)


def open_field(grid, x, y):
    global invisible_fields
    field = grid[x][y]
    if field[0].visible:
        if field[1] is True:
            # place holder
            print("Game Over")
        else:
            if field[1] != 0:
                add_label(field)
            else:
                flood_fill(play_grid, x, y)

    field[0].visible = False
    invisible_fields += 1


@window.event
def on_draw():
    window.clear()
    grid_batch.draw()
    labels_batch.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    player_input(x, y, button)


def player_input(x, y, button):
    field_pos = get_field(play_grid, x, y)
    if field_pos is not None:
        if game_started:
            if button == mouse.LEFT:
                open_field(play_grid, field_pos[0], field_pos[1])
            elif button == mouse.RIGHT:
                toggle_flag(play_grid, field_pos[0], field_pos[1])

            if mines_flagged == mines and w * h - mines - invisible_fields == 0:
                print("you win")
        else:
            begin_game(play_grid, field_pos[0], field_pos[1])


if __name__ == '__main__':
    populate_grid(play_grid)
    pyglet.app.run()
