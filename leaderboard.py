# set the levels of scoring
bronze_score = 100
silver_score = 150
gold_score = 250
platinum_score = 300
diamond_score = 350

# load leaderboard from file
def update_leaderboard(file_name, leaderboard_values, player_name, player_score):

  leaderboard_file = open(file_name, 'r')  # need to create the file ahead of time in same folder

  for line in leaderboard_file:
    #Split line into list containing name and score
    line = line.split(",")

    # Add name and score to lists4
    leaderboard_values.append([line[0], int(line[1])])


  leaderboard_file.close()

  leaderboard_values.append([player_name,player_score])

  #Sort leaderboard into correct values
  leaderboard_values.sort(key = lambda a: -a[1] )
  

  leaderboard_file = open(file_name, "w")  # this function opens the file and erases its contents for a fresh start
  
  # Loop through the leaderboard values and write into file
  for index in range(min(len(leaderboard_values), 5)):
    line = leaderboard_values[index]
    
    leaderboard_file.write(line[0] + "," + str(line[1])+"\n")
  
  leaderboard_file.close()

  #Checks if player made leaderboard
  if leaderboard_values[-1][1] == player_score and leaderboard_values[-1][0] == player_name:
    return False
  else:
    return True
  

  

# draw leaderboard and display a message to player
def draw_leaderboard(made_leaderboard, file_name, turtle_object, player_score, player_win):
  
  # clear the screen and move turtle object to (-200, 100) to start drawing the leaderboard
  leaderboard_space = "    "

  font_setup = ("Times New Roman", 16, "normal")
  title_font = ("Times New Roman", 30, "normal")
  turtle_object.clear()
  turtle_object.penup()

  #Create Title
  turtle_object.setpos(0,325)
  turtle_object.down()
  turtle_object.write("Leaderboard", align = "center", font = title_font)
  turtle_object.penup()
  turtle_object.setpos(0,250)
  turtle_object.down()
  if player_win:
    turtle_object.write("You Won!", align = "center", font = title_font)
  else:
    turtle_object.write("You lost", align = "center", font = title_font)

  turtle_object.penup()

  turtle_object.goto(-225,100)
  turtle_object.hideturtle()
  turtle_object.down()
  
  leaderboard_file = open(file_name, "r")

  for index, line in enumerate(leaderboard_file):

    line = line.split(",")
  # loop through the lists and use the same index to display the corresponding name and score, separated by spaces
    if index == 0:
      turtle_object.color("aqua")
    elif index == 1:
      turtle_object.color("lightblue")
    elif index == 2:
      turtle_object.color("gold")
    elif index == 3:
      turtle_object.color("silver")
    else:
      turtle_object.color("saddlebrown")
    turtle_object.write(str(index + 1) + leaderboard_space + line[0] + leaderboard_space + line[1], font=font_setup)
    turtle_object.penup()
    turtle_object.goto(-225,int(turtle_object.ycor())-50)
    turtle_object.pendown()

  # Display message about player making/not making leaderboard based on high_scorer

  turtle_object.penup()
  turtle_object.setx(0)
  turtle_object.pendown()
  if (made_leaderboard):
    turtle_object.color("ghostwhite")
    turtle_object.write("You Made The Leaderboard. Returning Home in 10 Seconds", align = "center", font=font_setup)
  else:
    turtle_object.color("black")
    turtle_object.write("You Did Not Make The Leaderboard. Returning Home in 10 Seconds", align = "center", font=font_setup)

  turtle_object.color("black")
  if player_win:
    turtle_object.penup()
    # move turtle to a new line
    turtle_object.goto(0,int(turtle_object.ycor())-50)
    turtle_object.pendown()
    turtle_object.write("Your Score: " + str(player_score), align = "center", font=font_setup)
  turtle_object.penup()
  # move turtle to a new line
  turtle_object.goto(0,int(turtle_object.ycor())-50)
  turtle_object.pendown()

  # TODO 10: Display a gold/silver/bronze message if player earned a gold/silver/or bronze medal; display nothing if no medal
  
  if (player_score >= bronze_score and player_score < silver_score):
    turtle_object.color("saddlebrown")
    turtle_object.write("Rank: Bronze Medal",align = "center",  font=font_setup)
  elif (player_score >= silver_score and player_score < gold_score):
    turtle_object.color("silver")
    turtle_object.write("Rank: Silver Medal",align = "center",  font=font_setup)
  elif (player_score >= gold_score and player_score<player_score):
    turtle_object.color("gold")
    turtle_object.write("Rank: Gold Medal", align = "center", font=font_setup)
  elif (player_score>= platinum_score and player_score<diamond_score):
    turtle_object.color("lightblue")
    turtle_object.write("Rank: Platinum Medal", align = "center", font=font_setup)
  elif (player_score >= diamond_score):
    turtle_object.color("aqua")
    turtle_object.write("Rank: Diamond Medal :)", align = "center", font=font_setup)
  else:
    turtle_object.color("black")
    turtle_object.write("Rank: None", align = "center", font=font_setup)