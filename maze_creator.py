#-----import statements-----
import random
import turtle
import time
import leaderboard


#-----game configuration----
#Leaderboard condigurations
score = 0
score_multiplyer = 1
username = input("Username: ")
leaderboard_values = []

chosen_num = 0
choose = 1
height_count = 0
length_count = 0
blackpixels = 0
choosevar=0
wallgen=0
randomgen=0
bordergen=0
powerupnum=0
difficulty = 0

standard_font = ("Times New Roman", 24, "normal")
small_font = ("Times New Roman", 18, "normal")

sprite_x = 0
sprite_y = 0
length = 30
height = 30
score = 0

leaderboard_file_name = "leaderboard.txt"
custom_maze_file = "custom_maze.txt"

#Set up screen configurations
wn = turtle.Screen()
wn.setup(1000,850)
wn.title("Turtle Adventure")
wn.tracer(False)
wn.listen()

block_stamp = turtle.Turtle()
block_stamp.speed(0)
block_stamp.penup()
block_stamp.hideturtle()
block_stamp.shape("square")

word_pen = turtle.Turtle()
word_pen.speed(0)
word_pen.penup()
word_pen.hideturtle()
word_pen.shape("square")

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.penup()
score_pen.color("black")
score_pen.hideturtle()
score_pen.setpos(150,340)

home_button = turtle.Turtle()
home_button.penup()
home_button.shape("square")
home_button.color("lime")
home_button.goto(-400,375)
home_button.shapesize(2)

buttons = turtle.Turtle()
buttons.shape("square")
buttons.shapesize(7.6)
buttons.penup()

powerup_value_changed = True

game_started = False
is_custom = False

button_colors = ["dodgerblue", "lightblue", "mediumspringgreen"]
button_names = ["Random Maze", "Custom Maze", "Instructions"]


#Function to draw home screen
def home_screen():
    global button_colors
    global button_colors
    global score
    global leaderboard_values
    global standard_font
    global small_font
    global grid
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global powerup_value_changed
    global game_started
    global sprite_y
    global sprite_x
    global score_multiplyer

    #Default powerup values
    num_of_bombs = 1
    num_of_lasers = 2
    num_of_path_clears = 1
    teleport_num = 1
    powerup_shuffles = 2

    wn.tracer(False)
    wn.clear()
    wn.bgcolor("aqua")

    score = 0
    score_multiplyer = 1
    sprite_x = 0
    sprite_y = 0

    leaderboard_values = []
    grid = []

    powerup_value_changed = True
    game_started = False

    word_pen.color("black")
    word_pen.setpos(0,325)
    word_pen.penup()
    word_pen.write("Turtle Adventure", move=False, align="center", font= standard_font )

    wn.onclick(lambda x,y: button_pressed(x,y))

    for i in range(3):
        wn.tracer(False)
        buttons.goto(0,145-i*190)
        buttons.color(button_colors[i])
        buttons.stamp()
        word_pen.setpos(0,225-i*190)
        word_pen.write(button_names[i], move=False, align="center", font= small_font )

    wn.update()


