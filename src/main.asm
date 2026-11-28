; ============================================================
;  1711  (working title) - v0.9: title, prologue, the trial (a
;  witness's cross-examination), credits
;  ZX Spectrum 128K. pasmo syntax. Loaded at 6000h by the BASIC
;  loader (CLEAR 24575). Everything here stays below C000h; the
;  scripts, pictures and the trial are in banks paged in at C000h
;  (src/boot.asm loads them, build.py writes src/banks.inc).
;
;  The game is driven by scripts (src/script.inc, compiled by
;  scripts/script.py): a byte opcode, then its arguments.
; ============================================================
        ORG 6000h

ATTR    EQU 5800h
PROMPTC EQU 0C7h            ; FLASH + BRIGHT white: the SPACE prompt
MARGIN  EQU 4               ; pixels of left margin on every line of text

start:
        call detect128
        jr z,is128
        ld a,07h            ; a 48K: say so and stop
        call clsa
        ld hl,msg48
        call textat
        ld hl,msg48b
        call textat
stop48: halt
        jr stop48

is128:  xor a               ; bank 0 at C000h, 48 BASIC ROM
        call page
        call B_boot         ; load the banks (the stub, in abuf)
        jr c,booted
        ld a,07h            ; a tape error or BREAK: say so and stop
        call clsa
        ld hl,msgtape
        call textat
        ld hl,msgtapeb
        call textat
stopt:  halt
        jr stopt

booted: di                  ; IM2: FDFDh jumps to isr, in every bank
        ld a,0FEh
        ld i,a
        im 2
        ld sp,5C00h         ; the stack in 5B00h-5BFFh: BASIC is done with
        ei
        xor a
        ld (border),a
        out (254),a
game:   xor a               ; chunk 0: the title
        call loadchunk
        call run            ; the scripts LOAD one another
        jr game

loadchunk:                  ; unpack script chunk A to SBUF (its bank stays in); HL = SBUF
        ld hl,chunktab
        call farent
        call page
        ld de,SBUF
        call dzx0_standard
        ld hl,SBUF
        ret

;  ---- Banks. curbank is the bank at C000h, written before the OUT
; so an interrupt that pages (the music, later) always puts the right
; one back.
page:   ld (curbank),a      ; page bank A in at C000h (keeps DE, HL)
        or 10h              ; and the 48 BASIC ROM
        push bc
        ld bc,7FFDh
        out (c),a
        pop bc
        ret

farent:                     ; entry A of table HL (db bank, dw address):
        ld e,a              ; A = bank, HL = address
        ld d,0
        add hl,de
        add hl,de
        add hl,de
        ld a,(hl)
        inc hl
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ret

isr:    push af             ; IM2, every frame, whichever bank is in
        push hl
        ld hl,(frames)
        inc hl
        ld (frames),hl
        pop hl
        pop af
        ei
        reti

; ---- Z set if this is a 128K (bank 1 is separate RAM at C000h) ----
detect128:
        ld bc,7FFDh
        ld a,(0C000h)
        ld e,a
        ld a,11h
        out (c),a
        ld a,(0C000h)
        ld d,a
        ld a,e
        cpl
        ld (0C000h),a
        ld a,10h
        out (c),a
        ld a,(0C000h)
        cp e
        push af
        ld a,11h
        out (c),a
        ld a,d
        ld (0C000h),a
        ld a,10h
        out (c),a
        pop af
        ret

; ============================================================
;  The script interpreter. HL = script. Each handler takes its
;  arguments from (HL), leaves HL after them and jumps to run.
; ============================================================
NOPS    EQU 14

run:    ld a,(hl)
        inc hl
        cp NOPS
        jr nc,run_bad
        add a,a
        push hl
        ld hl,optab
        ld e,a
        ld d,0
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ex (sp),hl          ; HL = script again, handler on the stack
        ret
run_bad:
        ld a,2              ; a bad opcode: red border and stop
        out (254),a
        jr run_bad

optab:  dw op_end,op_cls,op_pic,op_text,op_type,op_wait
        dw op_pause,op_border,op_clrrows,op_jump,op_choice
        dw op_trial,op_load,op_portrait

op_end: ret

op_cls: ld a,(hl)           ; attr
        inc hl
        push hl
        call clsa
        pop hl
        jp run

op_pic: ld a,(hl)           ; db picture number (pictab: bank, ZX0 screen)
        inc hl
        push hl
        ld hl,pictab
        call farent
        ld d,a
        ld a,(curbank)
        push af
        ld a,d
        call page
        push hl
        ld hl,ATTR          ; hide the screen while it is unpacked;
        ld de,ATTR+1        ; the colours come last and show it at once
        ld bc,767
        ld (hl),0
        ldir
        pop hl
        ld de,4000h
        call dzx0_standard
        pop af              ; the script's bank back
        call page
        xor a
        ld (skip),a
        pop hl
        jp run

op_text:
        xor a
        jr op_t1
op_type:
        ld a,1
op_t1:  ld (typing),a
        call textat
        xor a
        ld (typing),a
        jp run

op_wait:                    ; db first text row: prompt, SPACE, clear the text
        ld a,(hl)
        inc hl
        push hl
        push af
        ld hl,prompt
        call textat
        call waitspace
        pop af
        ld b,a
        ld a,24
        sub b
        ld c,a
        ld a,b
        call clrrows
        xor a
        ld (skip),a
        pop hl
        jp run

op_pause:                   ; db frames (SPACE cuts it short)
        ld b,(hl)
        inc hl
opp1:   halt
        call spacedn
        jr c,opp2
        djnz opp1
opp2:   jp run

op_border:
        ld a,(hl)
        inc hl
        ld (border),a
        out (254),a
        jp run

op_clrrows:                 ; db first row, count
        ld a,(hl)
        inc hl
        ld c,(hl)
        inc hl
        push hl
        call clrrows
        pop hl
        jp run

op_jump:
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        jp run

op_choice:                  ; db n, then n x (db key, dw label)
        push hl
opc0:   halt                ; let go of every key first
        call getkey
        or a
        jr nz,opc0
opc1:   halt
        call getkey
        or a
        jr z,opc1
        pop hl
        push hl
        ld b,(hl)
        inc hl
opc2:   cp (hl)
        inc hl
        jr z,opc_go
        inc hl
        inc hl
        djnz opc2
        jr opc1             ; not one of ours: keep waiting
opc_go: ld e,(hl)
        inc hl
        ld d,(hl)
        pop hl
        ex de,hl
        jp run

op_trial:                   ; db chunk: the cross-examination (trial.asm),
        ld a,(hl)           ; then that chunk, as the trial's bank has
        push af             ; been paged in over the scripts'
        call trial
        pop af
        call loadchunk
        jp run

op_load:                    ; db chunk: unpack it and run it from the start
        ld a,(hl)
        call loadchunk
        jp run

op_portrait:                ; db portrait number, row, col
        ld a,(hl)
        inc hl
        ld b,(hl)
        inc hl
        ld c,(hl)
        inc hl
        push hl
        call portrait
        pop hl
        jp run

; ============================================================
;  Screen
; ============================================================
; ---- portrait A (porttab, ZX0) at character row B, column C ----
; Unpacked to PSCR (in the portrait's own bank, paged in for the
; drawing; the bank that was in goes back after): its width and height
; in cells (v0.9: each portrait has its own size), the pixels, the
; colours. Its colour cells are blacked out first, then the pixels, then
; the colours, so it appears at once. Colours go through attrbase, so a
; hidden (veiled) screen keeps it hidden too.
portrait:
        ld (p_rc),bc
        ld hl,porttab
        call farent
        ld d,a
        ld a,(curbank)
        ld (p_was),a
        ld a,d
        call page
        ld de,PSCR
        call dzx0_standard
        ld a,(PSCR)
        ld (p_w),a
        neg
        add a,32
        ld (p_skip),a       ; 32 - width: to the next row of colours
        ld a,(PSCR+1)
        ld (p_h),a
        ld bc,(p_rc)
        ld l,b              ; HL = its top left colour cell
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld b,0
        add hl,bc
        ld bc,(attrbase)
        add hl,bc
        push hl
        ld a,(p_h)          ; black out its colours
        ld b,a
pt1:    push bc
        ld a,(p_w)
        ld b,a
pt2:    ld (hl),0
        inc hl
        djnz pt2
        ld a,(p_skip)
        ld e,a
        ld d,0
        add hl,de
        pop bc
        djnz pt1
        ld a,(p_rc+1)       ; first pixel row = row * 8
        add a,a
        add a,a
        add a,a
        ld (p_y),a
        ld hl,PSCR+2
        ld a,(p_h)
        add a,a
        add a,a
        add a,a
        ld b,a
pt3:    push bc
        ld a,(p_y)          ; DE = screen address of pixel row A, column
        ld e,a
        and 0C0h
        rrca
        rrca
        rrca
        or 40h
        ld d,a
        ld a,e
        and 7
        or d
        ld d,a
        ld a,e
        and 38h
        rlca
        rlca
        ld e,a
        ld a,(p_rc)
        add a,e
        ld e,a
        ld a,(p_w)
        ld c,a
        ld b,0
        ldir
        ld a,(p_y)
        inc a
        ld (p_y),a
        pop bc
        djnz pt3
        pop de              ; HL = PSCR + its pixels: the colours
        ld a,(p_h)
        ld b,a
pt4:    push bc
        ld a,(p_w)
        ld c,a
        ld b,0
        ldir
        ex de,hl
        ld a,(p_skip)
        ld c,a
        add hl,bc
        ex de,hl
        pop bc
        djnz pt4
        ld a,(p_was)
        jp page

p_rc:   dw 0                ; col, row
p_y:    db 0
p_was:  db 0                ; the bank that was in
p_w:    db 0                ; its width and height in cells
p_h:    db 0
p_skip: db 0

clsa:                       ; clear the screen; every colour cell = A
        push af
        ld hl,4000h
        ld de,4001h
        ld bc,6143
        ld (hl),0
        ldir
        pop af
        ld hl,ATTR
        ld de,ATTR+1
        ld bc,767
        ld (hl),a
        ldir
        xor a
        ld (skip),a
        ret

clrrows:                    ; clear C character rows from row A (white on black)
        ld b,c
        inc b
        dec b
        ret z
crr1:   push bc
        push af
        ld b,a
        and 18h
        or 40h
        ld h,a
        ld a,b
        and 7
        rrca
        rrca
        rrca
        ld l,a
        ld c,8
crr2:   push hl
        ld b,32
crr3:   ld (hl),0
        inc l
        djnz crr3
        pop hl
        inc h
        dec c
        jr nz,crr2
        pop af
        push af
        ld l,a              ; colours: ATTR + row*32
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld de,ATTR
        add hl,de
        ld b,32
crr4:   ld (hl),07h
        inc hl
        djnz crr4
        pop af
        inc a
        pop bc
        djnz crr1
        ret

; ---- text in the game's own font (font.inc), FONTW pixels a char ----
textat:                     ; HL -> row, col, attr, chars, 0. HL after the 0
        ld a,(hl)
        ld (c_row),a
        inc hl
        ld a,(hl)
        ld (c_col),a
        inc hl
        ld a,(hl)
        ld (c_attr),a
        inc hl
textraw:                    ; c_row, c_col, c_attr set; HL -> chars, 0
        ld a,(c_col)
        add a,a
        add a,a
        add a,a
        add a,MARGIN        ; text starts a few pixels into the cell
        ld (t_x),a
        push hl
        ld a,MARGIN         ; A = margin + width in pixels
ta0:    ld c,(hl)
        inc hl
        inc c
        dec c
        jr z,ta0e
        add a,FONTW
        jr ta0
ta0e:   add a,7             ; cells = (width + 7) / 8
        rra
        srl a
        srl a
        jr z,ta0z
        ld b,a              ; clear and colour the cells first
ta0c:   call clearcell
        ld hl,c_col
        inc (hl)
        djnz ta0c
ta0z:   pop hl
ta1:    ld a,(hl)
        inc hl
        or a
        ret z
        push hl
        call putch
        pop hl
        ld a,(t_x)
        add a,FONTW
        ld (t_x),a
        ld a,(typing)
        or a
        call nz,typedelay
        jr ta1

typedelay:                  ; one letter's wait while typing (keeps HL)
        ld a,(skip)
        or a
        ret nz
        call spacedn        ; SPACE: the rest of the page at once
        jr nc,tdl1
        ld a,1
        ld (skip),a
        ret
tdl1:   ld a,(border)       ; a faint tick of the quill
        or 10h
        out (254),a
        ld b,10
tdl2:   djnz tdl2
        ld a,(border)
        out (254),a
        halt
        halt
        ret

clearcell:                  ; blank cell c_row,c_col in c_attr (keeps BC, HL)
        push bc
        push hl
        ld a,(c_row)
        ld b,a
        and 18h
        or 40h
        ld h,a
        ld a,b
        and 7
        rrca
        rrca
        rrca
        ld l,a
        ld a,(c_col)
        or l
        ld l,a
        ld b,8
ccl1:   ld (hl),0
        inc h
        djnz ccl1
        ld a,(c_row)
        ld l,a
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld a,(c_col)
        ld c,a
        ld b,0
        add hl,bc
        ld bc,(attrbase)    ; the screen, or trial.asm's hidden copy (veil)
        add hl,bc
        ld a,(c_attr)
        ld (hl),a
        pop hl
        pop bc
        ret

putch:                      ; draw char A at c_row, pixel t_x (ORed in)
        sub 32
        ld l,a
        ld h,0
        ld d,h
        ld e,l
        add hl,hl
        add hl,hl
        add hl,hl
        sbc hl,de           ; x7: font.inc keeps rows 1-7 (row 0 is blank)
        ld de,font
        add hl,de
        ex de,hl
        ld a,(c_row)
        ld b,a
        and 18h
        or 40h
        ld h,a
        ld a,b
        and 7
        rrca
        rrca
        rrca
        ld l,a
        ld a,(t_x)
        ld c,a
        rrca
        rrca
        rrca
        and 1Fh
        or l
        ld l,a
        ld a,c
        and 7
        ld c,a              ; C = shift within the byte
        inc h               ; start at pixel row 1
        ld b,7
pc1:    push bc
        ld a,(de)
        inc de
        push de
        ld d,a
        ld e,0
        inc c
        jr pc3
pc2:    srl d
        rr e
pc3:    dec c
        jr nz,pc2
        ld a,(hl)
        or d
        ld (hl),a
        inc l
        ld a,(hl)
        or e
        ld (hl),a
        dec l
        inc h
        pop de
        pop bc
        djnz pc1
        ret

; ============================================================
;  Keyboard
; ============================================================
getkey:                     ; A = ASCII of a pressed key, or 0
        ld hl,keytab
        ld bc,0FEFEh
gk1:    in a,(c)
        cpl
        and 1Fh
        jr nz,gk_found
        ld de,5
        add hl,de
        rlc b
        jr c,gk1
        xor a
        ret
gk_found:
        rrca
        jr c,gk2
        inc hl
        jr gk_found
gk2:    ld a,(hl)
        ret

keytab: db 0,"ZXCV"
        db "ASDFG"
        db "QWERT"
        db "12345"
        db "09876"
        db "POIUY"
        db 13,"LKJH"
        db " ",0,"MNB"

spacedn:                    ; carry set if SPACE is held
        ld a,7Fh
        in a,(0FEh)
        rra
        ccf
        ret

waitspace:                  ; let go of SPACE, then press it
ws1:    halt
        call spacedn
        jr c,ws1
ws2:    halt
        call spacedn
        jr nc,ws2
        ret

; ============================================================
;  Data
; ============================================================
msg48:  db 10,4,47h,"1711 needs a 128K Spectrum.",0
msg48b: db 12,4,07h,"(128, +2, +2A, +3 or Next)",0
msgtape: db 10,4,47h,"Tape loading error.",0
msgtapeb: db 12,4,07h,"Rewind a little and load again.",0
prompt: db 23,27,PROMPTC,"SPACE",0

c_row:  db 0
c_col:  db 0
c_attr: db 0
t_x:    db 0
typing: db 0
skip:   db 0
border: db 0
attrbase: dw ATTR
curbank: db 0
frames: dw 0

        INCLUDE "trial.asm"
        INCLUDE "dzx0_standard.asm"
        INCLUDE "font.inc"
        INCLUDE "banks.inc"         ; chunks, pictures, portraits: bank + address (build.py)
        INCLUDE "trialsym.inc"      ; the trial's labels, at TBUF in its bank (build.py)
END_OF_CODE:
