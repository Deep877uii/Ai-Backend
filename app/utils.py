from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password : str):#
    return pwd_context.hash(password)#yaha pe hum password ko hash kar rahe hai taki hume plain password database me store na karna pade

def verify(plain_password, hashed_password):#yaha pe hum plain password ko hashed password ke sath compare kar rahe hai
    return pwd_context.verify(plain_password, hashed_password)#yaha pe hum plain password ko hashed password ke sath compare kar rahe hai