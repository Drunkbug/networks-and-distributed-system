CS 3700 - Networks and Distributed System Project-1 README

Language used : Python
For Project1 our high level approach was to use sockets to connect to the server. Once connected, we 
used a while loop to recieve the problems, solve them and send them back to the server. We broke the 
while loop using a check to see if we recieved a message starting with "cs3700spring2016 BYE". After 
recieving this message we split the message to isolate the secret flag. This secret flag was tested
to see if it was 64 bytes. If the test passes, the secret flag is printed to the user. One of the
challenges we faced was because we used sys.argv. Since we used sys.argv, we had to check the number 
of arguements we recieved and keep a count on the number of flags we added in order to map the right
arguements and connect to the server. In order to confirm that we recieved the right secret flag, we
checked if the secret flag was 64 bytes and we made sure the socket was connecting to the right 
sockket by using the function gethostbyname. If the gethostname was not the same as the host_name sent 
by the user, an exception is thrown and the sockect connection is closed.
 