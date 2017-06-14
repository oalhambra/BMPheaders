
def longitudes_validas(longitud):
    longitudes = []
    for i in range(17):
        if (longitud - i) % 3 == 0:
            longitudes.append((longitud - i) - 54)
    return longitudes

def calcular_divisores(dividendo):
    divisor = []
    for i in range(1,dividendo+1):
        if dividendo%i==0:
            divisor.append(i)
    return divisor

def padhexa(s):
    return s[2:].zfill(8)

def inserta_tamaño(longitud_hex_list, cabecera):
    cabecera[34]=longitud_hex_list[0]
    cabecera[35] = longitud_hex_list[1]
    cabecera[36] = longitud_hex_list[2]
    cabecera[37] = longitud_hex_list[3]
    return cabecera
def inserta_alto(alto_list,cabecera):
    cabecera[22]=alto_list[0]
    cabecera[23] = alto_list[1]
    cabecera[24] = alto_list[2]
    cabecera[25] = alto_list[3]
    return cabecera
def inserta_ancho(ancho_list,cabecera):
    cabecera[18]=ancho_list[0]
    cabecera[19] =ancho_list[1]
    cabecera[20] = ancho_list[2]
    cabecera[21] = ancho_list[3]
    return cabecera

in_file = open("entrada.bmp", "rb")
data = in_file.read()
in_file.close()
longitud=data.__len__()-54 # calcula longitud de los datos

longitudes=longitudes_validas(data.__len__()) # considera el padding realizado en el cifrado y genera lista de todas las posibles longitudes
datos=data[54:] # toma los datos de la imagen y quita la cabecera
datos_str=datos.hex() # convierte datos a valores hexadecimales
# formato de la cabecera correcto, los valores '--' son los variables
correct_header=['42','4d','00','00','00','00','00','00','00','00','36','00','00','00','28','00','00','00',
                '--','--','--','--','--','--','--','--','01','00','18','00','00','00','00','00','--','--','--','--',
                '00','00','00','00','00','00','00','00','00','00','00','00','00','00','00','00']

cuenta_imagenes=0

for i in longitudes:
    # calculamos las posibles dimensiones de la imagen
    dividendo=int(i/3)
    divisores=calcular_divisores(dividendo)
    dimensiones_validas=[]
    for j in range (divisores.__len__()):
        dimension=[divisores[j], divisores[(divisores.__len__() - 1) - j]]
        dimensiones_validas.append(dimension)
        # fin del calculo de las posibles dimensiones
        # convierte dimensiones y longitud correspondiente a hexadecimal
    for k in dimensiones_validas:
        alto=padhexa(hex(k[0]))
        alto_list=[]
        for l in range(4):
            alto_list.append(alto[:2])
            alto=alto[2:]
        ancho=padhexa(hex(k[1]))
        ancho_list=[]
        for l in range(4):
            ancho_list.append(ancho[:2])
            ancho=ancho[2:]
        longitud_hex=padhexa(hex(i))
        longitud_hex_list=[]
        for l in range(4):
            longitud_hex_list.append(longitud_hex[:2])
            longitud_hex=longitud_hex[2:]
        # invierte las listas porque el primer byte que aparece en el fichero en cualquiera de los casos es el menos significativo
        alto_list=alto_list[::-1]
        ancho_list=ancho_list[::-1]
        longitud_hex_list=longitud_hex_list[::-1]
        # inserta los valores calculados en la cabecera
        cabecera=correct_header.copy()
        cabecera=inserta_tamaño(longitud_hex_list,cabecera)
        cabecera=inserta_alto(alto_list,cabecera)
        cabecera=inserta_ancho(ancho_list,cabecera)
        cabecera_str=''.join(cabecera)
        cabecera_byte=bytearray.fromhex(cabecera_str)
        total=cabecera_byte+bytearray.fromhex(datos_str)
        #guarda la imagen
        f = open('salida'+str(cuenta_imagenes)+'.bmp', 'wb')
        cuenta_imagenes+=1
        f.write(total)
        f.close()