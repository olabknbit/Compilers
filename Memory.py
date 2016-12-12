class Memory:
    def __init__(self, name):  # memory name
        self.vals = {}
        self.name = name

    def has_key(self, name):  # variable name
        return name in self.vals.keys()

    def get(self, name):  # gets from memory current value of variable <name>
        return self.vals.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.vals[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memory = []
        if memory is not None:
            self.memory.append(memory)

    def get(self, name):  # gets from memory stack current value of variable <name>
        # val_memory = self.get(name)
        for mem in self.memory[::-1]:
            if mem.name == 'while':
                if mem.has_key(name):
                    return mem.get(name)
            else:
                if mem.has_key(name):
                    return mem.get(name)
                return None
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.memory[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        val_memory = None
        if val_memory is None:
            for mem in self.memory[::-1]:
                if mem.name == 'while':
                    if mem.has_key(name):
                        mem.put(name, value)
                        return
                else:
                    if mem.has_key(name):
                        mem.put(name, value)
                        return

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.memory.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.memory = self.memory[:-1]