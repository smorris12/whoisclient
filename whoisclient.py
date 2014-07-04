__author__ = 'smorris'

# Just experimenting with a whois client

# Imports
import telnetlib
import sys

# Use a simple telnet connection to query the whois server
def telnet_connect(server):
    # Open a telnet server return a connection object
    connection = telnetlib.Telnet(server, 43)
    return connection

def querywhois_server_list(domain, site):
    #parse the whois server list to find the right server for domain
    # Let's test if it is a ip address though and if so skip to arin for now
    try:
        is_number = int(domain)
        test_whois = make_whois_connection("whois.arin.net", site + "\n")
        if "APNIC" in test_whois:
            return "whois.apnic.net"
        else:
            return "whois.arin.net"
    except:
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

def format_query(query_site, server):
    # Determine if commands need to be added to the query
    try:
        is_number = int(query_site[0])
        if server == "whois.arin.net":
            output_site = "n " + query_site + "\n"
            return output_site
        else:
            return query_site + "\n"
    except:
        return query_site + "\n"

def make_whois_connection(server_name, query):
    if server_name == "whois.arin.net":
        query = "n " + query

    whois_connection = telnet_connect(server_name)
    whois_connection.write(query)
    output = whois_connection.read_all()
    whois_connection.close()
    return output

if __name__ == "__main__":
    # Get 1st argument from the command line
    try:
        input_site = sys.argv[1]
    except:
        input_site = raw_input('Please enter an address to whois: ')

    who_server = querywhois_server_list(parse_domain(input_site), input_site)

    # If the domain can't be parsed or their is no whois server
    if who_server == False:
        print 'Domain does not have a valid whois server'
    else:
        print make_whois_connection(who_server, format_query(input_site, who_server))