DB = {
  "vbkhanh": {
    "username": "vbkhanh",
    "password": "hohoho"
  },
  "ronaldo": {
    "username": "ronaldo",
    "password": "hihihi"
  },
  "messi": {
    "username": "messi",
    "password": "hehehe"
  }
}

def getUser(userName: str):
    user = DB.get(userName)
    return user

def checkUserName(userName : str):
    for user in DB:
        if userName == user:
            return False
    return True

def addUser(userName, password):
    newUser = {
      "username": userName,
      "password": password
    }
    DB[userName] = newUser
