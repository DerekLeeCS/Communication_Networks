import requests

link = 'http://localhost:80'

if __debug__:
    username = 'josh'
else:
    username = input("Please enter your username: ")

# GET request
def get(user):
    params = {'user':user}
    r = requests.get(link, params=params)
    return r


# Returns a parsed GET request
def parseGet(user):
    r = get(user)
    parsed = r.json()
    return { (msg['sender'],msg['value']) for msg in parsed['response']['messages'] }


# Pretty prints a parsed GET request
def printGet(parsed):
    temp = [ "(" + x[0] + ") " + x[1] for x in parsed ]
    print(*temp, sep="\n", end="\n\n")


# POST request
def post(sender, receiver, message):
    params = {'sender':sender, 'receiver':receiver, 'message':message}
    r = requests.post(link, data=params)
    return r


if __name__ == "__main__":

    # Initial GET request to fetch messages
    seen = parseGet(username)
    printGet(seen)

    while True:

        command = input( "Please enter a command: " )
        
        if command == 'refresh':

            # GET the messages again
            new = parseGet(username)

            # Find the difference (new elements)
            unseen = new-seen
            printGet(unseen)
            
            # Update seen
            seen = seen.union(new)

        elif command.split(':')[0] == 'send' and len(command.split(':')) == 3:
            _, receiver, msg = command.split(':')
            post(username, receiver, msg)
            print("Message Sent.")

        elif command == 'quit':
            exit()

        else:
            print("Error: Invalid Command.", end="\n\n")