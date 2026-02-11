import curses
import time
import random

Info = "" # *used later vvv*


# Vector2 Class to store a pos easily
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # Equality check
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Particle Classes
class ParLogic: # Logic (How the Particle reacts)
    def __init__(self, moveSpaces):
        self.Spaces = moveSpaces

# Used for rubber/bomb ect.
class DeletPar:
    def __init__(self, moveSpaces, removeArea):
        self.Spaces = moveSpaces
        self.Area = removeArea

# Alive Particle Class
class RandomPar:
    def __init__(self, Area):
        self.area = Area
        
class ExpandPar:
    def __init__(self, Spaces):
        self.space = Spaces

class Particle: # Particle (The Particle itself)
    def __init__(self, pos, Par):
        self.Pos = Vector2(pos.x, pos.y)  # Create a copy of the position
        self.Type = Par

# Function to move the spawn position
def MovePos(key, Pos, max_x, max_y):
        if key == curses.KEY_UP:
            Pos.y -= 1
            if Pos.y < 0:
                Pos.y = max_y - 2
        elif key == curses.KEY_DOWN:
            Pos.y += 1
            if Pos.y > max_y - 2:
                Pos.y = 0
        elif key == curses.KEY_LEFT:
            Pos.x -= 1
            if Pos.x < 0:
                Pos.x = max_x - 1
        elif key == curses.KEY_RIGHT:
            Pos.x += 1
            if Pos.x > max_x - 1:
                Pos.x = 0

# Function to change pen size with mouse or + / e and - / q Keys
def ChangePenSize(key, PENSIZE, MAXPENSIZE):
    Info_msg = ""
    if key == curses.KEY_MOUSE:
            _, x, y, _, button = curses.getmouse()
            if button == curses.BUTTON4_PRESSED:  # Scroll Up
                PENSIZE += 1
                if PENSIZE > MAXPENSIZE:
                    PENSIZE = MAXPENSIZE
                    Info_msg = "Max Pen Size reached!"
                    
            elif button == curses.BUTTON5_PRESSED:  # Scroll Down
                PENSIZE -= 1
                if PENSIZE < 1:
                    PENSIZE = 1
                    Info_msg = "Min Pen Size reached!"
    else:
        if key in (ord("+"),ord("e")):
            PENSIZE += 1
            if PENSIZE > MAXPENSIZE:
                PENSIZE = MAXPENSIZE
                Info_msg = "Max Pen Size reached!"
        elif key in (ord("-"),ord("q")):
            PENSIZE -= 1
            if PENSIZE < 1:
                PENSIZE = 1
                Info_msg = "Min Pen Size reached!"
    return PENSIZE, Info_msg


