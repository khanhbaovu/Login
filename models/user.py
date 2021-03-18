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