#Function to check if any buttons are clicked
def button_pressed(x_coor,y_coor):
    global button_names
    global game_started
    global custom_maze_file
    global length
    global height
    global grid
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global is_custom

    if x_coor<-380 and x_coor>-420:
        if y_coor<395 and y_coor>355:
            home_screen()
            return

    if game_started:
        return

    button_index = -1

    if x_coor<74 and x_coor>-74:
        if y_coor<211 and y_coor>60:
            button_index = 0
        elif y_coor<20 and y_coor>-130:
            button_index = 1
        elif y_coor<-170 and y_coor>-320:
            button_index=2
    
    if button_index==0 or button_index == 1:
        wn.clear()
        wn.bgcolor("aqua")
        game_started = True
        wn.onkeypress(lambda: move_left(), "a")
        wn.onkeypress(lambda: move_right(), "d")
        wn.onkeypress(lambda: move_up(), "w")
        wn.onkeypress(lambda: move_down(), "s")
        wn.onkeypress(lambda: use_bomb(), "r")
        wn.onkeypress(lambda: horizontal_laser(), "q")
        wn.onkeypress(lambda: vertical_laser(), "e")
        wn.onkeypress(lambda: clear_path(), "Q")
        wn.onkeypress(lambda: teleport(), "E")
        wn.onkeypress(lambda: shuffle_powerups(), "R")
        
        #Maze randomly set up
        if button_index == 0:
            #Set up grid (Number corresponds to color, 0 is empty, 1 is wall)
            grid = []

            num_of_bombs = 1
            num_of_lasers = 2
            num_of_path_clears = 1
            teleport_num = 1
            powerup_shuffles = 2
            
            for i in range(height):
                row = []
                for j in range(length):
                    row.append(0)
                grid.append(row)
            generate_grid()
            is_custom = False

        #Reads custom maze file and puts it into the grid
        else:
            custom_maze = open(custom_maze_file,"r")
            for i in range(height):
                line = custom_maze.readline().split()
                for j in range(len(line)):
                    if int(line[j])>9 or int(line[j]) < 0 or (int(line[j]) >1 and int(line[j])<5):
                        line[j] = int(1)
                    else:
                        line[j] = int(line[j])
                
                grid.append(line)
            
            #Reads custom powerup amounts (Last line of file)
            powerups = custom_maze.readline().split()
            for index in range(len(powerups)):
                powerups[index] = int(powerups[index])
                if powerups[index]<0:
                    powerups[index] = 0
                elif powerups[index]>999:
                    powerups[index] = 999


            num_of_bombs = powerups[0]
            num_of_lasers = powerups[1]
            teleport_num = powerups[2]
            num_of_path_clears = powerups[3]
            powerup_shuffles = powerups[4]
            is_custom = True

        grid[0][0] = 3
        grid[height-1][length-1] = 4

        home_button.sety(395)
        home_button.color("black")
        home_button.write("Home", move=False, align="center", font= small_font)
        home_button.sety(375)
        home_button.color("lime")
        home_button.stamp()
        draw_grid()
        wn.update()


#Function that redraws grid after every block
def draw_grid():
    global grid
    global score
    global num_of_path_clears
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global powerup_shuffles
    global sprite_x
    global sprite_y
    global length
    global height
    global powerup_value_changed
    global game_started
    if not game_started:
        return
        
    wn.onclick(lambda x,y: button_pressed(x,y))


    wn.tracer(False)
    block_stamp.clear()
    time.sleep(0.05)
    top = 325
    left = -300
    
    colors = ["white","black", "blue", "red","gold", "purple", "lime", "green", "pink", "brown"]
    
    #Redraw grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            i_pos = top - (i * 20)
            j_pos = left + (j * 20)

            block_stamp.color(colors[grid[i][j]])
            block_stamp.setpos(j_pos, i_pos)
            block_stamp.stamp()

    score_pen.clear()
    wn.update()
    if float(score) - int(score) == 0:
        score_pen.write("Score: " + str(int(score)), move=False, align="center", font= small_font)
    else:
        score_pen.write("Score: " + str(float(score)), move=False, align="center", font= small_font)

    #Pruning to only rewrite powerup values if it changed
    if powerup_value_changed and game_started:

        wn.tracer(False)
        word_pen.clear()

        #Display inventory drawings
        word_pen.setpos(-380,-305)
        word_pen.color(colors[5])
        word_pen.stamp()
        word_pen.setpos(-190,-305)
        word_pen.color(colors[6])
        word_pen.stamp()
        word_pen.setpos(0,-305)
        word_pen.color(colors[7])
        word_pen.stamp()
        word_pen.setpos(190,-305)
        word_pen.color(colors[8])
        word_pen.stamp()
        word_pen.setpos(380,-305)
        word_pen.color(colors[9])
        word_pen.stamp()

        #Write inventoryy values
        word_pen.color("black")
        word_pen.setpos(0,375)
        word_pen.write("Turtle Adventure", move=False, align="center", font= standard_font )
        word_pen.setpos(0,-293)
        word_pen.write("Inventory", move=False, align="center", font= small_font)

        word_pen.setpos(-380,-342)
        word_pen.write("Bombs: " + str(num_of_bombs), move=False, align="center", font= small_font)
        word_pen.setpos(-380,-367)
        word_pen.write("'r'", move=False, align="center", font= small_font)

        word_pen.setpos(-190,-342)
        word_pen.write("Lasers: " + str(num_of_lasers), move=False, align="center", font= small_font)
        word_pen.setpos(-190,-367)
        word_pen.write("Vertical: 'e', Horizontal: 'q'", move=False, align="center", font= small_font)

        word_pen.setpos(0,-342)
        word_pen.write("Teleports: " + str(teleport_num), move=False, align="center", font= small_font)
        word_pen.setpos(0,-370)
        word_pen.write("'E'", move=False, align="center", font= small_font)

        word_pen.setpos(190,-342)
        word_pen.write("Path Clears: " + str(num_of_path_clears), move=False, align="center", font= small_font)
        word_pen.setpos(190,-367)
        word_pen.write("'Q'", move=False, align="center", font= small_font)

        word_pen.setpos(380,-342)
        word_pen.write("Powerup Shuffles: " + str(powerup_shuffles), move=False, align="center", font= small_font)
        word_pen.setpos(380,-367)
        word_pen.write("'R'", move=False, align="center", font= small_font)

        powerup_value_changed = False
    wn.update()
    if (sprite_x != length-1 or sprite_y != height-1) and check_lose():
        player_lose()
        return

