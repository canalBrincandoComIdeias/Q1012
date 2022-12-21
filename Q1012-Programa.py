#     AUTOR:    BrincandoComIdeias
#     APRENDA:  https://cursodearduino.net/
#     SKETCH:   Fontes e Baterias para o Pico
#     DATA:     14/12/22

import machine
from utime import sleep as delay 


pinCTRLX = machine.ADC(27)
pinCTRLY = machine.ADC(26)
pinCTRLZ = machine.Pin(22, machine.Pin.IN)

pinGarra = machine.Pin(21)
pinPulso = machine.Pin(20)
pinBraco = machine.Pin(19)
pinBase  = machine.Pin(18)

garra = machine.PWM(pinGarra)
garra.freq(50) #Frequencia do sinal do Servo

pulso = machine.PWM(pinPulso)
pulso.freq(50) #Frequencia do sinal do Servo

braco = machine.PWM(pinBraco)
braco.freq(50) #Frequencia do sinal do Servo

base = machine.PWM(pinBase)
base.freq(50) #Frequencia do sinal do Servo

posX = 90
posY = 90
estadoGarra = 1
posZAnt = 0

neutroX = 86
neutroY = 86
faixaNeutra = 10

# Equivalente a função map()
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Converte um angulo no valor de pulso do Servo
def pulsoServo(x):
    if (x <= 0) :
        return 3276 # 1 mS = 0º
    elif (x >= 180) :
        return 6553 # 2 mS = 180º
    else :
        return map(x, 0, 180, 3276, 6553) 

while True:
    
    leituraX = pinCTRLX.read_u16() # 0 ~ 65535
    anguloX = map(leituraX, 0, 65535, 180, 0)
    
    if anguloX > (neutroX + faixaNeutra):
        posX = posX + ((((anguloX - faixaNeutra) - neutroX) / 10)) ** 1
        posX = int(min(posX, 180))
        
    if anguloX < (neutroX - faixaNeutra):
        posX = posX - (((neutroX - (anguloX + faixaNeutra)) / 10)) ** 1
        posX = int(max(posX, 0))
    
    leituraY = pinCTRLY.read_u16() # 0 ~ 65535
    anguloY = map(leituraY, 0, 65535, 180, 0)
    
    if anguloY > (neutroY + faixaNeutra):
        posY = posY + ((((anguloY - faixaNeutra) - neutroY) / 10)) ** 1
        posY = int(min(posY, 180))
        
    if anguloY < (neutroY - faixaNeutra):
        posY = posY - (((neutroY - (anguloY - faixaNeutra)) / 10)) ** 1
        posY = int(max(posY, 0))
    
    base.duty_u16(pulsoServo(posX))
    braco.duty_u16(pulsoServo(posY))
    pulso.duty_u16(pulsoServo(posY))
    
    posZ = pinCTRLZ.value()
    if posZ and not posZAnt:
        estadoGarra = not estadoGarra
    
    if estadoGarra:
        garra.duty_u16(pulsoServo(70))
    else:
        garra.duty_u16(pulsoServo(20))
    
    print(f"LeituraX: {leituraX}\t AnguloX: {anguloX}\t PosX: {posX}\t LeituraY: {leituraY}\t AnguloY: {anguloY}\t PosY: {posY}   ", end='\r')
    
    delay(0.05) # delay de 50mS
    
    posZAnt = posZ