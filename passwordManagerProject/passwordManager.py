''' 
A password manager created for CS 351.
When code is executed, it can:
1 - generate and write a key to a file named key.key 
2- take user-inputted passwords and encrypt them to a text file (called cipher.txt) stored locally onto a computer
3- decrypt specific passwords for the user that is stored in the text file
4- determine user-inputted password strength
5- generate a password for the user
'''
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
  """
  Determines a user-inputted password stength and returns a print statement stating if it is secure enough or not.
  """
  specialChar = "!@#$%^&*()-+?_=,<>/`"
  test = True
  #counts how many if statements it failed
  failedTest = 0
  #a statement to print out if password failed one or more if statements
  statement = "Your password "
  #counts how many special characters there are
  specialCount = 0
  #but if there are lots of special characters it is considered not weak -- so here we are counting how many special characters there are
  for c in newPassword:
    if c in specialChar:
      specialCount +=1

  #if length is shorter than 8
  if len(newPassword) < 8:
      test =  False
      failedTest += 1
      statement += " is shorter than 8 characters;"
  #if there is no special characters
  if not any(c in specialChar for c in newPassword):
      test =  False
      failedTest += 1
      statement += " does not contain any special characters;"
  #if there are no numbers and not too many special characters
  if not any(c.isnumeric() for c in newPassword):
      if specialCount < 2:
        test =  False
        failedTest += 1
        statement += " does not contain any numbers;"
  #if there are no capital letters and not too many special characters
  if not any(c.isupper() for c in newPassword):
      if specialCount < 2:
        test =  False
        failedTest += 1
        statement += " does not contain any capital letters;"

  if not test:
    if (failedTest > 1):
      print("Your password is weak!")
      print(statement)
    else:
      print("Your password is medium.")
      statement = statement.replace(";", ".")
      print(statement)
  elif test:
    print("Your password is secure!")

#--------------------------------------
"""
Before running program, we need to check if the user is a first time user or a returning user.
"""
print("Welcome to Password Manager: \n\n")
firstTime = input("Is this the first time running this program? [Y/n] ")

if firstTime.lower() == 'y':
  #if first time running program then create key.key file and ciphertext file
  write_key()
  try:
    cFile = open('cipher.txt', 'x')
    cFile.close()
  except FileExistsError:
    print('You already have a cipher.txt file created. If you want to delete your old passwords, please do so now and then restart the program.')
  
  cFile = open("cipher.txt", "r+")
else:
  cFile = open("cipher.txt", "r+")

#--------------------------------------
#gets key stored in key.key and stores in variable f
with open("key.key","rb") as f:
    key=f.read()
    #print(key)
f = Fernet(key)

"""
The start of the program.
"""
while True:
  userChoice = input("What would you like to do: View Password(1), Save New Password(2), Test Password(3), Generate a secure password(4)")

  #Viewing passwords option
  if userChoice == '1':
    choice = input("Which account would you like to view (Enter Website): ")
    choice = choice.lower()
    #search for user-inputted string for account
    for line in cFile:
      data = line.split(" ")
      if data[0] == choice:
        password = data[-1]
        de = f.decrypt(password.encode("utf"))
        print("Account: " + data[0])
        print("User ID: " + data[1])
        print("Password: " + de.decode("utf"))
  
  #Entering a new password
  elif userChoice == '2':
    #======Take user input======
    #Enter website name
    accountName = input("What's the website associated with the password you want to store?")
    accountName = accountName.lower()
    #Enter username/email
    userID = input("What is the User ID?")
    #Enter password
    newPassword = input("Enter new password: ")
    #===========================
    #Encrypt password
    newToken = f.encrypt(newPassword.encode('utf-8'))
    
    #If it's a first time user, then write at first line and turn first time to no.
    if firstTime.lower() == 'y':
        cFile.write(accountName+" "+ userID+ " "+newToken.decode("utf"))
        firstTime = 'n'
    else:
          lines = cFile.readlines()
          accountExist = 0
          #first check if the website already exists
          for i, line in enumerate(lines):
              if line.startswith(accountName):
                  accountExist = 1
                  break
          #if account exists, then add the new userid/password write underneath that line
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
              #If wesbite not in file already; add to eof
              cFile.close()
              cFile = open('cipher.txt', 'a')
              cFile.write('\n'+accountName+" "+ userID+ " "+newToken.decode("utf"))
              cFile.close()
              cFile = open("cipher.txt", "r+")
  
  #Checking password strength
  elif userChoice == "3":
    stCheck = input("Enter a password to check: ")
    passwordStength(stCheck)
  
  #Generate a password for the user
  elif userChoice == "4":
    passGen()
  
  #Any other choice is not valid, will send a print statement and then user will be presented with the same options again.
  elif userChoice != '-1':
    print("Not a valid choice. Please try again.")

  #stops program
  if userChoice == '-1':
    cFile.close()
    break

