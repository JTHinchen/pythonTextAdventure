listofpersons = []

class personObject:
    Name = ""
    Description = ""
    Location = [0, 0]

    def __init__(self, nameString):
        self.Name = nameString
        self.Location = [0,0]
        self.Description = ""

#This is the top-level function. It could probably use some
#de-cluttering
def interpretIncoming(data):
    print('Got Data from client:' + data)
    myincoming = data.split(sep=',')
    #with create as the first message, makes a new character
    if myincoming[0] == 'Create':
        newperson = personObject(myincoming[1])
        listofpersons.append(newperson)
        return str.encode("Created a new person with a name:" +
                          newperson.Name +
                          " at location:" + str(newperson.Location))
    #move a character based on the location sent, moves along
    #an x,y grid
    if myincoming[0] == 'Move':
        myperson = getPersonFromName(myincoming[1])
        movePerson(myperson, myincoming[2])
        return str.encode(myperson.Name + " has moved to " +
                          str(myperson.Location))
    #Adds a description to a character
    if myincoming[0] == 'Description':
        myperson = getPersonFromName(myincoming[1])
        describePerson(myperson, myincoming[2])
        return str.encode(myperson.Name + "'s description is now: " +
                          myperson.Description)
    else:
        return str.encode(data)

#Returns a person object from a name
def getPersonFromName(personname):
    for x in listofpersons:
        if x.Name == personname:
            return x

#moves a person from a place
def movePerson(myperson, direction):
    if direction == "west":
        myperson.Location = [myperson.Location[0] - 1, myperson.Location[1]]
    if direction == "east":
        myperson.Location = [myperson.Location[0] + 1, myperson.Location[1]]
    if direction == "north":
        myperson.Location = [myperson.Location[0], myperson.Location[1] + 1]
    if direction == "south":
        myperson.Location = [myperson.Location[0], myperson.Location[1] - 1]

#adds a description to a person object
def describePerson(myperson, description):
    myperson.Description = description
