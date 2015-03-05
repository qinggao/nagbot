import socket
import requests

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

def help(arg):
    if arg == 'exch':
        return('exch [<ammount>] [<currency1>] in [<currency2>] - Converts value in <currency1> to <currency2>')
    else:
        return('Help section under construction')

def get_conversion(args):
    url = ('http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=1') % (args[1], args[3])
    try:
        result = requests.get(url).json()['v']
        cur_result = str(result*int(args[0]))
        return(cur_result)
    except KeyError:
        return('Error: failed to parse response')


def commOpts(comm, args, user_nick):
    print(message)
    
    if comm == 'author':
        return(' I am a PLUG Project!')

    elif comm == 'hello':

        return('Hello ' + user_nick)

    elif comm == 'echo':
        if len(args) <= 1:
            return('what do you want me to say?')
        else:
            result = ''
            for x in args:
                result = result + x
            return(result)

    elif comm == 'exch':
        args = args.split(' ')
        return(get_conversion(args))

    elif comm == 'help':
        if len(args) == 0:
            return(user_nick + ': help [<command>] - Prints discription of what <command> does.')
        return(help(args))

    elif comm == 'commands':
        return('Valid commands: author, echo, hello, help')

    else:
        return(comm + ' is not a valid command.')

def sender(destination, user_nick):
    if destination == chan:
        return(chan)
    elif destination == nick:
        return(user_nick)

while True:
    data = irc.recv (4096) # make data the receive buffer
    print(data)
    if data.find(bytes('PING', 'UTF-8')) != -1: # if ping is found in the data
        irc.send(bytes('PONG ' + data.decode('UTF-8').split()[1] + '\r\n','UTF-8')) # send pong back
        print('PONG sent')

    elif data.find(bytes('PRIVMSG', 'UTF-8')) != -1: # if PRIVMSG is in Data, Parse it

        message = ':'.join(data.decode('UTF-8').split (':')[2:]) # split command from the message
        print('this: ' + message)

        if message.lower().find(chan) == -1: # if (change to chan name) is taken from hostname
            arg = data.decode('UTF-8').split( ) # Arguments after the command

            print(arg)

            args = ''
            # comm = ''
            for index, item in enumerate(arg) : #for every item in arg
                if index == 3:
                    comm = item.lower().replace(':','')
                elif index > 3 :
                    if args == '':
                        args = item
                    else:
                        args += ' ' + item # add the item to the string
            user_nick = data.decode('UTF-8').split('!')[ 0 ].replace(':','')

            destination = ''.join(data.decode('UTF-8').split(':')[:2]).split (' ')[-2] # destination taken from the data
            print('destination: ' + destination)

            print ('Function is ' + comm + ' From ' + user_nick) # print who commanded
            if comm.find(';') == 0:     # finds ; at the start of the string
                irc.send(bytes('PRIVMSG ' + sender(destination, user_nick) + ' :' + commOpts(comm[1:], args, user_nick) + '\r\n', 'UTF-8'))

