from cryptography.fernet import Fernet
import random
import string

def passGen():
  length = 10
  requirements = string.ascii_letters + string.digits + string.punctuation
  password = "".join(random.sample(requirements, length))

  print("Your secure password: " + password)
    
def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def passwordStength(newPassword):
  #tests password strength
  specialChar = "!@#$%^&*()-+?_=,<>/"
  test = False

  if len(newPassword) < 8:
      test =  False
  elif not any(c in specialChar for c in newPassword):
      test =  False
  elif not any(c.isnumeric() for c in newPassword):
      test =  False
  elif not any(c.isupper() for c in newPassword):
      test =  False
  else: 
      test =  True

  if not test:
    print("Your password is not secure!")
  elif test:
    print("Your password is secure!")


print("Welcome to Password Manager: \n\n")
firstTime = input("Is this the first time running this program? [Y/n] ")

#if first time running program then create key.key file and ciphertext file
if firstTime.lower() == 'y':
  write_key()
  try:
    cFile = open('cipher.txt', 'x')
    cFile.close()
  except FileExistsError:
    print('You already have a cipher.txt file created. If you want to delete your old passwords, please do so now.')
  
  cFile = open("cipher.txt", "r+")
else:
  cFile = open("cipher.txt", "r+")

#--------------------------------------
#gets key
with open("key.key","rb") as f:
    key=f.read()
    #print(key)
f = Fernet(key)

while True:
  userChoice = input("What would you like to do: View Password(1), Save New Password(2), Test Password(3), Generate a secure password(4)")

  if userChoice == '1':
    choice = input("Which account would you like to view (Enter Website): ")
    for line in cFile:
      data = line.split(" ")
      if data[0] == choice:
        password = data[-1]
        de = f.decrypt(password.encode("utf"))
        print("Account: " + data[0])
        print("User ID: " + data[1])
        print("Password: " + de.decode("utf"))
  elif userChoice == '2':
    accountName = input("What's the website associated with the password you want to store?")
    accountName = accountName.lower()
    userID = input("What is the User ID?")
    newPassword = input("Enter new password: ")
    
    newToken = f.encrypt(newPassword.encode('utf-8'))
    
    if firstTime.lower() == 'y':
        cFile.write(accountName+" "+ userID+ " "+newToken.decode("utf"))
        firstTime = 'n'
    else:
          lines = cFile.readlines()
          accountExist = 0
          for i, line in enumerate(lines):
              if line.startswith(accountName):
                  accountExist = 1
                  break

          if (accountExist == 1):
              print('Account exists!')
              for i, line in enumerate(lines):
                  if line.startswith(accountName):
                      lines[i] = lines[i].strip() + '\n'+accountName+" "+ userID+ " "+newToken.decode("utf")+'\n'
                      break
              print("Added new password")
              cFile.seek(0)
              for line in lines:
                  cFile.write(line)
          else:
              #If not in file already
              cFile.close()
              cFile = open('cipher.txt', 'a')
              cFile.write('\n'+accountName+" "+ userID+ " "+newToken.decode("utf"))
              cFile.close()
              cFile = open("cipher.txt", "r+")
  elif userChoice == "3":
    stCheck = input("Enter a password to check: ")
    passwordStength(stCheck)
  elif userChoice == "4":
    passGen()
  elif userChoice != '-1':
    print("Not a valid choice. Please try again.")

  #stops program
  if userChoice == '-1':
    cFile.close()
    break

