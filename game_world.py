
# layer 0: Background Objects
# layer 1: player units
# layer 2: computer units
# layer 3: corpse
# layer 4: hp bar
# layer 5: projectile


objects = [[], [], [], [], [], []]

def add_object(o, layer):
    objects[layer].append(o)
    

def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)

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

