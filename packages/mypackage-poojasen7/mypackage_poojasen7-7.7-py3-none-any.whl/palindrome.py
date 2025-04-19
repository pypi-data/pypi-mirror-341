def is_palindrome(text):
    text=text.lower(),replace(" "," ")
    return text==text[::-1]
string=input("Enter a string:")
if is_palindrome(string):
    print(" it's a palindrome ^^")
else:
    print("it's not a palindrome...")