def move_left():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global powerup_value_changed
    global score_multiplyer
    #Check if sprite can move left (and not collide with maze or wall)
    if sprite_x > 0:
        if grid[sprite_y][sprite_x - 1] != 1 and grid[sprite_y][sprite_x - 1] != 2:
            if grid[sprite_y][sprite_x - 1] == 4:
                grid[sprite_y][sprite_x] = 2
                sprite_x -= 1
                grid[sprite_y][sprite_x] = 3
                draw_grid()
                time.sleep(1)
                player_wins()
                return
            elif grid[sprite_y][sprite_x - 1] == 5:
                num_of_bombs += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x - 1] == 6:
                num_of_lasers += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x - 1] == 8:
                num_of_path_clears += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x - 1] == 7:
                teleport_num += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x - 1] == 9:
                powerup_shuffles += 1
                powerup_value_changed = True
            grid[sprite_y][sprite_x] = 2
            sprite_x -= 1
            grid[sprite_y][sprite_x] = 3
            score += score_multiplyer
            draw_grid()
            time.sleep(0.1)
        
def move_right():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global powerup_value_changed
    global score_multiplyer
    #Check if sprite can move right (and not collide with maze or wall)    
    if sprite_x < length-1:
        if grid[sprite_y][sprite_x + 1] != 1 and grid[sprite_y][sprite_x + 1] != 2:
            if grid[sprite_y][sprite_x + 1] == 4:

                grid[sprite_y][sprite_x] = 2
                sprite_x += 1
                grid[sprite_y][sprite_x] = 3
                draw_grid()
                time.sleep(1)
                player_wins()
                return
            elif grid[sprite_y][sprite_x + 1] == 5:
                num_of_bombs += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x + 1] == 6:
                num_of_lasers += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x + 1] == 8:
                num_of_path_clears += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x + 1] == 7:
                teleport_num += 1
                powerup_value_changed = True
            elif grid[sprite_y][sprite_x + 1] == 9:
                powerup_shuffles += 1
                powerup_value_changed = True

            grid[sprite_y][sprite_x] = 2
            sprite_x += 1
            grid[sprite_y][sprite_x] = 3
            score += score_multiplyer
            draw_grid()
            time.sleep(0.1)
                    
def move_up():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global powerup_value_changed
    global score_multiplyer
    #Check if sprite can move up (and not collide with maze or wall)    
    if sprite_y > 0:
        if grid[sprite_y-1][sprite_x] != 1 and grid[sprite_y- 1][sprite_x ] != 2:
            if grid[sprite_y - 1][sprite_x ] == 4:
                grid[sprite_y][sprite_x] = 2
                sprite_y -= 1
                grid[sprite_y][sprite_x] = 3
                draw_grid()
                time.sleep(1)
                player_wins()

                return
            elif grid[sprite_y - 1][sprite_x ] == 5:
                num_of_bombs += 1
                powerup_value_changed = True
            elif grid[sprite_y - 1][sprite_x] == 6:
                num_of_lasers += 1
                powerup_value_changed = True
            elif grid[sprite_y - 1][sprite_x ] == 8:
                num_of_path_clears += 1
                powerup_value_changed = True
            elif grid[sprite_y - 1][sprite_x] == 7:
                teleport_num += 1
                powerup_value_changed = True
            elif grid[sprite_y - 1][sprite_x] == 9:
                powerup_shuffles += 1
                powerup_value_changed = True
            grid[sprite_y][sprite_x] = 2
            sprite_y -= 1
            grid[sprite_y][sprite_x] = 3
            score += score_multiplyer
            draw_grid()
            time.sleep(0.1)
        
