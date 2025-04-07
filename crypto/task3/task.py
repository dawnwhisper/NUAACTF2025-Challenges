import ast
import hashlib
import random
import socketserver
import gmpy2
import sympy
from Crypto.Util.number import *
from secret import flag


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        data = b''
        while True:
            part = self.request.recv(2048)
            data += part
            if len(part) < 2048:
                break
        return data.strip()

    def send(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def handle(self):
        bound = getPrime(round(20.25))
        a = [random.randint(0, bound) for _ in range(64)]
        random.seed(bound)
        p, q = sympy.nextprime(random.getrandbits(512)), sympy.nextprime(random.getrandbits(512))
        n = p * q
        phi = (p - 1) * (q - 1)
        while True:
            e = 7 * phi + getPrime(16)
            try:
                d = gmpy2.invert(e, phi)
                break
            except:
                continue
        e_bin = bin(e)[2:]
        self.send(
            f'''
This is an RSA system!
Here are some codes for you:
bound=getPrime(round(20.25))
a=[random.randint(0,bound) for i in range(64)]
random.seed(bound)
p, q = sympy.nextprime(random.getrandbits(512)),sympy.nextprime(random.getrandbits(512))
Now give you sha256(bound):{hashlib.sha256(str(bound).encode()).hexdigest()}
give you a:{a}\n'''.encode()
        )
        self.send(
            f'''
\nNow, give me your vector v1 (e_length={e.bit_length()}
doing:
v1=[]
for i in range(e.bit_length()):
    self.send(f"v1{{i}}=".encode())
    num = int(self._recvall().rstrip(b'\n').decode())
    v1.append(num)
for i in range(e.bit_length()):
    sum += int(e_bin[i]) * int(v1[i])
a,b = [getPrime(1024) for _ in range(2)]
k = (sum << 2400) // (b + a)
end.\n'''.encode()
        )
        try:
            v1 = []
            for i in range(e.bit_length()):
                self.send(f"v1{i}=".encode())
                num = int(self._recvall().rstrip(b'\n').decode())
                v1.append(num)
            assert len(v1) == len(e_bin)
            sum = 0
            for i in range(e.bit_length()):
                sum += int(e_bin[i]) * int(v1[i])
            self.send(f"接收完成\n".encode())
            a, b = [getPrime(1024) for _ in range(2)]
            k = (sum << 2400) // (b + a)
        except Exception as err:
            self.send(f"err={err}".encode())
            return
        self.send(f"""
k={k}\nGive me your e, I will decrypt to get flag (flag=pow(c,e,n),using RSA encryption)\n
        """.encode())
        try:
            e = int(self._recvall().rstrip(b'\n').decode())
        except:
            return
        if e <= 20:
            self.send("e过小(Need e>20".encode())
            return
        if e >= 100000:
            self.send("e过大(Need e<100000".encode())
            return
        c = pow(bytes_to_long(flag.encode()), d, n)
        decrypted_flag = long_to_bytes(pow(c, e, n))
        self.send(f"flag={decrypted_flag.decode()}\n".encode())


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10080
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    print(HOST, PORT)
    server.serve_forever()
