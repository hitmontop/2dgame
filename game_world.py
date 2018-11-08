
# layer 0: Background Objects
# layer 1: corpse
# layer 2: player units
# layer 3: hp bar
# layer 4: projectile
# layer 5: UI


objects = [[], [], [], [], [], []]

def add_object(o, layer):
    objects[layer].append(o)
    

def pull_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)

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

def search_objects(i):
    for o in objects[i]:
        yield o

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

