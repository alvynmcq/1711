; ============================================================
;  1711 - the boot stub (v0.7), as in Night Porter. Assembled
;  inside abuf (night.asm), the veil buffer, so it costs nothing
;  on the tape: it runs once at startup, before abuf is first used.
;
;  B_boot: loads each bank from the headerless tape blocks after
;  the code (B_tab in banks.inc, written by build.py: 7FFDh value,
;  where it loads, length, where it unpacks or 0 if raw), unpacks
;  a packed one in place with ZX0, then writes the IM2 jump and
;  table (FDFDh-FF00h) into every bank that can be at C000h.
;  Carry set = all loaded; carry clear = a tape error or BREAK.
;  Bank 0 is paged back in either way. Runs under IM1 (the ROM's
;  interrupt) with BASIC's stack; main.asm turns IM2 on after.
; ============================================================

B_boot: ld hl,B_tab
bb1:    ld a,(hl)
        or a
        jr z,bb_vec
        inc hl
        ld bc,7FFDh
        out (c),a
        ld e,(hl)
        inc hl
        ld d,(hl)
        inc hl
        push de
        pop ix              ; IX = where it loads
        ld e,(hl)
        inc hl
        ld d,(hl)
        inc hl              ; DE = length
        ld c,(hl)
        inc hl
        ld b,(hl)
        inc hl              ; BC = where it unpacks (0: raw)
        push hl
        push bc
        push ix
        ld a,0FFh           ; a headerless data block
        scf
        call B_ldbytes
        pop hl              ; HL = where it loaded
        pop de              ; DE = where it unpacks
        jr nc,bb_fail
        ld a,d
        or e
        call nz,dzx0_standard
        pop hl
        jr bb1
bb_fail:
        pop hl
        call B_bank0
        or a
        ret

bb_vec: ld hl,B_all         ; the IM2 jump and table in every bank
bb2:    ld a,(hl)
        inc hl
        or a
        jr z,bb_ok
        push hl
        ld bc,7FFDh
        out (c),a
        ld hl,0FE00h        ; FE00h-FF00h = FDh, FDFDh = JP isr
        ld de,0FE01h
        ld bc,256
        ld (hl),0FDh
        ldir
        ld a,0C3h
        ld (0FDFDh),a
        ld hl,isr
        ld (0FDFEh),hl
        pop hl
        jr bb2
bb_ok:  call B_bank0
        scf
        ret

B_bank0:
        xor a
        jp page

B_all:  db 10h,11h,13h,14h,16h,17h,0

; The ROM's LD-BYTES (0556h), entered so that it comes back here
; rather than to SA/LD-RET, which reports BREAK as a BASIC error.
B_ldbytes:
        inc d
        ex af,af'
        dec d
        di
        ld a,0Fh
        out (0FEh),a
        ld hl,B_ldret
        push hl
        in a,(0FEh)
        rra
        and 20h
        or 02h
        ld c,a
        cp a
        jp 056Bh            ; LD-BREAK, then the ROM loader proper
B_ldret:
        push af
        xor a
        out (0FEh),a        ; black border, like the loading screen
        pop af
        ei
        ret
