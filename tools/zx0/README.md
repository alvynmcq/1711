# ZX0 (vendored)

ZX0 by Einar Saukas (https://github.com/einar-saukas/ZX0), BSD 3-Clause
licence (see LICENSE). Copied from commit ecde3a2:
the compressor source (`src/`) and two Z80 decoders: `z80/dzx0_turbo.asm`
(the game's `unlz` in src/porter.asm, for fast camera switches) and
`z80/dzx0_standard.asm` (`L_unlz` in src/low128.asm, 128K scare frames).

`art/zx0.py` compiles `src/` to `tools/zx0/zx0` with `cc` the first time
it's needed, and checks every stream it makes with a Python decoder.
