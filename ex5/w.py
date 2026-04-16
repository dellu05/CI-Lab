import random


try:
    SIZE = int(input("Enter grid size (e.g., 4): "))
    if SIZE < 2:
        SIZE = 4
except:
    SIZE = 4

print(f"\nEnter Agent position (0 to {SIZE-1})")
a_r = int(input("Agent Row: "))
a_c = int(input("Agent Col: "))
agent = [a_r, a_c]

print(f"\nEnter Wumpus position (0 to {SIZE-1})")
w_r = int(input("Wumpus Row: "))
w_c = int(input("Wumpus Col: "))
wumpus = (w_r, w_c)


print(f"\nEnter Gold position (0 to {SIZE-1})")
g_r = int(input("Gold Row: "))
g_c = int(input("Gold Col: "))
gold = (g_r, g_c)


NUM_PITS = int(input("\nEnter number of pits: "))
pits = []
for i in range(NUM_PITS):
    print(f"Enter position for Pit {i+1} (0 to {SIZE-1})")
    p_r = int(input(f"Pit {i+1} Row: "))
    p_c = int(input(f"Pit {i+1} Col: "))
    pits.append((p_r, p_c))

pit_probability = round(NUM_PITS / (SIZE * SIZE), 3)



arrow = 1
step = 1
bumped = False
scream = "None"

def get_adjacent(pos):
    x, y = pos
    adj = []
    if x > 0: adj.append((x-1, y))
    if x < SIZE-1: adj.append((x+1, y))
    if y > 0: adj.append((x, y-1))
    if y < SIZE-1: adj.append((x, y+1))
    return adj

def display_grid():
    for i in range(SIZE):
        for j in range(SIZE):
            if (i, j) == tuple(agent):
                print("A", end=" ")
#            elif (i, j) == wumpus:
 #               print("W", end=" ")
  #          elif (i, j) == gold:
   #             print("G", end=" ")
    #        elif (i, j) in pits:
     #           print("P", end=" ")
            else:
                print(".", end=" ")
        print()

def get_percepts(is_bumped, is_scream):
    pos = tuple(agent)
    adj = get_adjacent(pos)

    stench = "Stench" if wumpus in adj else "None"
    breeze = "Breeze" if any(p in adj for p in pits) else "None"
    glitter = "Glitter" if pos == gold else "None"
    bump = "Bump" if is_bumped else "None"

    return (stench, breeze, glitter, bump, is_scream)

print(f"\n===== WUMPUS WORLD {SIZE}x{SIZE} =====")
print(f"Pit Probability (per cell): {pit_probability}")

while True:
    print(f"\n===== STEP {step} =====")
    print("GRID:")
    display_grid()

    print(f"\nCURRENT LOCATION: {tuple(agent)}")

    percepts = get_percepts(bumped, scream)
    print(f"PERCEPTS: {percepts}")


    scream = "None"
    bumped = False


    print("\nAvailable Actions: UP, DOWN, LEFT, RIGHT, SHOOT")
    action = input("Enter your action: ").upper().strip()

    if action == "UP":
        if agent[0] > 0:
            agent[0] -= 1
        else:
            bumped = True

    elif action == "DOWN":
        if agent[0] < SIZE-1:
            agent[0] += 1
        else:
            bumped = True

    elif action == "LEFT":
        if agent[1] > 0:
            agent[1] -= 1
        else:
            bumped = True

    elif action == "RIGHT":
        if agent[1] < SIZE-1:
            agent[1] += 1
        else:
            bumped = True

    elif action == "SHOOT" and arrow > 0:
        arrow -= 1
        if wumpus in get_adjacent(tuple(agent)):
            scream = "Scream"
            wumpus = (-1, -1)
        else:
            scream = "None"
    elif action == "SHOOT" and arrow <= 0:
        print("OUT OF ARROWS!")

    print(f"NEXT LOCATION: {tuple(agent)}")


    if tuple(agent) == wumpus:
        print("\nWUMPUS ATE THE AGENT! GAME OVER")
        display_grid()
        break

    if tuple(agent) in pits:
        print("\nAGENT FELL INTO A PIT! GAME OVER")
        display_grid()
        break

    if tuple(agent) == gold:
        print("\nAGENT FOUND THE GOLD! WIN")
        display_grid()
        break

    step += 1
    if step > 100:
        print("\nToo many steps! Game timed out.")
        break
