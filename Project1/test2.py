import socket
import sys
import ssl


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    flag = 0
    port = 27993
    if len(sys.argv) > 3:
        if sys.argv[3] == "-s":
            flag = flag + 1
        if sys.argv[1] == "-p":
            flag = flag + 2
            port = sys.argv[2]
        host_name = sys.argv[1 + flag]
        nuid = sys.argv[2 + flag]
    else:
        host_name = sys.argv[1]
        nuid = sys.argv[2]


    s.connect((host_name, int(port)))
    if flag == 3:
        s = ssl.wrap_socket(s)
    s.send("cs3700spring2016 HELLO " + nuid + " \n")
    while 1:
        msg = s.recv(1024)
        if str.startswith(msg, "cs3700spring2016 BYE "):
            print(msg[21:])
            break
        else:
            msg = msg[24:-1]
            msg = str.split(msg, ' ')
            num1 = msg[0]
            num2 = msg[2]
            ops = msg[1]
            msg_string = num1 + ops + num2
            result = eval(msg_string)
            s.send("cs3700spring2016 " + str(result) + "\n")


if __name__ == '__main__':
    main()
