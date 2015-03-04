import socket

nick = "nagbot"
debug = True
network = 'plug.cs.fiu.edu'
port = 6667

if debug == True:
    chan = '#bottest'
elif debug == False:
    chan = '#chat'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((network, port))

irc.recv (4096)
irc.send(bytes('NICK ' + nick + '\r\n', 'UTF-8'))
irc.send(bytes('USER NAGbot NAGbot NAGbot :Plug IRC\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + chan + '\r\n', 'UTF-8'))
irc.send(bytes('PRIVMSG ' + chan + ' :Hello.\r\n', 'UTF-8'))

def help(message):
    return('Help section under construction')

def commOpts(comm, args, data):
    print(message)
    
    if comm == 'author':
        return(' I am a PLUG Project!')

    elif comm == 'hello':

        return('hello ' + nick)

    elif comm == 'echo':
        if len(args) <= 1:
            return('what do you want me to say?')
        else:
            result = ''
            for x in args:
                result = result + x
            return(result)

    elif comm == 'help':
        result = message[6:].strip()
        if result == '':
            return(nick + ': help [<command>] - Prints discription of what <command> does.')
        return(help(message))

    elif comm == 'commands':
        return('Valid commands: author, hello, echo')

    else:
        return(comm + ' is not a valid command.')

while True:
    data = irc.recv (4096) # make data the receive buffer
    print(data)
    if data.find(bytes('PING', 'UTF-8')) != -1: # if ping is found in the data
        irc.send(bytes('PONG ' + data.decode('UTF-8').split()[1] + '\r\n','UTF-8')) # send pong back

    elif data.find(bytes('PRIVMSG', 'UTF-8')) != -1: # if PRIVMSG is in Data, Parse it

        message = ':'.join(data.decode('UTF-8').split (':')[2:]) # split command from the message
        print('this: ' + message)

        if message.lower().find('TheDefaced') == -1: # if the defaced (change to chan name) is taken from hostname
            nick = data.decode('UTF-8').split('!')[ 0 ].replace(':','')

            destination = ''.join(data.decode('UTF-8').split(':')[:2]).split (' ')[-2] # destination taken from the data

            comm = message.split( )[0]
            print ('Function is ' + comm + ' From ' + nick) # print who commanded

            arg = data.decode('UTF-8').split( ) # Arguments after the command

            args = ''
            for index, item in enumerate(arg) : #for every item in arg
                if index > 3 :
                    if args == '':
                        args = item
                    else:
                        args += ' ' + item # add the item to the string

            if comm.find(';') == 0:
                irc.send(bytes('PRIVMSG ' + chan + ' :' + commOpts(comm[1:], args, nick) + '\r\n', 'UTF-8'))

