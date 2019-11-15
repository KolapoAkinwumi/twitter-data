#########################################################################
#   Computer Project 9
#   Algorithm
#       prompt for a filename.
#       input a filename.
#       iterate through the filename.
#           return data containing a month,username,and list of hashtags.
#               iterate through the data and get the hashtags tweeted per month.
#                   make a list of the most used hashtags.
#                   make a list of the most used hashtags per individual.
#                       make a list of common hashtags between two individuals.
#                       make a plot of common hashtags between two individuals.
#       display a graph.
##########################################################################

from collections import Counter
import string, calendar, pylab

MONTH_NAMES = [calendar.month_name[month] for month in range(1,13)]

def open_file():
    '''receives a valid file as input and returns the file for reading (fp)'''
    while True:
        #try to open a file for reading.
        try:
            #prompt for a filename.
            filename = input("Input a filename: ")
            fp = open(filename,"r")
            return fp
        #if there is a FileNotFoundError, reprompt.
        except FileNotFoundError:
            print("Error in input filename. Please try again.")
 
 
def validate_hashtag(s):
    '''
    Checks if a string is a hashtag or not.
    s: string that the function checks.
    Returns true or false.
    '''
    #If the first index of an index is a hashtag, return true.
    if s[0] == "#":
        #if the length of the hashtag is less than 3, return false.
        if len(s) <= 2:
            return False
        #iterate through the string.
        for ch in s[1:]:
            #if a part in the string is a punctuation mark, return false.
            if ch in string.punctuation:
                return False
            #if a part of the string has a number, return false.
            if s.isdigit():
                return False
        return True
    else:
        return False


def get_hashtags(s):
    '''
    Adds valid hashtags to a list.
    s: string being assessed. 
    Returns a list of hashtags (hashtag_list)
    '''
    #create an empty list.
    hashtag_list = []
    words = s.split()
    #iterate through the list of words in a tweet.
    for word in words:
        #call the validate_hastag function to see if there's hashtags.
        hashtags = validate_hashtag(word)
        #if there are hashtags, add it to the list of hashtags.
        if hashtags:
            hashtag_list.append(word)
    #return the list of hashtags.
    return(hashtag_list)


def read_data(fp):
    '''
    Reads through a file and gets the username,month, and list of hashtags.
    fp: file being read.
    returns a list containing the username, month, and list of hashtags.
    '''
    #create an empty list
    tweet_info_list = []
    #iterate through the file.
    for line in fp:
        line = line.split(",")
        #get the username, month, and string of tweets.
        username = str(line[0])
        month = int(line[1])
        tweets = str(line[2])
        #call the get_hashtags function to get a list of hashtags.
        list_of_hashtags = get_hashtags(tweets)
        tweets = [username,month,list_of_hashtags]
        #append the list of tweets to the empty list.
        tweet_info_list.append(tweets)
    return tweet_info_list
   

def get_histogram_tag_count_for_users(tweet_info_list,usernames):
    '''
    Creates a dictionary of hashtags with the hashtag as the key and the
    amount of times it occurs as the value.
    tweet_info_list: the list containing the tweet information being iterated.
    usernames: the owners of the tweets.
    returns a dictionary containing the hashtags and the amount they occur.
    (hashtag_dict)
    '''
    #create an empty dictionary.
    hashtag_dict = Counter()
    #iterate through the list of tweets.
    for tweet in tweet_info_list:
        #initialize the username variable.
        username = tweet[0]
        #if the username is in the list of the usernames:
        if username in usernames:
            hashtags = tweet[2]
            #update the dictionary with the corresponding hashtags.
            hashtag_dict.update(hashtags)
    return hashtag_dict

def get_tags_by_month_for_users(tweet_info_list,usernames):
    '''
    Create a list of hashtags for users organized by month.
    tweet_info_list: list of tweets being examined.
    usernames: the owners of the tweets.
    returns a list of hashtags tweeted by users, organized by month(tag_month_list).
    '''
    #create an empty dictionary.
    tag_month_dict = {}
    #create an empty list.
    tag_month_list = []
    #iterate through the list of tweets.
    for tweet in tweet_info_list:
        username = tweet[0]
        month = tweet[1]
        #if the a username is in the list of usernames,
        if username in usernames:
            #but the month is not in the dictionary of hashtags and months,
            if month not in tag_month_dict:
                #update the dictionary and make an empty set for every month. 
                tag_month_dict[month] = set()
            hashtags = tweet[2]
            #update the dictionary with the hashtags for the corresponding month.
            tag_month_dict[month].update(hashtags)
        #iterate through the months in a year
    for month in range(1,13):
        #if a month is in the dictionary,
        if month in tag_month_dict:
            #append a tuple containing the month number and the month to the list
            tup = (month,tag_month_dict[month])
            tag_month_list.append(tup)
        else:
            #if a month isn't in a dictionary,
            tup = (month,set())
            #append a tuple containing the month number and an empty set to the list.
            tag_month_list.append(tup)
    #return the list.
    return tag_month_list

def get_user_names(tweet_info_list):
    '''
    Makes a list of usernames in alphabetical order.
    tweet_info_list: List being iterated through, returned from read_data.
    returns a sorted list of usernames.
    '''
    #make an empty list of usernames.
    usernames = []
    #iterate through the list returned in read_data.
    for tweet in tweet_info_list:
        username = tweet[0]
        #if a username isn't already in the list of usernames, add it.
        if username not in usernames:
            usernames.append(username)
    #sort the list of usernames.
    return sorted(usernames)

