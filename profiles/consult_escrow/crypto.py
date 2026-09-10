"""Independent integer implementation of Keccak-256 and secp256k1 recovery.
Not a production wallet library. Inputs are public conformance signatures.
No EVM, adapter, ethers, source execution, or expectation artifact dependency.
"""
MASK=(1<<64)-1
RC=(1,0x8082,0x800000000000808a,0x8000000080008000,0x808b,0x80000001,0x8000000080008081,0x8000000000008009,0x8a,0x88,0x80008009,0x8000000a,0x8000808b,0x800000000000008b,0x8000000000008089,0x8000000000008003,0x8000000000008002,0x8000000000000080,0x800a,0x800000008000000a,0x8000000080008081,0x8000000000008080,0x80000001,0x8000000080008008)
ROT=((0,36,3,41,18),(1,44,10,45,2),(62,6,43,15,61),(28,55,25,21,56),(27,20,39,8,14))
def rol(v,n):return ((v<<n)|(v>>(64-n)))&MASK

def keccak(data):
    pad=bytearray(data);pad.append(1)
    pad.extend(bytes((-len(pad))%136));pad[-1]|=128
    a=[0]*25
    for offset in range(0,len(pad),136):
        for i in range(17):a[i]^=int.from_bytes(pad[offset+8*i:offset+8*i+8],'little')
        for rc in RC:
            c=[a[x]^a[x+5]^a[x+10]^a[x+15]^a[x+20] for x in range(5)]
            d=[c[(x-1)%5]^rol(c[(x+1)%5],1) for x in range(5)]
            for x in range(5):
                for y in range(5):a[x+5*y]^=d[x]
            b=[0]*25
            for x in range(5):
                for y in range(5):b[y+5*((2*x+3*y)%5)]=rol(a[x+5*y],ROT[x][y])
            for x in range(5):
                for y in range(5):a[x+5*y]=b[x+5*y]^((~b[(x+1)%5+5*y])&b[(x+2)%5+5*y])
            a[0]^=rc
    return b''.join(x.to_bytes(8,'little') for x in a)[:32]
P=2**256-2**32-977
N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
G=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
def add(a,b):
    if a is None:return b
    if b is None:return a
    x,y=a;u,v=b
    if x==u and (y+v)%P==0:return None
    m=((3*x*x)*pow(2*y,-1,P) if a==b else (v-y)*pow(u-x,-1,P))%P
    q=(m*m-x-u)%P
    return q,(m*(x-q)-y)%P

def mul(k,p=G):
    r=None
    while k:
        if k&1:r=add(r,p)
        p=add(p,p);k>>=1
    return r

def recover(digest,signature):
    raw=bytes.fromhex(signature[2:]);r=int.from_bytes(raw[:32],'big');s=int.from_bytes(raw[32:64],'big');v=raw[64]
    if not 0<r<N or not 0<s<N or v not in (27,28):return '0x'+'0'*40
    y=pow((r*r*r+7)%P,(P+1)//4,P)
    if (y*y-r*r*r-7)%P:return '0x'+'0'*40
    if y%2!=v-27:y=P-y
    q=mul(pow(r,-1,N),add(mul(s,(r,y)),mul((-int.from_bytes(digest,'big'))%N)))
    if q is None:return '0x'+'0'*40
    return '0x'+keccak(q[0].to_bytes(32,'big')+q[1].to_bytes(32,'big'))[-20:].hex()

def commitment(job,result):return keccak(bytes.fromhex(job[2:]+result[2:]))
def signer(job,result,signature):return recover(keccak(b'\x19Ethereum Signed Message:\n32'+commitment(job,result)),signature)
