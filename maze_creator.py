#-----import statements-----
import random
import turtle
import time


#-----game configuration-----
score = 0
username = input("Username: ")
level_type = input("Enter 0 or 1 if you want a random level or a custom level from the mazelvl.txt file: ")


#-----level editor setup-----

level_type=int(level_type)
if(level_type==1):
    print("Custom level selected!")
    maze = open("mazelvl.txt", "r")
    l = []
    l = [ line.split() for line in maze]
    print(l)
    print(l[0][0])
else:
    print("Random level selected!")
    



#Set up grid (Number corresponds to color, 0 is empty, 2 is wall)
grid = []
length = 30
height = 30
for i in range(height):
    row = []
    for j in range(length):
        row.append(2)
    grid.append(row)

standard_font = ("Times New Roman", 24, "normal")
small_font = ("Times New Roman", 18, "normal")

sprite_x = 0
sprite_y = 0
sprite = [sprite_x,sprite_y]



#Set up screen configurations
wn = turtle.Screen()
wn.tracer(False)
wn.bgcolor("aqua")
wn.setup(800,800)
wn.title("Turtle Adventure")

pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()
pen.shape("square")
pen.color("black")

#Function that redraws grid after every block
def draw_grid():
    global grid
    pen.clear()
    top = 275
    left = -300
    
    colors = ["white","red", "black", "blue"]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            i_pos = top - (i * 20)
            j_pos = left + (j * 20)

            pen.color(colors[grid[i][j]])
            pen.setpos(j_pos, i_pos)
            pen.stamp()
    pen.color("black")
    pen.setpos(0,325)
    pen.write("Turtle Adventure", move=True, align="center", font= standard_font )


def move_left():
    global grid
    global sprite_x
    global sprite_y

    #Check if sprite can move left (and not collide with maze or wall)
    if sprite_x > 0:
        if grid[sprite_y][sprite_x - 1] != 2:

            grid[sprite_y][sprite_x] = 0
            sprite_x -= 1
            grid[sprite_y][sprite_x] = 1
            draw_grid()
        
def move_right():
    global grid
    global sprite_x
    global sprite_y
    #Check if sprite can move right (and not collide with maze or wall)    
    if sprite_x < height-1:
        if grid[sprite_y][sprite_x + 1] != 2:
            grid[sprite_y][sprite_x] = 0
            sprite_x += 1
            grid[sprite_y][sprite_x] = 1
            draw_grid()
                    
def move_up():
    global grid
    global sprite_x
    global sprite_y

    #Check if sprite can move up (and not collide with maze or wall)    
    if sprite_y > 0:
        if grid[sprite_y-1][sprite_x] != 2:

            grid[sprite_y][sprite_x] = 0
            sprite_y -= 1
            grid[sprite_y][sprite_x] = 1
            draw_grid()
        
def move_down():
    global grid
    global sprite_x
    global sprite_y
    #Check if sprite can move down (and not collide with maze or wall)    
    if sprite_y < length-1:
        if grid[sprite_y+1][sprite_x] != 2:
            grid[sprite_y][sprite_x] = 0
            sprite_y += 1
            grid[sprite_y][sprite_x] = 1
            draw_grid()


wn.update()
wn.listen()
wn.onkeypress(lambda: move_left(), "a")
wn.onkeypress(lambda: move_right(), "d")
wn.onkeypress(lambda: move_up(), "w")
wn.onkeypress(lambda: move_down(), "s")

#Used to see if there are filled blocks around
i_offset = [-1,0,1]
j_offset = [-1,0,1]


grid[0][0] = 0

    


#Draws the walls of the maze
for i in range(len(grid)):
    for j in range(len(grid[i])):
        counter = 0
        for r in i_offset:
            for k in j_offset:
                if not (r== 0 and k == 0) and i+r>=0 and j+k>=0 and r+i<len(grid) and j+k<len(grid[i]) and i**2 - j**2 != 0:
                    if grid[i+r][k+j] == 0:
                        counter += 1
                    
        
        if counter >=1:
            possibilities = [0]
            for k in range(counter-1):
                possibilities.append(2)
            grid[i][j] = random.choice(possibilities)

white_columns = []
white_rows = []

path_x = 0
path_y = 0
counter = 0


#Add more movable paths to the maze
while path_x!= height-1 and path_y!=length-1 and counter<10:
    counter += 1
    new_x = random.randint(2-path_x,length-2-path_x)
    new_y = random.randint(1-path_y,height-2-path_y)

    x_y_choice = random.randint(0,1)

    #Randomly decide if move (1 is x, 2 is y)
    if x_y_choice == 0:
        #See if there are no adjacent white rows
        if path_y-1 not in white_rows and path_y+1 not in white_rows and path_y!= height-2:
            white_rows.append(path_y)
            for x_index in range(new_x+1):
                grid[path_y][path_x+x_index] = 0
        
            path_x += new_x
    elif x_y_choice == 1:
        #See if there are no adjacent white rows
        if path_x-1 not in white_columns and path_x+1 not in white_columns and path_x != length-2:
            white_columns.append(path_x)
            for y_index in range(new_y+1):
                grid[path_y + y_index][path_x] = 0
            path_y += new_y

#Add a possibile path to the end (Make it random)
while path_x != length-1 and path_y != height-1:
    for i in range(random.randint(1,height-1-path_y)):
        grid[path_y][path_x] = 0
        path_y += 1
    for i in range(random.randint(1,length-1-path_x)):
        grid[path_y][path_x] = 0
        path_x += 1

if path_x == height-1:
    for i in range(length-1-path_y):
        grid[path_y][path_x] = 0
        path_y += 1
elif path_y == length-1:
    for i in range(height-1-path_x):
        grid[path_y][path_x] = 0
        path_x += 1

    for i in range(30-path_x):
        grid[path_y][path_x] = 0
        path_x += 1

grid[height-1][length-1] = 0
grid[0][0] = 1



draw_grid()




wn.mainloop()
