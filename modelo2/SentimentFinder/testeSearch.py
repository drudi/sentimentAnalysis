from sentilex import *
from sentifinder import *

sl = Sentilex("../SentiLex-PT02")
sf = SentiFinder(sl)

texto = "Perda de tempo, e quando optei por cancelar me ligaram insistindo que permanecesse. Resultado, perdi mais dinheiro. NÃO DESEJO SER CONTATADA POR TELEFONE PARA REATIVAÇÃO DA ASSINATURA!"
texto2 = "não... talves um maior período gratuito. pois se estou procurando emprego não tenho recursos para pagar esta mensalidade alta."

sl.searchFlex(texto)

sf.scoreFromText(texto)