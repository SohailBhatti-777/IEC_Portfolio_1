# Funtion to read buildings data from a file
def read_buildings(filename):
    buildings = []

# Open the file
    with open(filename) as file:
        result = file.read()   # Read the contents of the file

# Process the data
    result = result.strip("```\n").split("```\n")
    # Split data into individual buildings
    buildings_strings = []
    for buildg in result:
        bstrip = buildg.rstrip("\n")
        buildings_strings.append(bstrip)

# Convert building strings into lists of rows
    building_rows = []
    for bstr in buildings_strings:
        building_rows.append(bstr.split("\n"))

# Convert rows into building matrices
    for brow in building_rows:
        building = []
        for row in brow:
            building.append(row.split("|"))
        buildings.append(list(reversed(building)))
        # Reverse the building matrix and append to the list
    return buildings

# SCORING SECTION
# Function to calculate stone score for a building
def calculate_stone_score(building):
    score = 0
    for row_index, row in enumerate(building):
        for dies in row:
            if str(dies).startswith("S"):
                level = row_index + 1   # level of the building
                if level == 1:
                    score += 2
                elif level == 2:
                    score += 3
                elif level == 3:
                    score += 5
                else:
                    score += 8
    return score

# Function to calculate the number of adjacent spaces filled for a die in the building
def calculate_adjacent_count(row, col, building):
    row_len = len(building[0])
    adjacents = []
    # Determine adjacent spaces based on position
    if row == 0:
        if col == 0:
            adjacents.append(building[row+1][col])
            adjacents.append(building[row][col+1])
        elif col == row_len -1:
            adjacents.append(building[row][col-1])
            adjacents.append(building[row+1][col])
        else:
            adjacents.append(building[row][col-1])
            adjacents.append(building[row][col+1])
            adjacents.append(building[row+1][col])

    elif row == len(building)-1:
        if col == 0:
            adjacents.append(building[row][col+1])
            adjacents.append(building[row-1][col])
        elif col == row_len - 1:
            adjacents.append(building[row][col-1])
            adjacents.append(building[row-1][col])
        else:
            adjacents.append(building[row][col+1])
            adjacents.append(building[row][col-1])
            adjacents.append(building[row-1][col])

    else:
        if col == 0:
            adjacents.append(building[row][col+1])
            adjacents.append(building[row+1][col])
            adjacents.append(building[row-1][col])
        elif col == row_len -1:
            adjacents.append(building[row][col-1])
            adjacents.append(building[row+1][col])
            adjacents.append(building[row-1][col])
        else:
            adjacents.append(building[row][col-1])
            adjacents.append(building[row][col+1])
            adjacents.append(building[row+1][col])
            adjacents.append(building[row-1][col])

# Count filled adjacent spaces
    count = 0
    for ad in adjacents:
        if ad != '--':
            count += 1
    return count

# Function to calculate wood score for a building
def calculate_wood_score(building):
    score = 0
    for row_ind, level in enumerate(building):
        for col_ind, die in enumerate(level):
            if die.lower().startswith("w"):
                count = calculate_adjacent_count(row_ind, col_ind, building)
                score += count * 2
    return score

# Function to calculate recycled score for a building
def calculate_glass_score(building):
    score = 0
    for row in building:
        for die in row:
            if str(die).startswith("G"):
                score += int(die[1:])
    return score

def calculate_recycled_score(building):
    recycled_count = 0
    for row in building:
        for die in row:
            if str(die).startswith("R"):
                recycled_count += 1
    return [0, 2, 5, 10, 15, 20, 30][min(recycled_count, 6)]

# Function to generate a scoring table
def make_table(stone, wood, glass, recycled):
    total = stone + wood + glass + recycled
    rslt = f"--------------------------\n"\
         f"| stone      | {stone:<10}|\n"\
         f"| wood       | {wood:<10}| \n"\
         f"| glass      | {glass:<10}|\n"\
         f"| recycled   | {recycled:<10}|\n"\
          "=============|============\n"\
         f"| Total      | {total:<10}|\n"\
          "--------------------------\n\n"
    return rslt

# Function to format building data for display
def input_buildings(building):
    return "\n".join([" ".join(row) for row in building])

# Main function to execute the scoring process
def main():
    buildings = read_buildings("datafiles/buildings.txt")
    result = ""
    for building in buildings:
        wood = calculate_wood_score(building)
        glass = calculate_glass_score(building)
        recycled = calculate_recycled_score(building)
        stone = calculate_stone_score(building)
        result += input_buildings(building) + "\n"
        result += make_table(stone, wood, glass, recycled) + "\n"
    with open("datafiles/scoring-result.txt", "w") as output_file:
        output_file.write(result)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
