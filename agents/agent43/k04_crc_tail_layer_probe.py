"""Read-only K04/TRP2 CRC-layer experiment. Run: python agents/agent43/k04_crc_tail_layer_probe.py case.zip"""
import hashlib, json, re, struct, sys, zlib
from zipfile import ZipFile

RECORDER_SHA="5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
SPOOL_SHA="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
def crc(r): return zlib.crc32(r[:20])
def stored(r): return struct.unpack_from("<I",r,20)[0]
def flip_control(r, change):
    q=bytearray(r);q[12:16]=bytes(x^y for x,y in zip(q[12:16],change))
    return q
def inverse_control(record):
    """Determine the unique offset12..15 control bytes if all other bytes and stored CRC are intact."""
    base=bytearray(record);base[12:16]=b"\0"*4
    c0=crc(base)
    cols=[crc(flip_control(base,(1<<k).to_bytes(4,"little")))^c0 for k in range(32)]
    target=stored(record)^c0
    rows=[sum(((cols[j]>>i)&1)<<j for j in range(32))|(((target>>i)&1)<<32) for i in range(32)]
    for bit in range(32):
        pivot=next(i for i in range(bit,32) if rows[i]&(1<<bit))
        rows[bit],rows[pivot]=rows[pivot],rows[bit]
        for i in range(32):
            if i!=bit and rows[i]&(1<<bit): rows[i]^=rows[bit]
    result=sum(((rows[i]>>32)&1)<<i for i in range(32)).to_bytes(4,"little")
    assert crc(flip_control(base,result))==stored(record)
    return result
def unshift_right(x,k):
    y=x
    for _ in range(6): y=x^(y>>k)
    return y&0xFFFFFFFF
def unshift_left(x,k,m):
    y=x
    for _ in range(6): y=x^((y<<k)&m)
    return y&0xFFFFFFFF
def untemper(x):
    return unshift_right(unshift_left(unshift_left(unshift_right(x,18),15,0xEFC60000),7,0x9D2C5680),11)
def inverse_twist(v):
    parity=v>>31
    return (((v^(0x9908B0DF if parity else 0))<<1)|parity)&0xFFFFFFFF

with ZipFile(sys.argv[1]) as z:
    data=z.read("evidence/recorder/trip-recorder.raw")
    spool=z.read("evidence/print/spool-reconstruction.log")
    route=json.loads(z.read("evidence/recovery-routing.json"))
    acceptance=json.loads(z.read("acceptance.json"))
assert hashlib.sha256(data).hexdigest()==RECORDER_SHA
assert hashlib.sha256(spool).hexdigest()==SPOOL_SHA
assert data[:8]==b"TRP2DUMP" and struct.unpack_from("<HHI",data,8)==(2,24,88)
records=[data[16+24*i:16+24*i+24] for i in range(88)]
assert all(len(r)==24 for r in records)
assert crc(records[0])==stored(records[0])
mask=bytes.fromhex("3F9B320D")
assert inverse_control(flip_control(records[0],mask))==records[0][12:16]
fixed_crc=bytearray(records[0]);fixed_crc[21]^=1
assert crc(fixed_crc)^stored(fixed_crc)==0x100
print("synthetic positive controls PASS")

bad=[]
for i,r in enumerate(records):
    syndrome=crc(r)^stored(r)
    if syndrome:
        alt=inverse_control(r)
        difference=bytes(a^b for a,b in zip(r[12:16],alt))
        bad.append((i,r[12:16],alt,syndrome,difference))
        print("bad",i,"seq",struct.unpack_from("<I",r,8)[0],
              "crc_syndrome",f"{syndrome:08X}","original",r[12:16].hex().upper(),
              "conditional_control_fix",alt.hex().upper(),"difference",difference.hex().upper())
assert [x[0] for x in bad]==[14,41,72,77]
assert all(x[3]==0x100 and x[4]==mask for x in bad)

lines=[l for l in spool.decode().splitlines() if l.startswith("2026-")]
assert len(lines)==133
printer=[]
for row,l in enumerate(lines):
    if row==129: continue
    p=bytes.fromhex(re.search("PAYLOAD=([0-9A-F]{32})",l).group(1))
    printer += [(row,j,untemper(w)) for j,w in enumerate(struct.unpack("<4I",p))]
assert len(printer)==528
for idx,raw,alt,_,_ in bad:
    x=untemper(int.from_bytes(alt,"little"))
    matches=[]
    for j,(_,_,u) in enumerate(printer):
        for right in printer[j+1:]:
            if (inverse_twist(u^right[2])&0x7FFFFFFF)==(x&0x7FFFFFFF):
                matches.append((printer[j][:2],right[:2]))
    print("conditional_control_bridge",idx,"matches",matches)
    assert not matches
print("source-only inverse-twist fingerprint tests 556512, matches 0")
# Discriminate CRC-field damage versus control-field damage independently of CRC.
# Original raw row72's full untempered word has a pre-existing exact printer
# inverse-twist witness; replacing its control bytes would destroy that match.
for idx,raw,alt,_,_ in bad:
    x=untemper(int.from_bytes(raw,"little"))
    matches=[]
    for j,(_,_,u) in enumerate(printer):
        for right in printer[j+1:]:
            if inverse_twist(u^right[2])==x:
                matches.append((printer[j][:2],right[:2]))
    print("raw_bad_crc_control_bridge",idx,"matches",matches)
    assert matches==([((10,2),(41,2))] if idx==72 else [])


selected=[l for l in lines if "JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK CLASS=RECOVER" in l]
assert len(selected)==1
p=bytes.fromhex(re.search("PAYLOAD=([0-9A-F]{32})",selected[0]).group(1))
m=bytes.fromhex(route["K04"]["masked_component"])
wanted=acceptance["slot_sha256"]["K04"]
hits=[]
for orientation,four in [("source",mask),("reversed",mask[::-1])]:
    for subset in range(1,16):
        trial=bytearray(p)
        for w in range(4):
            if subset&(1<<w):
                for j in range(4):trial[4*w+j]^=four[j]
        component=bytes(a^b for a,b in zip(trial,m))
        if hashlib.sha256(component).hexdigest()==wanted:
            hits.append((orientation,subset,component.hex().upper()))
print("K04 30 source-motif lane-repair candidates", "matches",hits)
assert not hits
print("no authenticated K04 coupon bytes recovered; K08 remains missing")
