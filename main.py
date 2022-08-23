#Importing pygame module
import pygame as pg
#Importing sys (system) module
import sys
#Importing randrange from the random module
from random import randrange

#A 2-D (2 Dimensional) vector
vec2 = pg.math.Vector2

#Main snake class
class Snake:
    #Class Constructor
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        #Initializing the snake rectangle of width and height of tile size
        # -2 for the grid
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        #Range of the random position coordinate
        self.x_range = self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size
        self.y_range = self.size + self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size
        #Getting random position for the rectangle
        self.rect.center = self.get_random_position()
        #Movement vector of the snake
        self.direction = vec2(0, 0)
        #Snake drawing delay (milliseconds)
        ## The more the delay the solwer the snake speed
        ## This can be used to control the speed of snake
        self.step_delay = 100
        #current time of the game
        self.time = 0
        #Length of the snake
        self.length = 1
        #List of the segments of snake
        self.segments = []
        #Permissions of the snake movement
        ## Initially in every direction
        ## K_UP => UP key
        ## K_DOWN => DOWN key
        ## K_LEFT => LEFT key
        ## K_RIGHT => RIGHT key
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    #Method for movement controls        
    def control(self, event):
        #If key is pressed
        if event.type == pg.KEYDOWN:
            #If UP key pressed and having the Permissions to go up
            if event.key == pg.K_UP and self.directions[pg.K_UP]:
                #Setting the movement vector to upward
                self.direction = vec2(0, -self.size)
                #Disabling downward movement permissions
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}

            #If DOWN key pressed and having the Permissions to go down
            if event.key == pg.K_DOWN and self.directions[pg.K_DOWN]:
                #Setting the movement vector to downward
                self.direction = vec2(0, self.size)
                #Disabling upward movement permission
                self.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

            #If LEFT key pressed and having the Permissions to go left
            if event.key == pg.K_LEFT and self.directions[pg.K_LEFT]:
                #Setting the movement vector to left
                self.direction = vec2(-self.size, 0)
                #Disabling right movement permission
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}

            #If RIGHT key pressed and having the Permissions to go right
            if event.key == pg.K_RIGHT and self.directions[pg.K_RIGHT]:
                #Setting the movement vector to right
                self.direction = vec2(self.size, 0)
                #Disabling left movement permission
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

    
    def delta_time(self):
        #Getting current time
        time_now = pg.time.get_ticks()
        #If time difference is greater than step_delay
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    #This method will give a random position coordinate
    def get_random_position(self):
        return [randrange(*self.x_range), randrange(*self.y_range)]

    #Method to detect hiting the border
    def check_borders(self):
        #if it hits left or right border
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
            self.game.game_over = True
        #if it hits top or bottom border
        if self.rect.top < self.game.TILE_SIZE or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()
            self.game.game_over = True

    #Method to detect worm
    def check_worm(self):
        #if snake's center is equal to the center of the worm
        if self.rect.center == self.game.worm.rect.center:
            #Assigining new random position to the worm
            self.game.worm.rect.center = self.get_random_position()
            #Increment of the length
            self.length += 1
            #Increment of score
            self.game.score.increase()

    #Method to detect eating itself
    def check_selfeating(self):
        # if the length of the segments is not equal to the length of the Set of the segments
        # as Set takes only unique values
        # Thus the overriding center will be taken out from the Set
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            #Restart the game
            self.game.new_game()
            self.game.game_over = True

    #Method to Move
    def move(self):
        #if time interval crosses delay_step
        if self.delta_time():
            #Moving the rectangle to the direction
            self.rect.move_ip(self.direction)
            #Making copy of itself and putting into the segments
            self.segments.append(self.rect.copy())
            #Poping the first segment out
            self.segments = self.segments[-self.length:]

    #Method to snake position
    def update(self):
        #Checking if self eating
        self.check_selfeating()
        #Checking if hits the border
        self.check_borders()
        #Checking if hits worm
        self.check_worm()
        #Moving
        self.move()

    #Method to Draw each segments of the snake in green color
    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]

#Worm Class
class Worm:
    #Class constructor
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        #Initializing the rectangle of width and height of tile size
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        #Getting a random center position coordinate of the worm
        self.rect.center = self.game.snake.get_random_position()

    #Method to draw the worm
    def draw(self):
        #Drawing the worm in red color to the screen
        pg.draw.rect(self.game.screen, 'red', self.rect)

