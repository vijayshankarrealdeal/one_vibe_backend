from enum import Enum

class UserType(Enum):
    ADMIN = "admin"
    USER = "user"

class UserRank(Enum):
    BEGINNER = 0
    INTERMEDIATE = 1
    ADVANCED = 2
    EXPERT = 3
    MASTER = 4
    LEGENDARY = 5
    GODLIKE = 6