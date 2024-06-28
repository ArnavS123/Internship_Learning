class Room_DNE(Exception):
    pass

class Item_DNE(Exception):
    pass

class Invalid_Action(Exception):
    pass

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.adj_rooms = {}
    
    def add_items(self, item):
        self.items.append(item)
    
    def connect_room(self, direction, room):
        self.adj_rooms[direction] = room
    
    def describe(self):
        return f"{self.name}: {self.description}"
    
    def __str__(self):
        return f"{self.name}"

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def describe(self):
        return f"{self.name}: {self.description}"
    
    def __str__(self):
        return f"{self.name}"

class Player:
    def __init__(self, name, start):
        self.name = name
        self.current_room = start
        self.inventory = []
    
    def move(self, direction):
        if direction in self.current_room.adj_rooms:
            self.current_room = self.current_room.adj_rooms[direction]
        else:
            raise Room_DNE(f"No room in the {direction}")
    
    def pick_up(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                return
        raise Item_DNE(f"{item_name} is not in {self.current_room}")
    
    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                # Implement item use logic here
                print(f"Used {item_name}")
                self.inventory.remove(item)
                return
        raise Item_DNE(f"{item_name} is not in {self.name}'s inventory")
    
    def describe(self):
        return f"{self.name} is currently located in {self.current_room} with the following in their inventory: {[item.name for item in self.inventory]}"

def main():
    room1 = Room("Entrance Hall", "A large hall with doors to the north and east.")
    room2 = Room("Kitchen", "A kitchen with pots and pans hanging from the ceiling.")
    room3 = Room("Armory", "A room with mostly broken tools and weapons, except one.")

    room1.connect_room("north", room2)
    room2.connect_room("south", room1)

    room1.connect_room("east", room3)
    room3.connect_room("west", room1)

    potion = Item("potion", "A health potion.")
    sword = Item("sword", "A melee weapon.")
    room2.add_items(potion)
    room3.add_items(sword)

    name = input("Enter your name --> ")
    player = Player(name, room1)

    while True:
        #print(player)
        command = input("Enter your next move (move <direction>, grab <item>, use <item>, describe room, describe item <item>, describe situation, quit) --> ")

        if command == "quit":
            print("Thank you for playing!")
            break

        try:
            if command.startswith("move"):
                _, direction = command.split()
                player.move(direction)
            elif command.startswith("grab"):
                _, item_name = command.split(maxsplit=1)
                player.pick_up(item_name)
            elif command.startswith("use"):
                _, item_name = command.split(maxsplit=1)
                player.use_item(item_name)
            elif command == "describe room":
                print(player.current_room.describe())
            elif command.startswith("describe item"):
                _, _, item_name = command.split()
                for item in player.inventory:
                    if item.name == item_name:
                        print(item.describe())
            elif command == "describe situation":
                print(player.describe())
            else:
                raise Invalid_Action("Invalid command.")
        except (Room_DNE, Item_DNE, Invalid_Action) as error:
            print(error)

if __name__ == "__main__":
    main()