def move_down():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global num_of_path_clears
    global powerup_shuffles
    global powerup_value_changed
    global score_multiplyer
    #Check if sprite can move down (and not collide with maze or wall)    
    if sprite_y < height-1:
        if grid[sprite_y+1][sprite_x] != 1 and grid[sprite_y + 1][sprite_x ] != 2:
            if grid[sprite_y + 1][sprite_x] == 4:
                grid[sprite_y][sprite_x] = 2
                sprite_y += 1
                grid[sprite_y][sprite_x] = 3
                draw_grid()
                time.sleep(1)
                player_wins()
                return
            elif grid[sprite_y + 1][sprite_x ] == 5:
                num_of_bombs += 1
                powerup_value_changed = True
            elif grid[sprite_y + 1][sprite_x] == 6:
                num_of_lasers += 1
                powerup_value_changed = True
            elif grid[sprite_y + 1][sprite_x ] == 8:
                num_of_path_clears += 1
                powerup_value_changed = True
            elif grid[sprite_y + 1][sprite_x] == 7:
                teleport_num += 1
                powerup_value_changed = True
            elif grid[sprite_y + 1][sprite_x] == 9:
                powerup_shuffles += 1
                powerup_value_changed = True
            grid[sprite_y][sprite_x] = 2
            sprite_y += 1
            grid[sprite_y][sprite_x] = 3
            score += score_multiplyer
            draw_grid()
            time.sleep(0.1)

def use_bomb():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_bombs
    global score_multiplyer
    global powerup_value_changed
    i_offset = [-2,-1,0,1,2]
    j_offset = [-2,-1,0,1,2]

    if num_of_bombs <= 0:
        return
    for r in i_offset:
        for k in j_offset:
            if sprite_x + k>=0 and sprite_x+k<length and sprite_y + r>=0 and sprite_y+r<height:
                if grid[sprite_y + r][sprite_x+k] != 1 and grid[sprite_y + r][sprite_x+k] != 2:
                    continue
                grid[sprite_y + r][sprite_x+k] = 0
                score += score_multiplyer
    
    num_of_bombs -= 1
    grid[sprite_y][sprite_x] = 3
    powerup_value_changed = True
    draw_grid()

def horizontal_laser():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_lasers
    global score_multiplyer
    global powerup_value_changed
    if num_of_lasers <= 0:
        return
    for i in range(6):
        if sprite_x - i>=0:
            if grid[sprite_y][sprite_x-i] == 1 or grid[sprite_y][sprite_x-i] == 2:
                grid[sprite_y][sprite_x-i] = 0
                score += score_multiplyer
        if sprite_x + i<length:
            if grid[sprite_y][sprite_x+i] == 1 or grid[sprite_y][sprite_x+i] == 2:
                grid[sprite_y][sprite_x+i] = 0
                score += score_multiplyer
    
    num_of_lasers -= 1
    grid[sprite_y][sprite_x] = 3
    powerup_value_changed = True
    draw_grid()

def vertical_laser():
    global grid
    global sprite_x
    global sprite_y
    global score
    global num_of_lasers
    global score_multiplyer
    global powerup_value_changed
    if num_of_lasers <= 0:
        return
    for i in range(6):
        if sprite_y - i>=0:
            if grid[sprite_y-i][sprite_x] == 1 or grid[sprite_y-i][sprite_x] == 2:
                grid[sprite_y-i][sprite_x] = 0
                score += score_multiplyer
        if sprite_y + i<height:
            if grid[sprite_y+i][sprite_x] == 1 or grid[sprite_y+i][sprite_x] == 2:
                grid[sprite_y+i][sprite_x] = 0
                score += score_multiplyer
    
    num_of_lasers -= 1
    grid[sprite_y][sprite_x] = 3
    powerup_value_changed = True
    draw_grid()

def clear_path():
    global grid
    global num_of_path_clears
    global powerup_value_changed

    if num_of_path_clears <= 0:
        return

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 2:
                grid[i][j] = 0
    
    num_of_path_clears -= 1
    powerup_value_changed = True
    draw_grid()

