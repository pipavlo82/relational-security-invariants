"""Separate Python Keccak/RLP/path obligations; no JavaScript or adapter calls.

Bounded account inclusion/non-inclusion oracle, not a general consensus verifier.
"""
MASK=(1<<64)-1
ROT=((0,36,3,41,18),(1,44,10,45,2),(62,6,43,15,61),(28,55,25,21,56),(27,20,39,8,14))
RC=(0x1,0x8082,0x800000000000808a,0x8000000080008000,0x808b,0x80000001,0x8000000080008081,0x8000000000008009,0x8a,0x88,0x80008009,0x8000000a,0x8000808b,0x800000000000008b,0x8000000000008089,0x8000000000008003,0x8000000000008002,0x8000000000000080,0x800a,0x800000008000000a,0x8000000080008081,0x8000000000008080,0x80000001,0x8000000080008008)
def rotate(v,n):return ((v<<n)|(v>>(64-n)))&MASK
def keccak(data):
    padded=bytearray(data);padded.append(1)
    padded.extend(b'\0'*((-len(padded))%136));padded[-1]|=128
    a=[0]*25
    for offset in range(0,len(padded),136):
        for j in range(17):a[j]^=int.from_bytes(padded[offset+j*8:offset+j*8+8],'little')
        for rc in RC:
            c=[a[x]^a[x+5]^a[x+10]^a[x+15]^a[x+20] for x in range(5)]
            d=[c[(x-1)%5]^rotate(c[(x+1)%5],1) for x in range(5)]
            b=[0]*25
            for x in range(5):
                for y in range(5):b[y+5*((2*x+3*y)%5)]=rotate(a[x+5*y]^d[x],ROT[x][y])
            for x in range(5):
                for y in range(5):a[x+5*y]=b[x+5*y]^((~b[(x+1)%5+5*y])&b[(x+2)%5+5*y])
            a[0]^=rc
    return b''.join(x.to_bytes(8,'little') for x in a)[:32]

def rlp(data):
    def item(at):
        if at>=len(data):raise ValueError('truncated RLP')
        tag=data[at]
        if tag<128:return bytes([tag]),at+1
        is_list=tag>=192;base=192 if is_list else 128;short=tag-base
        if short<=55:n=short;start=at+1
        else:
            width=short-55;start=at+1+width
            if start>len(data) or data[at+1]==0:raise ValueError('RLP length')
            n=int.from_bytes(data[at+1:start],'big')
            if n<56:raise ValueError('noncanonical RLP length')
        end=start+n
        if end>len(data):raise ValueError('truncated payload')
        if not is_list:
            if n==1 and data[start]<128:raise ValueError('noncanonical RLP byte')
            return data[start:end],end
        out=[]
        while start<end:
            v,start=item(start);out.append(v)
        if start!=end:raise ValueError('RLP list boundary')
        return out,end
    result,end=item(0)
    if end!=len(data):raise ValueError('RLP trailing data')
    return result

def nibbles(raw):return [n for b in raw for n in (b>>4,b&15)]
def account(proof,address):
    nodes=[bytes.fromhex(h[2:]) for h in proof]
    by_hash={keccak(n):n for n in nodes}
    reference=keccak(nodes[0]);path=nibbles(keccak(bytes.fromhex(address[2:])))
    for _ in range(65):
        if not reference:return None
        if type(reference) is list:node=reference
        else:
            raw=by_hash.get(reference) if len(reference)==32 else reference
            if raw is None:raise ValueError('missing committed path node')
            node=rlp(raw)
        if len(node)==17:
            if not path:return node[16] or None
            reference=node[path.pop(0)];continue
        if len(node)!=2:raise ValueError('MPT arity')
        compact=nibbles(node[0]);flag=compact[0]
        if flag>3 or (not flag&1 and compact[1]!=0):raise ValueError('hex-prefix')
        segment=compact[1:] if flag&1 else compact[2:]
        if path[:len(segment)]!=segment:return None
        path=path[len(segment):]
        if flag&2:return node[1] if not path else None
        reference=node[1]
    raise ValueError('path depth')

def derive(v,relation):
    try:leaf=account(v['response']['accountProof'],v['address'])
    except ValueError as e:
        if str(e)!='missing committed path node':raise
        return dict(relation_id=relation,relation_state='account_observed',outputs=dict(verified=False,boundToHeader=None,claimMatchesProof=None,provenBalanceWei=None,accountExists=None,stateTrust='MPT-REJECTED',headerTrust='RPC-TRUSTED',overall='rejected',headerAuthority='UNSUPPORTED',downstreamAuthority='UNSUPPORTED'))
    balance=int.from_bytes(rlp(leaf)[1],'big') if leaf is not None else 0
    bound=keccak(bytes.fromhex(v['response']['accountProof'][0][2:]))==bytes.fromhex(v['header']['stateRoot'][2:])
    matches=balance==int(v['response']['balance'],16);ok=bound and matches
    outputs=dict(verified=ok,boundToHeader=bound,claimMatchesProof=matches,provenBalanceWei=str(balance),accountExists=leaf is not None,stateTrust='RE-DERIVED' if ok else 'UNVERIFIED',headerTrust='RPC-TRUSTED',overall='state-proven / header RPC-TRUSTED' if ok else 'rejected',headerAuthority='UNSUPPORTED',downstreamAuthority='UNSUPPORTED')
    return dict(relation_id=relation,relation_state='account_observed',outputs=outputs)
