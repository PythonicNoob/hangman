import pygame
import math
import random
import string
import time
import os
import pandas

# game variables
hm_status = 0
# represents which hangman image to be displayed.
guessed = ["A", "I", "E", "O", "U", " "]

# word selection
wordlist = []
dialog_box = True
DIALOG_TEXT = ""
DIALOG_TEXTBOX = None
ERROR_MSSG = None

IMDBPATH = "data/imdbbdata"
CUSTOMPACK_PATH = "data/custompacks"

custompacks = []
[custompacks.append(file.replace(".txt", "")) for file in os.listdir(CUSTOMPACK_PATH)]


# setup display
pygame.init()
# initiating pygame and giving permission to use pygame's functionality.
# also initializes display.
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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
A = 65  # 65 is the ASCII value of capital letter A ~Ansh

listofletters = string.ascii_uppercase + string.digits# Storing all uppeercase letters in this variable
for vowel in ["A", "I", "E", "O", "U"]: # Remove vowels as we dont need to type vowels
    listofletters = listofletters.replace(vowel, "")


for i, lr in enumerate(listofletters):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, lr, True])

# creating fonts using font.SysFont('font name', font size)
LETTER_FONT = pygame.font.SysFont('georgia', 35)
WORD_FONT = pygame.font.SysFont('georgia', 55)
TITLE_FONT = pygame.font.SysFont('georgia', 65)
ERROR_FONT = pygame.font.SysFont('georgia', 25)
ERROR_FONT.italic = True

# load images.
images = []
for i in range(7):
    image = pygame.image.load("data\images\hangman" + str(i) + ".png")
    # png file raises error: "libpng warning: iCCP: known incorrect sRGB profile"
    images.append(image)

# define rgb value for colors being used in the program.
ALMOND = (239, 222, 205)
AMARANTH = (229, 43, 80)


def use_prebuilt_pack(name):
    if name in custompacks:
        file = open(f"data\custompacks\{name}.txt", "r")
        movies = [nm.strip() for nm in file.readlines()]
        return movies
    else:
        return "No such pack exists!"

def drawWrappedText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def draw():  # def defines a function ~Ansh
    global WIDTH
    global window

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
    draw
    pygame.time.delay(3000)

def draw_dialog_box():

    global DIALOG_TEXTBOX

    window.fill(ALMOND)
    text = TITLE_FONT.render("HANGMAN", True, AMARANTH)
    QS = LETTER_FONT.render("Please enter the words you would like to use", True, (0,0,0))

    if ERROR_MSSG:
        error = ERROR_FONT.render(ERROR_MSSG, True, AMARANTH)
        window.blit(error, ((WIDTH - error.get_width())/2, (text.get_height() + QS.get_height() )*1.1+ error.get_height()/2))

    window.blit(text, (WIDTH / 2 - text.get_width() / 2, text.get_height() / 4))
    window.blit(QS, (text.get_width() / 2, (text.get_height())+QS.get_height() / 2))
    DIALOG_TEXTBOX = textbox = pygame.Rect( WIDTH*0.1, ((2 * text.get_height())+QS.get_height() / 2), WIDTH*0.8, HEIGHT*0.6)
    textbox_boundary = pygame.Rect(WIDTH * 0.1, ((2 * text.get_height()) + QS.get_height() / 2), WIDTH * 0.8, HEIGHT * 0.6,)
    pygame.draw.rect(window, (255,255,255), textbox)
    pygame.draw.rect(window, (163, 174, 191), textbox_boundary, width=5)
    drawWrappedText(window, DIALOG_TEXT,(0,0,0),  textbox_boundary, LETTER_FONT,)
    pygame.display.update()

def main():
    # variables inside a function are different from those outside function even if they have same name.
    # to tell python that the variable outside the function and the variable inside it are same we use global. ~Ansh
    global hm_status
    global DIALOG_TEXT
    global dialog_box
    fps = 60
    clock = pygame.time.Clock()
    # object created to track time.
    run = True
    active = False
    remove_char = False

    while run:
        clock.tick(fps)
        # 60 frames per second. helps limit runtime speed of game.
        if remove_char:
            if time.time() - remove_char_time > 0.4:
                DIALOG_TEXT = DIALOG_TEXT[:-1]
        if dialog_box:
            draw_dialog_box()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if DIALOG_TEXTBOX.collidepoint(event.pos):
                        active = not active
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(DIALOG_TEXT)
                            # DIALOG_TEXT = ''

                            global word
                            global ERROR_MSSG

                            if "pack" in DIALOG_TEXT:
                                wordlist = use_prebuilt_pack( DIALOG_TEXT.split(":")[1].strip() )
                                if type(wordlist) != list:
                                    ERROR_MSSG = wordlist
                                else:
                                    word = random.choice(wordlist).upper()
                                    print(word)
                                    dialog_box = False
                            else:
                                print(DIALOG_TEXT.replace(",", ""))
                                if DIALOG_TEXT.replace(",", "").replace(" ","").isalnum():
                                    wordlist = DIALOG_TEXT.split(",")
                                    word = random.choice(wordlist).upper()
                                    dialog_box = False
                                else:
                                    ERROR_MSSG = "Please only use words and numbers!"


                        elif event.key == pygame.K_BACKSPACE:
                            DIALOG_TEXT = DIALOG_TEXT[:-1]
                            remove_char = True
                            remove_char_time = time.time()
                        else:
                            DIALOG_TEXT += event.unicode
                elif event.type == pygame.KEYUP:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            remove_char = False
        else:
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
