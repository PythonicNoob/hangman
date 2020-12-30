import pygame
import math
import random
import string

# game variables
hm_status = 0
# represents which hangman image to be displayed.
guessed = ["A", "I", "E", "O", "U"]

# word selection
wordlist = []
choice = int(input("Type 1 for built-in list of words. Type 2 to make your own:\n"))

if choice == 1:
    diff = int(input("Enter 1 for indian states, 2 for fruits and 3 for cars:\n"))
    if diff == 1:
        wordlist = ["CHHATTISGARH", "GUJARAT", "HARYANA", "JHARKHAND", "MEGHALAYA", "MIZORAM",
                    "MANIPUR", "TRIPURA"]
    if diff == 2:
        wordlist = ["DURIAN", "RAMBUTAN", "LEMON", "LYCHEE", "TOMATO", "POMEGRANATE", "AVOCADO",
                    "CANTALOUPE"]
    if diff == 3:
        wordlist = ["KOEINGSEGG", "VOLKSWAGEN", "LAMBORGHINI", "CHEVROLET", "SKODA", "MERCEDES",
                    "MAYBACH", "DATSUN"]
# if choice == 2:
#     n = int(input("Enter number of words in list: "))
#     print("Enter words:")
#     for i in range(n):
#         wordlist.append(input("-"))


#
#  ~Ansh
#   -Changed the way the words are entered.
#   -Changed it to allow only letters. otherwise numbers can be entered and then in-game
#    u do not have option to select numbers
#

if choice == 2:

    print("Enter the word:")
    while True:
        a = input("-").lower()  # \n is newline. lower() converts it to lowercase

        if a != "" and a.isspace() is False and a != "n" and a != "no":  # Check if it is blank or not

            if a not in wordlist:
                for letr in a:
                    if letr not in string.ascii_letters:
                        print("Please enter letters only from A-Z")
                        break
            else:
                print("world already exists! please enter a new wrd")
            wordlist.append(a)

        else:
            break

w = random.choice(wordlist)
word = w.upper()

# setup display
pygame.init()
# initiating pygame and giving permission to use pygame's functionality.
# also initializes display.
WIDTH, HEIGHT = 1000, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
# display surface object created using display.set_mode(size=(w,h))
pygame.display.set_caption("Hangman Using Pygame")
# text displayed on title bar (eg. Microsoft Word)


# button variables
RADIUS = 20
GAP = 20
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
# radius*2=diameter. diameter+gap=object. object*13 per row. width-objects=starting point.
starty = 400
A = 65  # 65 is the ASCII value of letter a ~Ansh
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    # 13 letters each in 2 rows.
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])  # chr converts ASCII code to letters ~Ansh

# creating fonts using font.SysFont('font name', font size)
LETTER_FONT = pygame.font.SysFont('georgia', 35)
WORD_FONT = pygame.font.SysFont('georgia', 55)
TITLE_FONT = pygame.font.SysFont('georgia', 65)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    # png file raises error: "libpng warning: iCCP: known incorrect sRGB profile"
    images.append(image)

# define rgb value for colors being used in the program.
ALMOND = (239, 222, 205)
AMARANTH = (229, 43, 80)


def draw():  # def defines a function ~Ansh
    window.fill(ALMOND)
    # background color

    # draw title
    text = TITLE_FONT.render("HANGMAN", True, AMARANTH)
    # render('message', True, colors used) creates a text surface object.
    # no rectangular object?
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    # text surface object copied to the display surface object using blit(text, position).

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
        text = WORD_FONT.render(display_word, True, AMARANTH)
    # render('message', True, colors used) creates a text surface object.
    window.blit(text, (400, 200))
    # text surface object copied to the display surface object using blit(text, position).

    # draw buttons
    for letter in letters:
        ax, ay, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, AMARANTH, (ax, ay), RADIUS, 3)
            # syntax: pygame.draw.circle(surface, color, centre, radius). what is 3?
            text = LETTER_FONT.render(ltr, True, AMARANTH)
            # render('message', True, colors used) creates a text surface object.
            window.blit(text, (ax - text.get_width() / 2, ay - text.get_height() / 2))
            # text surface object copied to the display surface object using blit(text, position).

    window.blit(images[hm_status], (150, 100))
    # image copied to display surface object using blit(image, position)
    pygame.display.update()
    # display surface object shown on pygame window.


def display_message(message):
    pygame.time.delay(1000)
    # pauses game for 1000 milliseconds. = 1 second
    window.fill(ALMOND)
    # bg
    text = WORD_FONT.render(message, True, AMARANTH)
    # text surface object
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    # text passed to display_message() will be copied to display surface object.
    pygame.display.update()
    # display surface object shown on pygame window.
    pygame.time.delay(3000)


def main():
    # variables inside a function are different from those outside function even if they have same name.
    # to tell python that the variable outside the function and the variable inside it are same we use global. ~Ansh
    global hm_status

    fps = 60
    clock = pygame.time.Clock()
    # object created to track time.
    run = True

    while run:
        clock.tick(fps)
        # 60 frames per second. helps limit runtime speed of game.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if a letter is selected?
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    bx, by, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((bx - m_x) ** 2 + (by - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hm_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!")
            break

        if hm_status == 6:
            display_message("You LOST!")
            display_message(word)
            break


main()
pygame.quit()
