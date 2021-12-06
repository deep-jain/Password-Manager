
def userPassword(passW):

    specialChar = "!@#$%^&*()-+?_=,<>/"

    if len(passW) < 8:
        return False
        #render red sign for size
    elif not any(c in specialChar for c in passW):
        return False
        #render red sign for special char
    elif not any(c.isnumeric() for c in passW):
        return False
        #render red sign for special char
    elif not any(c.isupper() for c in passW):
        return False
        #render red sign
    else: 
        return True




def main():
    test = "hell0World1@"
    print(userPassword(test))


if __name__ == "__main__":
    main()