def three_most_common_hashtags_combined(L,usernames):
    '''
    Creates a list of the most frequently used hashtags, collectively.
    L: list being iterated
    usernames: owners of the tweets.
    returns a list of the most frequent hashtags (most_common_hashtags).
    '''
    #store the histogram function in a variable.
    hashtags = get_histogram_tag_count_for_users(L,usernames)
    #get the most common hashtags out of the variable.
    common_hashtags = hashtags.most_common(3)
    #make an empty list.
    most_common_hashtags = []
    #iterate through the dictionary containing the common hashtags
    for hashtag,value in common_hashtags:
        #append the tuple containing the hashtags by count and hastags to the list.
        most_common_hashtags.append((value,hashtag))
    #return the list.
    return most_common_hashtags

def three_most_common_hashtags_individuals(data_lst,usernames):
    '''
    Creates a list of hashtags most frequently used by individual users.
    data_lst: tweets being examined.
    usernames: owners of the tweets
    returns a list of hashtags in descending order(master_hashtag)
    '''
    #create an empty list.
    master_hashtag = []
    #iterate through the list of usernames.
    for username in usernames:
        #store the histogram function in a variable.
        user_hashtags = get_histogram_tag_count_for_users(data_lst,[username])
        #iterate trhough the variable
        for hashtag in user_hashtags:
            #create a tuple countaining the count,hashtag,and username.
            tup = (user_hashtags[hashtag], hashtag, username)
            #append the tuple to the empty list.
            master_hashtag.append(tup)
        #return the sorted list in descending order by hashtag occurrence.
    return sorted(master_hashtag, key = lambda hashtag:hashtag[0], reverse = True)[:3]

            
def similarity(data_lst,user1,user2):
    '''
    Creates a list of hashtags tweeted by two twitter accounts
    data_lst: list of tweets being examined.
    user1: the first twitter account.
    user2: the second twitter account.
    '''
    #create an empty list.
    similar_tags = []
    #get the hashtags used for every month for the first twitter account.
    user1 = get_tags_by_month_for_users(data_lst,[user1])
    #get the hashtags used for every month for the second twitter account.
    user2 = get_tags_by_month_for_users(data_lst,[user2])
    #iterate through the months.
    for month in range (1,13):
        #make a set of common hashtags for every month.
        similarity_set = (user1[month-1][1] & user2[month-1][1])
        #create a tuple for every month with the corresponding hashtags.
        tup = (month,similarity_set)
        #append the tuple to the list.
        similar_tags.append(tup)
    #return the list.
    return similar_tags
        
def plot_similarity(x_list,y_list,name1,name2):
    '''Plot y vs. x with name1 and name2 in the title.'''
    
    pylab.plot(x_list,y_list)
    pylab.xticks(x_list,MONTH_NAMES,rotation=45,ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between '+name1+' and '+name2)
    pylab.tight_layout()
    pylab.show()
    # the next line is simply to illustrate how to save the plot
    # leave it commented out in the version you submit
    #pylab.savefig("plot.png")


def main():
    # Open the file
    fp = open_file()
    # Read the data from the file
    data = read_data(fp)
    # Create username list from data
    usernames = get_user_names(data)
    # Calculate the top three hashtags combined for all users
    top_combined = three_most_common_hashtags_combined(data,usernames)
    # Print them
    print()
    print("Top Three Hashtags Combined")
    print("{:>6s} {:<20s}".format("Count","Hashtag"))
    for tup in top_combined:
        print("{:>6d} {:<20s}".format(tup[0],tup[1]))
        
    # Calculate the top three hashtags individually for all users
    top_individual = three_most_common_hashtags_individuals(data,usernames)
    # Print them
    print()
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:<20s} {:<20s}".format("Count","Hashtag","User"))
    for tup in top_individual:
        print("{:>6d} {:<20s} {:<20s}".format(tup[0],tup[1],tup[2]))
    # Prompt for two user names from username list
    print()   
    print("Usernames: ",', '.join(usernames))
    # prompt for and validate user names
    while True:
            user_str = input("Input two user names from the list, comma separated: ")
            users = user_str.split(",")
            users = [user.strip() for user in users]
            if users[0] in usernames and users[1] in usernames:
                break
            else:
                print("Error in user names.  Please try again")
    print()
    # Calculate similarity for the two users
    similarities = similarity(data,users[0],users[1])
    print("Similarities for "+users[0]+" and "+users[1])
    print("{:12s}{:6s}".format("Month","Count",))
    # your printing loop goes here
    for tup in similarities:
        MONTH_NAMES = tup[0]
        count = len(tup[1])
        print("{:12s}{:<6d}".format(calendar.month_name[MONTH_NAMES],count))
    print()
    # Prompt to plot or not and plot if 'yes'
    # Prompt for a plot.
    choice = input("Do you want to plot (yes/no)?: ")
    #if yes.
    if choice.lower() == 'yes':
        # create x_list and y_list.
        x_list = []
        y_list = []
        #fill x_list in with months.
        for number in range(1,13):
            x_list.append(number)
        for tup in similarities:
            #fill the y_list with the amount of hashtags.
            count = len(tup[1])
            y_list.append(count)
        #plot the graph.
        plot_similarity(x_list,y_list,users[0],users[1])

if __name__ == '__main__':
    main()