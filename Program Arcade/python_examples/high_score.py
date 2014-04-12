# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Default high score
high_score = 0

# Try to read the high score from a file
try:
    f = open("high_score.txt", "r")
    high_score = int(f.read() )
    f.close()
    print ("The high score is",high_score)
except:
    # Error reading file, no high score
    print("There is no high score yet.")
    
# Get the score from the current game
current_score = 0
try:
    # Ask the user for his/her score
    current_score = int(input ("What is your score? "))
except:
    # Error, can't turn what they typed into a number
    print("I don't understand what you typed.")
    
# See if we have a new high score
if current_score > high_score:
    print ("Yea! New high score!")
    
    # We do! Save to disk 
    try:     
        # Write the file to disk   
        f = open("high_score.txt","w")
        f.write(str(current_score))
        f.close()
    except:
        # Hm, can't write it.
        print("Too bad I couldn't save it.")
else:
    print("Better luck next time.")