#Score Class
class Score:
    #Class constructor
    def __init__(self, scoreFactor = 10):
        self.score = 0
        self.highScore = 0
        self.scoreFactor = scoreFactor

    #Method to increase score
    def increase(self):
        self.score += 10
        if self.score > self.highScore:
            self.highScore = self.score

    #Method to reset score
    def reset(self):
        self.score = 0

#Main Game class
class Game:
    #Class constructor
    def __init__(self):
        #Initializing the pygame
        pg.init()
        #Window Size of the game
        self.WINDOW_SIZE = 600
        #Each Title size
        self.TILE_SIZE = 25
        #Frame rate of the game
        self.fps = 60
        #Setting screen size and getting the screen
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        # set the pygame window name
        pg.display.set_caption('Snake Game')
        #Clock of the game
        self.clock = pg.time.Clock()
        #Initialize score object
        self.score = Score()
        #
        self.game_over = False
        #Starting the game
        self.new_game()

    #Method to Draw grids
    def draw_grid(self):
        #Drawing vertical grids
        for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE):
            pg.draw.line(self.screen, [50] * 3, (x, self.TILE_SIZE), (x, self.WINDOW_SIZE))
                                             
        #Drawing horizontal grids
        for y in range(self.TILE_SIZE, self.WINDOW_SIZE, self.TILE_SIZE):
            pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y))


    #Method to Draw score
    def draw_score(self):
        #Score Font
        font = pg.font.SysFont(None, 24)
        #Score Text
        scoreText = font.render(f"Your Score: {self.score.score}", True, "green")
        scoreRect = scoreText.get_rect()
        #High Score Text
        highScoreText = font.render(f"High Score: {self.score.highScore}", True, "green")
        highScoreRect = highScoreText.get_rect()
        #Setting score position
        scoreRect.top = 5
        scoreRect.left = 5
        highScoreRect.right = self.WINDOW_SIZE - 5
        highScoreRect.top = 5

        #Drawing score text
        self.screen.blit(scoreText, scoreRect)
        self.screen.blit(highScoreText, highScoreRect)
        
    #Method to restart the game
    def new_game(self):
        #Initialize the Snake object
        self.snake = Snake(self)
        #Initialize the Worm object
        self.worm = Worm(self)

    #Method to show Game Over
    def game_over_draw(self):
        #Game Over Text
        text = pg.font.SysFont(None, 96).render('Game Over', True, "red")
        textRect = text.get_rect()
        #Press any key to Continue text
        smallText = pg.font.SysFont(None, 24).render("Press any key to continue", True, "blue")
        smallTextRect = smallText.get_rect()
        #Score Text
        scoreText = pg.font.SysFont(None, 24).render(f"Your score: {self.score.score}    Highest score: {self.score.highScore}", True, "green")
        scoreTextRect = scoreText.get_rect()
        # setting the position of the texts
        textRect.center = (self.WINDOW_SIZE/2, self.WINDOW_SIZE/2)
        scoreTextRect.center = (self.WINDOW_SIZE/2, self.WINDOW_SIZE/2 + 48)
        smallTextRect.center = (self.WINDOW_SIZE/2, self.WINDOW_SIZE/2 + 72)
        #Drawing the texts to the screen
        self.screen.blit(text, textRect)
        self.screen.blit(smallText, smallTextRect)
        self.screen.blit(scoreText, scoreTextRect)

    #Method to Update frame
    def update(self):
        #Updating snake object
        self.snake.update()
        #Updating the full surface of the window
        pg.display.flip()
        #Setting the frame rate
        self.clock.tick(self.fps)

    #Method to draw the window
    def draw(self):
        #Setting the Background color to black
        self.screen.fill('black')
        #if game is over
        if self.game_over:    
            #Drawing the game_over
            self.game_over_draw()
        else:
            #Drawing the grids
            self.draw_grid()
            #Draw Score
            self.draw_score()
            #Drawing worm object
            self.worm.draw()
            #Drawing the snake object
            self.snake.draw()

    #Method to check game over
    def check_game_over(self):
        if self.game_over:
            self.score.reset()
            self.game_over = False
            return True
        return False          

    #Method to check event
    def check_event(self):
        for event in pg.event.get():
            #If quit event is raised
            if event.type == pg.QUIT:
                #Exit the game
                pg.quit()
                sys.exit()
            #If game over
            if event.type == pg.KEYDOWN and self.check_game_over():
                return
            # snake control
            self.snake.control(event)

    #Method to run the game
    def run(self):
        #Runs infinitely
        while True:
            #Checking event
            self.check_event()
            #Updating frames
            self.update()
            #Drawing objects
            self.draw()


if __name__ == '__main__':
    #Creating game instance
    game = Game()
    #Running the main
    game.run()