"""Small x86-32 disassembly helper used to analyse Terrain.dll (needs: pip install pefile capstone).

  TERRAIN_DLL=".../Program_Files_(ENGLISH)/Terrain.dll" python3 x86dis.py tileAt getElevation
  python3 -c "from x86dis import *; show(0x76e0, 'loadTextures', 600)"   # any RVA

Follows the incremental-link jump thunks, filters debug-build noise, and annotates string
references, imported OpenGL calls and floating point constants.
"""
import os, sys, pefile, struct
from capstone import *
PATH=os.environ.get("TERRAIN_DLL","game/Program_Files_(ENGLISH)/Terrain.dll")  # path to your own copy of Terrain.dll
pe=pefile.PE(PATH); data=open(PATH,'rb').read(); base=pe.OPTIONAL_HEADER.ImageBase
md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=False
def rva2off(r):
    for s in pe.sections:
        if s.VirtualAddress<=r<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(r-s.VirtualAddress)
def read(rva,n): o=rva2off(rva); return data[o:o+n]
exports={s.name.decode():s.address for s in pe.DIRECTORY_ENTRY_EXPORT.symbols}
def resolve(rva):
    b=read(rva,5)
    if b[0]==0xE9: return rva+5+struct.unpack('<i',b[1:])[0]
    return rva
def dis(rva,maxins=120,stop_ret=True,label=""):
    print(f"--- {label} @ {hex(rva)}")
    n=0
    for i in md.disasm(read(rva,1200),base+rva):
        print(f"  {i.address-base:06x}: {i.mnemonic:6s} {i.op_str}")
        n+=1
        if (stop_ret and i.mnemonic in('ret',) and n>2) or n>=maxins: break
if __name__=="__main__":
    for name in sys.argv[1:]:
        k=[e for e in exports if name in e][0]
        r=resolve(exports[k]); dis(r,label=k)

import re
def cstring_at(va):
    r=va-base
    o=rva2off(r)
    if o is None: return None
    b=data[o:o+80]; z=b.find(b'\0')
    if z>=3 and all(32<=c<127 for c in b[:z]): return b[:z].decode()
IAT={}
for d in pe.DIRECTORY_ENTRY_IMPORT:
    for im in d.imports:
        if im.name: IAT[im.address]=im.name.decode()
def show(rva,label,maxins=400,skipnoise=True):
    r=resolve(rva)
    print(f"--- {label}: {hex(rva)} -> {hex(r)}")
    n=0
    for i in md.disasm(read(r,6000),base+r):
        s=f"{i.mnemonic:6s} {i.op_str}"
        if skipnoise and (s.strip() in ('mov    esi, esp','cmp    esi, esp','call   0x100180a0') or ('cccccccc' in s) or ('rep stosd' in s) or ('ebp - 0x' in s and 'lea' in s and 'edi' in s)): continue
        note=""
        mm=re.search(r'\[0x(1[0-9a-f]{7})\]',i.op_str)
        if mm and int(mm.group(1),16) in IAT and i.mnemonic=='call': note=f'    ; {IAT[int(mm.group(1),16)]}'
        fm=re.search(r'(dword|qword) ptr \[0x(1[0-9a-f]{7})\]',i.op_str)
        if fm and i.mnemonic.startswith('f'):
            o=rva2off(int(fm.group(2),16)-base)
            if o and o+8<=len(data):
                import struct as _s
                v=_s.unpack('<f',data[o:o+4])[0] if fm.group(1)=='dword' else _s.unpack('<d',data[o:o+8])[0]
                note=f'    ; = {v:g}'
        for m in re.finditer(r'0x(1[0-9a-f]{7})',i.op_str):
            sv=cstring_at(int(m.group(1),16))
            if sv: note=f'    ; "{sv}"'
        print(f"  {i.address-base:06x}: {s}{note}")
        n+=1
        if (i.mnemonic=='ret' and n>3) or n>=maxins: break
