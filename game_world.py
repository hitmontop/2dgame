
# layer 0: Background Objects
# layer 1: corpse
# layer 2: units
# layer 3: hp bar
# layer 4: projectile
# layer 5: UI

money = 0

#mouse
x, y = 0, 0
clicked = False

objects = []

computer_ground_unit = []
computer_air_unit = []
computer_all_unit = []

player_ground_unit = []
player_air_unit = []
player_all_unit = []

plants_checking_layer = []

def sort_unit_layer():
    objects[2].sort(key=lambda object : object.y, reverse = True)

def add_layer(l):
    for i in range(l):
        objects.append([])


def add_object(o, layer):
    objects[layer].append(o)
    

def pull_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            break

def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    for o in all_objects():
        del o
    objects.clear()
    clear_checking_layer()

def clear_checking_layer():
    computer_ground_unit.clear()
    computer_air_unit.clear()
    computer_all_unit.clear()

    player_ground_unit.clear()
    player_air_unit.clear()
    player_all_unit.clear()

    plants_checking_layer.clear()

def search_objects(i):
    for o in objects[i]:
        yield o


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