def teleport():
    global grid
    global teleport_num
    global sprite_x
    global sprite_y
    global score
    global score_multiplyer
    global powerup_value_changed
    if teleport_num <= 0:
        return
    i_offset = [-3,-2,-1,0,1,2,3]
    j_offset = [-3,-2,-1,0,1,2,3]


    grid[sprite_y][sprite_x] = 0
    sprite_x = random.randint(0,28)
    sprite_y = random.randint(0,28)
    while grid[sprite_y][sprite_x] != 0:
        sprite_x = random.randint(0,28)
        sprite_y = random.randint(0,28)

    for r in i_offset:
        for k in j_offset:
            if sprite_x + k>=0 and sprite_x+k<length and sprite_y + r>=0 and sprite_y+r<height:
                if grid[sprite_y + r][sprite_x+k] != 1 and grid[sprite_y + r][sprite_x+k] != 2:
                    continue
                grid[sprite_y + r][sprite_x+k] = 0
                score += score_multiplyer
    teleport_num -= 1
    grid[sprite_y][sprite_x] = 3
    powerup_value_changed = True
    draw_grid()

def shuffle_powerups():
    global grid
    global powerup_shuffles
    global powerup_value_changed

    if powerup_shuffles<= 0:
        return

    #First clear all previous powerups
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]>=5:
                grid[i][j] = 0

    #Function that randomly adds powerups players can collect
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0 and random.randint(1,125) == 2:
                grid[i][j] = 5
            elif grid[i][j] == 0 and random.randint(1,200) == 2:
                grid [i][j] = 6
            elif grid[i][j] == 0 and random.randint(1,350) == 2:
                grid [i][j] = 7
            elif grid[i][j] == 0 and random.randint(1,400) == 2:
                grid [i][j] = 8
            elif grid[i][j] == 0 and random.randint(1,400) == 2:
                grid [i][j] = 9

    powerup_shuffles -= 1
    powerup_value_changed = True
    draw_grid()
    
#Checks if player lost
def check_lose():
    global sprite_y
    global sprite_x
    global grid
    global num_of_path_clears
    global num_of_bombs
    global num_of_lasers
    global teleport_num
    global length

    if num_of_path_clears>0 or num_of_lasers>0 or num_of_bombs>0 or teleport_num>0:
        return False

    if sprite_y != 0 and grid[sprite_y-1][sprite_x] != 1 and grid[sprite_y-1][sprite_x] != 2:
        return False
    
    if sprite_y != height-1 and grid[sprite_y+1][sprite_x] != 1 and grid[sprite_y+1][sprite_x] != 2:
        return False

    if sprite_x != 0 and grid[sprite_y][sprite_x-1] != 1 and grid[sprite_y][sprite_x-1] != 2:
        return False

    if sprite_x != length -1 and grid[sprite_y][sprite_x+1] != 1 and grid[sprite_y][sprite_x+1] != 2:
        return False

    time.sleep(2)
    return True

#Shows player they won, sees if they made leaderboard, displays leaderboard
def player_wins():
    global leaderboard_file_name
    global score
    global username
    global is_custom

    wn.onclick(lambda x,y: button_pressed(x,y))

    wn.clear()
    wn.bgcolor("dimgrey")
    wn.tracer(False)
    wn.onclick(lambda x,y: button_pressed(x,y))

    home_button.sety(395)
    home_button.color("black")
    home_button.write("Home", move=False, align="center", font= small_font)
    home_button.sety(375)
    home_button.color("lime")
    home_button.stamp()

    if is_custom:
        word_pen.goto(0,150)
        word_pen.color("white")
        word_pen.write("Congratulations, you win!", move=False, align="center", font= standard_font)
        word_pen.goto(0,80)
        word_pen.write("Your score: " + str(int(score)), move = False, align = "center", font = small_font)
        return
    made_leaderboard = leaderboard.update_leaderboard(leaderboard_file_name,leaderboard_values,username,score)
    leaderboard.draw_leaderboard(made_leaderboard,leaderboard_file_name, word_pen, int(score),True)

    home_screen()

#Shows player they lost, displays leader
def player_lose():
    wn.clear()
    wn.bgcolor("dimgrey")
    wn.tracer(False)
    wn.onclick(lambda x,y: button_pressed(x,y))
    home_button.sety(395)
    home_button.color("black")
    home_button.write("Home", move=False, align="center", font= small_font)
    home_button.sety(375)
    home_button.color("lime")
    home_button.stamp()
    if is_custom:
        word_pen.goto(0,100)
        word_pen.color("white")
        word_pen.write("Sorry, you lost", move=False, align="center", font= standard_font)
        return
    leaderboard.draw_leaderboard(False,leaderboard_file_name, word_pen, -1, False)

