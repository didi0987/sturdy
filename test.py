import itertools

# data = ["A", "B", "C", "D"]
# combinations_of_2 = itertools.combinations(data, 3)
# print(list(combinations_of_2))

with open("characters.txt", "r", encoding="utf-8") as file:
    characters = file.read().splitlines()
    characters = [
        c.split(",") for c in characters if c.strip() and not c.startswith("#")
    ]

# print(characters)
character_names = [char[0] for char in characters]
# for char in character_names:
#     print(char)

# for i, char in enumerate(character_names):
#     print(f"{i}--- {char}")

name_to_index = {name: i for i, name in enumerate(character_names)}
# key : value
print(name_to_index)
(janet,lydia):1
  


