import random
import sympy
from Crypto.Util.number import *
from secret import flag, p

e = 65537
seed = random.randint(2 ** 14, 2 ** 15)
random.seed(seed)
q = sympy.nextprime(random.getrandbits(512))
n = p * q
m = bytes_to_long(flag)
c = pow(m, e, n)
print(n)
print(long_to_bytes(c))
'''
65733969010196175202921423218938408000843083687026217212621116459021635468765553471079037765733153810364049759952771919913067188154079049840404552861186230744890558542190577325835295327840068130131879335623818564919511202372583498297686980169960522765806915027061994807865866249515664338006720445483446544767
b"Y\xed\xdd\xb6\xbd.g#\x9e\x99\x0e'\x02#\x8b\xa3\xfdn\xd1\xbeTp\x04\xf8\xd3,\rJ?\x95\xaa \xc4=E\xa7\xc5'P\xdc\xb8.\xb6\xe52\x05\x14\xc9\xa3\xaa\xc2<\xf2\x9d\xdb\xc8X\x08\x17\xa4\x1c\xd4\xaa\x111>\xa2\xb8#&\nL\x89v]\x87\xdah@\x98\x93 \x8a\xc3N$\xdc\xe4g\x10Jm\x8bh\x0f\xf4\xea\xa5\xd4\xc7\xee\x10\xe1\x12\xc1\xdd05\x1f\n\xcdM\xdd\x88\xd9\t\x87R\xc7\xd9\xf5\x18\xb8)5\x04\x13F"
'''
