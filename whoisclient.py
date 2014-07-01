__author__ = 'smorris'
#!

# Just experimenting with a whois client

# Much thanks to the code on this page: http://www.binarytides.com/python-program-to-fetch-domain-whois-data-using-sockets/

# Imports
import socket
import sys

# function with sockets to open and read data from a whois query
def querywhois(server, domain):
    #setup a connection to specified server
    whoissocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    whoissocket.connect((server, 43))

    #take the given query and send it to the server
    whoissocket.send(domain + '\r\n')
    whoisdata = whoissocket.recv(10000)
    whoissocket.close()
    return whoisdata

def querywhois_server_list(domain):
    #parse the whois server list to find the right server for domain
    server_list = open('whois-servers.txt', 'r')
    whois_server = False
    for line in server_list:
        if domain == line[:line.find(" ")]:
            whois_server = line[line.find(" "):].strip()
    return whois_server

def parse_domain(site):
    # Parse the address for a top level domain
    top_domain = site[site.rindex(".") + 1:]
    return top_domain

if __name__ == "__main__":
    # Get 1st argument from the command line
    try:
        input_site = sys.argv[1]
    except:
        input_site = raw_input('Please enter an address to whois: ')

    who_server = querywhois_server_list(parse_domain(input_site))

    # If the domain can't be parsed or their is no whois server
    if who_server == False:
        print 'Domain not found'
    else:
        print querywhois(who_server, input_site)
