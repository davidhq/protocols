import sys
sys.path.insert(0, 'ethsnarks')
import os.path
import json

from ethsnarks.poseidon import poseidon, poseidon_params
from ethsnarks.field import SNARK_SCALAR_FIELD

def sigma_EVM_asm(o, t):
    nt = "n" + t
    o = o + nt + " := mulmod(" + t + ", " + t + ", q)\n"
    o = o + nt + " := mulmod(" + nt + ", " + nt + ", q)\n"
    o = o + nt + " := mulmod(" + t + ", " + nt + ", q)\n"
    return o

def poseidon_EVM_asm(params):
    ts = "t0"
    nts = "nt0"
    for t in range(1, params.t):
        ts = ts + ", t" + str(t)
        nts = nts + ", nt" + str(t)

    o = ""

    o = o + "function mix(" + ts + ", q) -> " + nts + " {\n"
    for i in range(params.t):
        for j in range(params.t):
            mulmod = "mulmod(t" + str(j) + ", " + str(params.constants_M[i][j]) + ", q)"
            if j == 0:
                o = o + "nt" + str(i) + " := " + mulmod + "\n"
            else:
                o = o + "nt" + str(i) + " := addmod(nt" + str(i) + ", " + mulmod + ", q)\n"
    o = o + "}\n"
    o = o + "\n"

    o = o + "function ark(" + ts + ", q, c) -> " + nts + " {\n"
    for t in range(params.t):
        o = o + "nt" + str(t) + " := addmod(t" + str(t) + ", c, q)\n"
    o = o + "}\n"
    o = o + "\n"

    o = o + "function sbox_full(" + ts + ", q) -> " + nts + " {\n"
    for j in range(params.t):
        o = sigma_EVM_asm(o, "t" + str(j))
    o = o + "}\n"
    o = o + "\n"

    o = o + "function sbox_partial(t, q) -> nt {\n"
    o = sigma_EVM_asm(o, "t")
    o = o + "}\n"
    o = o + "\n"

    o = o + "let q := " + str(params.p) + "\n\n"
    for i in range(params.nRoundsF + params.nRoundsP):
        o = o + "// round " + str(i) + "\n"
        # ark
        o = o + ts + " := ark(" + ts + ", q, " + str(params.constants_C[i]) + ")\n"
        # sbox
        if (i < params.nRoundsF/2) or (i >= params.nRoundsF/2 + params.nRoundsP):
            o = o + ts + " := sbox_full(" + ts + ", q)\n"
        else:
            o = o + "t0 := sbox_partial(t0, q)\n"
        # mix
        o = o + ts + " := mix(" + ts + ", q)\n"

    return o

poseidonParamsEVM = poseidon_params(SNARK_SCALAR_FIELD, 5, 6, 52, b'poseidon', 5, security_target=128)
data = poseidon_EVM_asm(poseidonParamsEVM)
print(data)