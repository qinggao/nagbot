import socket
import requests
import re
import bs4

nick = "nagbot"
debug = False
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

def link_title(url): # grabs title from url page
    result = '[title] '
    response = requests.get(url)
    titles = bs4.BeautifulSoup(response.text).select('title')
    if titles:
        for title in titles:
            result += title.get_text().strip() + ' '
        print('results: ' + result)
    else:
        result = '[untitled]'
    return(result)

def help(arg): 
    if arg == 'exch':
        return('exch [<ammount>] [<currency1>] in [<currency2>] - Converts value in <currency1> to <currency2>')
    else:
        return('Help section under construction')

def get_conversion(args): # converts currency
    url = ('http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=1') % (args[1], args[3])
    try:
        result = requests.get(url).json()['v']
        cur_result = str(result*int(args[0]))
        return(cur_result)
    except KeyError:
        return('Error: failed to parse response')

def commOpts(comm, args, user_nick):
    if comm == 'author':
        return(' I am a PLUG Project!')

    elif comm == 'hello' or comm == 'hi' or comm == 'yo':

        return('Greetings ' + user_nick)

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
    data_str = data.decode('UTF-8')
    print('data: ' + data_str)

    if data_str.find(nick) != -1:

    if data_str.find('PING') == 0: # if ping is found in 0th pos
        irc.send(bytes('PONG ' + data_str.split()[1] + '\r\n','UTF-8')) # send pong back
        print('PONG sent: ' + 'PONG ' + data_str.split()[1] + '\n')

    elif data_str.find('PRIVMSG') != -1: # if PRIVMSG is in Data, Parse it
        user_nick = data_str.split('!')[0].replace(':','')

        destination = data_str.split(':')[1].split (' ')[2] # destination taken from the data

        message = ''.join(data_str.split (':')[2:]) # split command from the message
        print('message: ' + message)
        

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data_str)

        print(urls)

        for x in urls:
            irc.send(bytes('PRIVMSG ' + sender(destination, user_nick) + ' :' + link_title(x) + '\r\n', 'UTF-8'))

        else:
            arg = data_str.split( ) # Arguments after the command

            print(arg)

            args = ''
            for index, item in enumerate(arg) : #for every item in arg
                if index == 3:
                    comm = item.lower().replace(':','')
                elif index > 3 :
                    if args == '':
                        args = item
                    else:
                        args += ' ' + item # add the item to the string


            print ('Function is ' + comm + ' From ' + user_nick) # print who commanded
            if comm.find(';') == 0:     # finds ; at the start of the string
                irc.send(bytes('PRIVMSG ' + sender(destination, user_nick) + ' :' + commOpts(comm[1:], args, user_nick) + '\r\n', 'UTF-8'))

