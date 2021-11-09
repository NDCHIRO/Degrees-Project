import csv
import sys
import time
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {} #btrag3 el id bta3 el person

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {} #byrga3 name of the person , birth , movies ely tl3 feha(movies_id)

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {} #byrga3 title , year , stars (person_id)


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])


    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass




def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)


    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    start=Node(state=source, parent=None, action=None)
    frontier= QueueFrontier()
    frontier.add(start)
    explored=set()
    num_explored = 0
    while(True):

        # If the frontier is empty, then no solution.
        if frontier.empty == True:
            raise Exception("no solution")

        #Remove a node from the frontier
        currentNode =frontier.remove()
        num_explored+=1

        #If node contains goal state, return the solution.
        """******************************  note  ********************************************"""
        #as the hint said if solution found just return it and dont add to the frontier so this condition will not be reached
        #because it always will be returned below when the code tries to add the taget as a child it will see that its the target
        #so it will just return it immediately but i just put it as the lecture
        if target ==currentNode.state:
            return (solutionFound(currentNode))

        #Add the node to the explored set
        explored.add(currentNode.state)
        #Expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set
        for action, state in neighbors_for_person(currentNode.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=currentNode, action=action)
                """******************************  note  ********************************************"""
                #here we will always return the  solution when found
                if (state == target):
                    return (solutionFound(child))
                frontier.add(child)

    #raise NotImplementedError

def solutionFound(currentNode):
    actions = []
    cells = []
    while currentNode.parent is not None:
        actions.append(currentNode.action)
        cells.append(currentNode.state)
        currentNode = currentNode.parent
    actions.reverse()
    cells.reverse()
    solution = []
    for i in range(len(actions)):
        solution.append((actions[i], cells[i]))
    return solution

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
