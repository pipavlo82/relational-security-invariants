"""Separately implemented BIP340 equation check; no source-verifier imports.
Same mathematical algorithm, not a claim of algorithm or author independence.
"""
import hashlib,json
P=2**256-2**32-977
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G=(55066263022277343669578718895168534326250603453777594175500187360389116729240,32670510020758816978083085130507043184471273380659243275938904335757337482424)
def add(a,b):
    if a is None:return b
    if b is None:return a
    x,y=a;u,v=b
    if x==u and (y+v)%P==0:return None
    slope=((3*x*x)*pow(2*y,-1,P) if a==b else (v-y)*pow(u-x,-1,P))%P
    xx=(slope*slope-x-u)%P;return xx,(slope*(x-xx)-y)%P
def mul(n,p):
    z=None
    for bit in bin(n)[2:]:
        z=add(z,z)
        if bit=='1':z=add(z,p)
    return z
def valid(ev):
    try:
        raw=json.dumps([0,ev['pubkey'],ev['created_at'],ev['kind'],ev['tags'],ev['content']],ensure_ascii=False,separators=(',',':')).encode()
        msg=hashlib.sha256(raw).digest()
        if msg.hex()!=ev['id']:return False
        key=bytes.fromhex(ev['pubkey']);sig=bytes.fromhex(ev['sig'])
        if len(key)!=32 or len(sig)!=64:return False
        x=int.from_bytes(key,'big');rr=int.from_bytes(sig[:32],'big');s=int.from_bytes(sig[32:],'big')
        if x>=P or rr>=P or s>=N:return False
        yy=(pow(x,3,P)+7)%P;y=pow(yy,(P+1)//4,P)
        if y*y%P!=yy:return False
        if y&1:y=P-y
        tag=hashlib.sha256(b'BIP0340/challenge').digest()
        e=int.from_bytes(hashlib.sha256(tag+tag+sig[:32]+key+msg).digest(),'big')%N
        point=add(mul(s,G),mul(N-e,(x,y)))
        return point is not None and point[0]==rr and point[1]%2==0
    except (KeyError,ValueError,TypeError):return False