#Percentage is the percentage the second number will be chosen
def randomchoice(a,b,percent):
    global chosen_num
    percent=int(percent)
    choose = random.randint(0,100)
    if(choose <= percent):
        chosen_num = b     
    else:
        chosen_num = a

def difficulty_settings():
    global diffculty 
    global chosen_num
    global choose
    global height_count
    global length_count
    global blackpixels
    global choosevar
    global wallgen
    global randomgen
    global bordergen
    global powerupnum
    global score_multiplyer


    chosen_num = 0
    choose = 1
    height_count = 0
    length_count = 0
    blackpixels = 0
    choosevar=0
    powerupnum=0
    difficulty=0

    while not(difficulty >=1 and difficulty <= 3):
        difficulty = int(input("Please enter a valid difficulty between 1 and 3: "))


    #Difficulty variables changed
    if(difficulty==1):
        wallgen = 40
        randomgen = 37
        bordergen = 30
        score_multiplyer = 1

    elif(difficulty==2):
        wallgen = 45
        randomgen = 45
        bordergen = 45
        score_multiplyer = 1.25

    else:
        wallgen = 60
        randomgen = 60
        bordergen = 55
        score_multiplyer = 1.5

#Code to draw a random grid
def generate_grid():
    global length
    global height
    global grid
    global diffculty 
    global chosen_num
    global choose
    global height_count
    global length_count
    global blackpixels
    global choosevar
    global wallgen
    global randomgen
    global bordergen
    global powerupnum

    difficulty_settings()

    #uses random function above to generate walls
    for o in range(height):
        for i in range(length):
            if(o>=1 and i>=1 and i<=29 and o<=29):
                if(grid[o-1][i] == grid[1][i]):
                    # 3rd num is the percentage that a wall will be generated next to another one, if there is a wall
                    # above the spot.
                    randomchoice(0,1,wallgen)
                    grid[o][i]=chosen_num
                elif(grid[o][i-1] == grid[o][1]):
                    # 3rd num is the percentage that a wall will be generated next to another one, if there
                    randomchoice(0,1,wallgen)
                    grid[o][i]=chosen_num
                else:
                    randomchoice(0,1,randomgen)
                    grid[o][i]=chosen_num 
            else:
                #chance of wall generating without any walls next to it
                randomchoice(0,1,bordergen)
                grid[o][i]=chosen_num
    height_count = 0
    length_count = 0
    while(length_count!=29 or height_count!=29):
        #The 90 determines the chance that the turtle will move forward, rather than backwards, on the generator for the "exit path"
        randomchoice(0,1,90)
        if(chosen_num==1):
            #chance turtle goes downwards, or forward
            randomchoice(0,1,50)
            if(chosen_num==1 and length_count!=29):
                #moveforward
                randomchoice(0,1,40)
                grid[length_count][height_count]=chosen_num
                length_count=length_count+1
            if(chosen_num==0 and height_count!=29):
                #movedown
                randomchoice(0,1,40)
                grid[length_count][height_count]=chosen_num
                height_count=height_count+1
            if(chosen_num==0):
                #chance turtle goes backwards or up
                randomchoice(0,1,50)
                if(chosen_num==1 and length_count!=0):
                    #moveback
                    grid[length_count][height_count]=0
                    length_count=length_count-1
                if(chosen_num==0 and height_count!=0):
                    #moveup
                    grid[length_count][height_count]=0
                    height_count=height_count-1

    #Part where I clean the maze up (ie remove unneeded black pieces)
    for o in range(height):
        for i in range(length):
            if(o>0 and i>0 and o<29 and i<29):
                blackpixels = 0
                if(grid[o-1][i]==1):
                    blackpixels+=1
                if(grid[o+1][i]==1):
                    blackpixels+=1
                if(grid[o][i-1]==1):
                    blackpixels+=1
                if(grid[o][i+1]==1):
                    blackpixels+=1
                if(blackpixels>2):
                    grid[o][i]=0

    #Spawn area
    for o in range(2):
        for i in range(2):
            grid[o][i]=0
    #end goal set
    grid[29][29]=4

    shuffle_powerups()

home_screen()
wn.update()



wn.mainloop()