# Main function
def main(stdscr):
    # setup Curses
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS) # Mouse support

    # Get maximum screen dimensions
    max_y, max_x = stdscr.getmaxyx()
    longness = 0
    # Main Variables
    Mats = ["Metal","Obsidian", "Stone", "Sand", "Water", "Bomb", "Air Bubble", 
            "Mover(Left)", "Mover(Right)", "Mover(Down)", "Mover(Up)","Pixel Killer(Breakable)",
            "Pixel Killer(Ubreakable)","Alive Pixel","Alive Teleporter","Foam"] # Selectable materials
    Mat = 0 # Selected material index (0 = "Metal", 1 = "Stone", ...)# 
    Pars = [  # Particle list and their movement spaces
        ParLogic([Vector2(0,0)]),      # 0: Metal
        ParLogic([Vector2(0,0)]),      # 1: Obsidian
        ParLogic([Vector2(0,1)]),      # 2: Stone
        ParLogic([Vector2(0,1),Vector2(-1,1),Vector2(1,1)]),  # 3: Sand
        ParLogic([Vector2(0,1),Vector2(-1,1),Vector2(1,1),Vector2(-1,0),Vector2(1,0)]),  # 4: Water
        DeletPar([Vector2(0,1)], 2),   # 5: Bomb
        ParLogic([Vector2(0,-1),Vector2(-1,-1),Vector2(1,-1)]),  # 6: Air Bubble
        ParLogic([Vector2(-1,0)]),     # 7: Mover Left
        ParLogic([Vector2(1,0)]),      # 8: Mover Right
        ParLogic([Vector2(0,1)]),      # 9: Mover Down
        ParLogic([Vector2(0,-1)]),     # 10: Mover Up
        ParLogic([Vector2(0,0)]),      # 11: Pixel Killer (Breakable)
        ParLogic([Vector2(0,0)]),      # 12: Pixel Killer (unbreakable)
        RandomPar(1),                  # 13: Alive Pixel
        RandomPar(3),                  # 14: Alive Teleporter
        ExpandPar([Vector2(0,1),Vector2(1,1),Vector2(1,0), Vector2(0,-1),Vector2(-1,-1),Vector2(-1,0)])  # 15: Foam
    ] 
    ParsInScene = [] # Particles in scene
    # Add Ground out of Material "Metal"
    for x in range(max_x):
        ParsInScene.append(Particle(Vector2(x, max_y - 2), 1))
    ParsTexture = ["#","=","O",".","~","x","*","<",">","v","ʌ","X","Z","A","T","/"] # Particle textures
    
    Pos = Vector2(max_x//2, max_y//2) # Particle Spawn position

    placed = 0 # Count of placed particles
    lastPlaced = 0 # How many pars spawnd at once
    PENSIZE = 1 # used to spawn multiple particles at once
    MAXPENSIZE = 5 # Max Pen Size
    Info = "Wellcome to Powder in Terminal" # Info string
    lastInfo = "" # Last Info string
    MaxFoam = 240 # Max Foam particles in scene (for better FPS)
    
    # Game loop
    while True:
        key = stdscr.getch()
        if key == 27: # ESC key
            break
        # Change materials with wasd
        if key == ord("d") or key == ord("w"):
            Mat += 1
            if Mat >= len(Mats):
                Mat = 0
        elif key == ord("a") or key == ord("s"):
            Mat -= 1
            if Mat < 0:
                Mat = len(Mats) - 1
        # Move Spawn pos with arrow keys
        MovePos(key, Pos, max_x, max_y)
        # Change Pen Size with Scroll Up/Down AND get Info message
        PENSIZE, lastInfo = ChangePenSize(key, PENSIZE, MAXPENSIZE)
        if lastInfo != "":
            Info = lastInfo
            lastInfo = ""
        # Spawn Particle with space
        if key == ord(" "):
            lastPlaced = 0
            if PENSIZE <= 1 or Mat == 5:
                # Check if space is free
                if not any(i.Pos == Pos for i in ParsInScene):
                    ParsInScene.append(Particle(Vector2(Pos.x, Pos.y), Mat))
                    placed += 1
                    lastPlaced += 1
            else:
                for X_ in range(-PENSIZE+1, PENSIZE-1):
                    for Y_ in range(-PENSIZE+1, PENSIZE-1):
                        # Check if space is free
                        if not any(i.Pos == Vector2(Pos.x + X_, Pos.y + Y_) for i in ParsInScene):
                            ParsInScene.append(Particle(Vector2(Pos.x + X_, Pos.y + Y_), Mat))
                            placed += 1
                            lastPlaced += 1
            Info = f"Placed {lastPlaced} '{Mats[Mat]}/s'"

        # Move Particles
        for par_ in ParsInScene[:]:  # iterate over COPY
            logic = Pars[par_.Type]
            moved = False
    
            try:
                for space_ in logic.Spaces:
                    target = Vector2(
                        par_.Pos.x + space_.x,
                        par_.Pos.y + space_.y
                    )

                    # check if target space is free
                    if any(i.Pos == target for i in ParsInScene):
                        # Bomb explodes when it hits something
                        if isinstance(logic, DeletPar):
                            for i in ParsInScene[:]:
                                if abs(par_.Pos.x - i.Pos.x) <= logic.Area and \
                                   abs(par_.Pos.y - i.Pos.y) <= logic.Area:
                                    if i in ParsInScene:
                                        # Dont Remove Obsidian
                                        if i.Type != 1:
                                            ParsInScene.remove(i)
                            if par_ in ParsInScene:
                                ParsInScene.remove(par_)
                            break
                        continue

                    # move particle
                    par_.Pos.x = target.x
                    par_.Pos.y = target.y
                    moved = True
                    break
            except AttributeError:
                try:
                    # Alive Particle Logic
                    logic_rand = Pars[par_.Type]
                    target = Vector2(
                        par_.Pos.x + random.randint(-logic_rand.area, logic_rand.area),
                        par_.Pos.y + random.randint(-logic_rand.area, logic_rand.area)
                    )
                    # Clamp to screen bounds
                    target.x = max(0, min(target.x, max_x - 1))
                    target.y = max(0, min(target.y, max_y - 2))
        
                    # Only move if target is free
                    if not any(i.Pos == target for i in ParsInScene):
                        par_.Pos.x = target.x
                        par_.Pos.y = target.y
                    else:
                        for i in ParsInScene:
                            if i.Pos == target:
                                if i.Type in (11,12): # One of the Pixel Killers
                                    # Pixel Killer removes the particle it hits
                                    if par_ in ParsInScene:
                                        ParsInScene.remove(par_)
                                    if i.Type == 11: # Breakable Pixel Killer also gets removed
                                        ParsInScene.remove(i)
                                    break # Dont check others because pixel already fund/removed
                except AttributeError:
                    # Foam Logic
                    logic_exp = Pars[par_.Type]
                    for spa_ in logic_exp.space:
                        target = Vector2(
                            par_.Pos.x + spa_.x,
                            par_.Pos.y + spa_.y
                        )
                        # check if space is free
                        if not any(i.Pos == target for i in ParsInScene):
                            # Check if limit is reached
                            foam_count = sum(1 for i in ParsInScene if i.Type == par_.Type)
                            if foam_count < MaxFoam:
                                # check if theres no water around
                                place code here
                                # place new foam particle
                                ParsInScene.append(Particle(Vector2(target.x, target.y), par_.Type))
                            else:
                                Info = "Max Foam particles reached!"
        # Draw
        stdscr.clear()
        for par_ in ParsInScene:
            if 0 <= par_.Pos.y < max_y and 0 <= par_.Pos.x < max_x:
                stdscr.addstr(par_.Pos.y, par_.Pos.x,ParsTexture[par_.Type])
        if 0 <= Pos.y < max_y and 0 <= Pos.x < max_x:
            stdscr.addstr(Pos.y, Pos.x,"V")
        # UI Info
        stdscr.addstr(0,0,Mats[Mat]) # Current Material
        stdscr.addstr(1,0,f"Pensize = {PENSIZE}")
        stdscr.addstr(2,0,Info)
        stdscr.addstr(0,max_x-8-(len(str(placed))),f"placed: {placed}") # Particles placed
        stdscr.refresh()
        time.sleep(0.001)
        longness += 0.1
    # Finish and print rounded Runtime (rounded to one decimal number)
    longness = round(longness*10)/10
    print(f"[Simulation Finish]\nInfos (' RunTime = {longness} , Particels placed = {placed} ')")

# Run Main function
curses.wrapper(main)