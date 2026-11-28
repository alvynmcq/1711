; ============================================================
;  The trial (stage 3, v0.9): a witness's cross-examination.
;  The words and tables come from trial.inc (scripts/trial.py),
;  read in place in TRIALBANK; this code draws them and keeps the
;  clock, the bench's patience and Lyle's notes.
;
;  The screen:
;    row 0       the witness (bright white); eight hour marks, cells 26-31
;    row 1       the time in words
;    rows 2-15   the portrait, 16 x 14, columns 8-23 (or the record)
;    row 16      a rule, "3 of 7" (the line)
;    rows 17-20  the testimony line (or what is said about it)
;    row 21      Ormsby's manner
;    row 22      keys
;    row 23      Ormsby's last remark
;  O / P a line (heard the first time: TR_CLINE minutes). SPACE presses
;  it (TR_CPRESS, once a line). ENTER opens the record over the
;  portrait: Q / A or 1-0 a fact, ENTER presents it, X back. A fact
;  that contradicts the line: HOLD, SIR! (TR_CHOLD), the witness
;  falters, answers, Ormsby answers, Lyle has it written. Anything
;  else: a rebuke, TR_CWRONG, and the bench loses TR_PWRONG; at 0
;  Lyle is silenced. X: let her stand down. At TR_END the bell.
;  Then Lyle's notes.
; ============================================================
TWHT    EQU 07h             ; the testimony
TBWHT   EQU 47h             ; Lyle's words, headings
TYEL    EQU 06h             ; the bench, the time
TBYEL   EQU 46h             ; the hour marks
TBRED   EQU 42h             ; HOLD, SIR! (red only for this and the verdict)
PROW    EQU 2               ; the portrait: rows 2-15, columns 8-23
PCOL    EQU 8
TROW    EQU 17              ; the testimony, rows 17-20
TROWS   EQU 4

trial:  ld a,TRIALBANK      ; the trial's text and tables, read in place
        call page           ; (op_trial's LOAD pages the scripts back)
        xor a
        ld (border),a
        out (254),a
        ld hl,0
        ld (tr_t),hl
        ld (tr_cur),a
        ld (tr_sil),a
        ld (tr_over),a
        ld (tr_nn),a
        ld (tr_reb),a
        ld (tr_spec),a
        ld (tr_sel),a
        ld (pr_mv),a
        ld a,TR_PAT0
        ld (tr_pat),a
        ld hl,tr_nflag
        ld b,16
ti1:    ld (hl),0
        inc hl
        djnz ti1
        ld b,0              ; each line: shown unless it is drawn out later
ti2:    ld a,b
        cp TR_NL
        jr nc,ti3
        push bc
        call lineaddr
        inc hl
        inc hl
        ld a,(hl)           ; flags: 1 = hidden
        xor 1
        and 1
        pop bc
        push af
        ld a,b
        call lsaddr
        pop af
        ld (hl),a
        inc b
        jr ti2
ti3:    ld hl,(tr_opening)
        ld (tr_rem),hl
        call tr_draw
        call hearcur
tl:     ld a,(tr_over)      ; the bell: she stands down
        or a
        jr nz,tl_bell
        call waitkey
        cp 'O'
        jr nz,tl1
        call prevline
        jr tl
tl1:    cp 'P'
        jr nz,tl2
        call nextline
        jr tl
tl2:    cp ' '
        jr nz,tl3
        call press
        jr tl
tl3:    cp 13
        jr nz,tl4
        call record
        jr tl
tl4:    cp 'X'
        jr nz,tl
        call standdown
        jr nc,tl
        ld hl,(tr_stand_down)
        jr tr_go
tl_bell:
        ld hl,(tr_bell)
tr_go:  push hl
        call clrtest
        pop hl
        ld b,TROW
        ld a,TYEL
        call typeblk
        call waitp
        jp notes

; ---- the whole screen (the line itself is shown by the caller) ----
tr_draw:
        xor a
        call clsa
        ld hl,tr_name
        ld bc,0*256+1
        ld a,TBWHT
        call strat
        call marks
        call drawtime
        call rule
        call manner
        call keysnow
        ld hl,(tr_rem)
        call remark
        jp drawport

drawport:
        ld a,TRIAL_PORT
        ld bc,PROW*256+PCOL
        jp portrait

keysnow:                    ; row 22: the keys (X shown at the last line),
        ld hl,keys_sil      ; or fewer once silenced
        ld a,(tr_sil)
        or a
        jr nz,keys
        ld a,(tr_cur)       ; a line shown after this one?
ks1:    inc a
        cp TR_NL
        jr nc,ks2
        push af
        call lsaddr
        bit 0,(hl)
        pop hl              ; (A back into H: only the count matters)
        ld a,h
        jr z,ks1
        ld hl,keys_main
        jr keys
ks2:    ld hl,keys_last
keys:   push hl             ; row 22: keys (a textat record)
        ld a,22
        ld c,1
        call clrrows
        pop hl
        jp textat

; ---- the lines ----
lineaddr:                   ; HL = line A's record (9 bytes)
        ld l,a
        ld h,0
        ld d,h
        ld e,l
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,de
        ld de,tr_lines
        add hl,de
        ret

lsaddr: ld l,a              ; HL = line A's state: bit 0 shown, 1 heard,
        ld h,0              ; 2 pressed
        ld de,tr_ls
        add hl,de
        ret

ldw:    ld a,(hl)           ; HL = the word at HL
        inc hl
        ld h,(hl)
        ld l,a
        ret

prevline:
        ld a,(tr_cur)
pl_1:   or a
        ret z
        dec a
        push af
        call lsaddr
        bit 0,(hl)
        jr nz,pl_2
        pop af
        jr pl_1
pl_2:   pop af
        ld (tr_cur),a
        call rule
        jp hearcur

nextline:
        ld a,(tr_cur)
nl_1:   inc a
        cp TR_NL
        ret nc
        push af
        call lsaddr
        bit 0,(hl)
        jr nz,nl_2
        pop af
        jr nl_1
nl_2:   pop af
        ld (tr_cur),a
        call rule
        jp hearcur

hearcur:                    ; the line: typed and timed the first time
        ld a,(tr_cur)
        call lsaddr
        bit 1,(hl)
        ld a,0
        jr nz,showline
        set 1,(hl)
        ld a,TR_CLINE
        call spend
        ld a,1
showline:                   ; the current line in rows 17-20, typed if A = 1
        push af
        call clrtest
        ld a,(tr_cur)
        call lineaddr
        call ldw
        pop af
        ld b,TROW
        or a
        ld a,TWHT
        jp nz,typeblk
        jp drawclause

clrtest:                    ; rows 17-20 blank
        ld a,TROW
        ld c,TROWS
        jp clrrows

; ---- SPACE: press the line ----
press:  ld a,(tr_sil)
        or a
        jp nz,silkey
        ld a,(tr_cur)
        call lsaddr
        bit 2,(hl)
        jr z,pr0
        ld hl,(tr_asked)    ; once a line
        jp setrem
pr0:    set 2,(hl)
        ld a,TR_CPRESS
        call spend
        ld a,(tr_cur)
        call lineaddr
        ld de,3
        add hl,de
        call ldw            ; its press, or 0: nothing more in it
        ld (pr_rec),hl
        ld a,h
        or l
        jr nz,pr1
        ld hl,tr_pnone
pr1:    push hl
        call clrtest
        pop hl
        push hl
        call ldw            ; Lyle asks
        ld b,TROW
        ld a,TBWHT
        call typeblk
        pop hl
        inc hl
        inc hl
        call ldw            ; she answers, under it
        ld a,TWHT
        call typeblk
        call waitp
        ld hl,(pr_rec)
        ld a,h
        or l
        jr z,pr_end
        ld de,4
        add hl,de
        ld a,(hl)           ; a line it draws out
        inc hl
        cp 0FFh
        jr z,pr2
        push hl
        ld (tr_cur),a
        call lsaddr
        set 0,(hl)
        pop hl
        ld a,1
        ld (pr_mv),a
pr2:    ld a,(hl)           ; a note for Lyle
        inc hl
        cp 0FFh
        jr z,pr_end
        ld e,(hl)           ; spectral
        push de
        call writenote
        pop de
        ld a,e
        or a
        jr z,pr_end
        ld hl,tr_spec
        inc (hl)
pr_end: ld hl,(tr_after_press)
        call setrem
        ld a,(pr_mv)
        or a
        ld a,0
        jp z,showline
        xor a
        ld (pr_mv),a
        call rule
        jp hearcur          ; the line it drew out, heard

silkey: ld hl,(tr_silent_key)
        jp setrem

; ---- Lyle's notes ----
writenote:                  ; note A: written, shown, SPACE
        ld (wn_i),a
        ld e,a
        ld d,0
        ld hl,tr_nflag
        add hl,de
        ld (hl),1
        ld a,(tr_nn)
        ld e,a
        inc a
        ld (tr_nn),a
        ld hl,tr_nord
        add hl,de
        ld a,(wn_i)
        ld (hl),a
        call clrtest
        ld hl,txt_written
        ld bc,TROW*256+1
        ld a,TBWHT
        call strat
        ld a,(wn_i)
        call noteblk
        ld b,TROW+1
        ld a,TWHT
        call typeblk
        jp waitp

noteblk:                    ; HL = note A's block
        add a,a
        ld l,a
        ld h,0
        ld de,tr_notes
        add hl,de
        jp ldw

; ---- ENTER: the record, over the portrait ----
record: ld a,(tr_sil)
        or a
        jp nz,silkey
        ld a,2
        ld c,14
        call clrrows
        ld hl,txt_record
        call textat
        ld b,0
rd1:    push bc
        ld a,b
        call factrow
        pop bc
        inc b
        ld a,b
        cp TR_NF
        jr c,rd1
        call sworn
        ld hl,keys_rec
        call keys
rk:     call waitkey
        cp 'X'
        jr z,rec_close
        cp 13
        jr nz,rk1
        call rec_close
        jp present
rk1:    cp 'Q'
        jr nz,rk2
        ld a,(tr_sel)
        or a
        jr z,rk
        dec a
        jr rk_set
rk2:    cp 'A'
        jr nz,rk3
        ld a,(tr_sel)
        inc a
        cp TR_NF
        jr nc,rk
        jr rk_set
rk3:    sub '0'             ; 1-9, 0 (the tenth)
        jr c,rk
        cp 10
        jr nc,rk
        dec a
        jp p,rk4
        ld a,9
rk4:    cp TR_NF
        jr nc,rk
rk_set: ld b,a              ; the old row plain, the new one lit
        ld a,(tr_sel)
        ld c,a
        ld a,b
        ld (tr_sel),a
        ld a,c
        call factrow
        ld a,(tr_sel)
        call factrow
        call sworn
        jr rk

rec_close:
        ld a,2
        ld c,14
        call clrrows
        call drawport
        jp keysnow

factrow:                    ; fact A in row 4+A: "> 1 fact", lit if chosen
        ld (fr_i),a
        ld hl,fr_buf
        ld c,a
        ld a,(tr_sel)
        cp c
        ld a,' '
        jr nz,fr1
        ld a,'>'
fr1:    ld (hl),a
        inc hl
        ld (hl),' '
        inc hl
        ld a,c
        inc a
        cp 10
        jr c,fr2
        xor a
fr2:    add a,'0'
        ld (hl),a
        inc hl
        ld (hl),' '
        inc hl
        push hl
        ld a,c
        add a,a
        add a,a
        ld l,a
        ld h,0
        ld de,tr_facts
        add hl,de
        call ldw
        pop de
fr3:    ld a,(hl)           ; the fact after it
        ld (de),a
        inc hl
        inc de
        or a
        jr nz,fr3
        ld a,(fr_i)
        add a,4
        ld b,a
        ld c,1
        ld hl,tr_sel
        ld a,(fr_i)
        cp (hl)
        ld a,TYEL
        jr nz,fr4
        ld a,TBWHT
fr4:    ld hl,fr_buf
        jp strat

sworn:  ld a,15             ; row 15: who swore the chosen fact, and when
        ld c,1
        call clrrows
        ld a,(tr_sel)
        add a,a
        add a,a
        ld l,a
        ld h,0
        ld de,tr_facts+2
        add hl,de
        call ldw
        ld bc,15*256+3
        ld a,TWHT
        jp strat

; ---- presenting a fact at the line ----
present:
        ld a,(tr_cur)
        call lineaddr
        ld de,5
        add hl,de
        call ldw            ; the facts that contradict it
        ld a,h
        or l
        jr z,wrong
        ld b,(hl)
        inc hl
ps1:    ld a,(tr_sel)
        cp (hl)
        jr z,ps_hit
        ld de,8             ; db fact, dw q, a, o, db note
        add hl,de
        djnz ps1
        jr wrong
ps_hit: inc hl
        ld (hd_rec),hl
        ld de,6
        add hl,de
        ld a,(hl)
        ld (hd_note),a
        ld e,a
        ld d,0
        ld hl,tr_nflag
        add hl,de
        ld a,(hl)
        or a
        jp z,hold
        ld hl,(tr_raised)   ; already had from her
        jp setrem

wrong:  ld a,(tr_cur)       ; Ormsby: its own words, or the next rebuke
        call lineaddr
        ld de,7
        add hl,de
        call ldw
        ld a,h
        or l
        jr z,wr_g
        ld b,(hl)
        inc hl
wr1:    ld a,(tr_sel)
        cp (hl)
        inc hl
        jr z,wr_c
        inc hl
        inc hl
        djnz wr1
wr_g:   ld a,(tr_reb)
        ld c,a
        inc a
        cp TR_NREB
        jr c,wr2
        xor a
wr2:    ld (tr_reb),a
        ld a,c
        add a,a
        ld l,a
        ld h,0
        ld de,tr_rebukes
        add hl,de
wr_c:   call ldw
        push hl
        ld hl,ay_low
        call aysnd
        call clrtest
        pop hl
        ld b,TROW
        ld a,TYEL
        call typeblk
        call waitp
        ld a,(tr_pat)
        sub TR_PWRONG
        jr nc,wr3
        xor a
wr3:    ld (tr_pat),a
        call manner
        ld a,TR_CWRONG
        call spend
        ld a,(tr_pat)
        or a
        jr nz,wr4
        ld a,1              ; silenced, for the rest of the day
        ld (tr_sil),a
        call clrtest
        ld hl,(tr_silenced)
        ld b,TROW
        ld a,TYEL
        call typeblk
        call waitp
        call manner
        call keysnow
wr4:    ld hl,(tr_after_wrong)
        call setrem
        xor a
        jp showline

; ---- HOLD, SIR! ----
hold:   call flash
        ld hl,ay_hold
        call aysnd
        call clrtest
        ld hl,ATTR+TROW*32  ; two rows in bright red
        ld b,64
hd1:    ld (hl),TBRED
        inc hl
        djnz hd1
        ld a,TROW
        ld (bs_row),a
        ld a,83             ; "HOLD, SIR!", 9 pixels a letter, centred
        ld (t_x),a
        ld hl,txt_hold
hd2:    ld a,(hl)
        or a
        jr z,hd3
        inc hl
        push hl
        call bigch
        pop hl
        ld a,(t_x)
        add a,9
        ld (t_x),a
        jr hd2
hd3:    ld hl,(hd_rec)      ; Lyle's question
        call ldw
        ld b,TROW+2
        ld a,TBWHT
        call typeblk
        call waitp
        xor a               ; she falters
        call falter
        call clrtest
        ld hl,(hd_rec)
        inc hl
        inc hl
        call ldw
        ld b,TROW
        ld a,TWHT
        call typeblk
        call waitp
        call clrtest        ; Ormsby, with the reasoning of the day
        ld hl,(hd_rec)
        ld de,4
        add hl,de
        call ldw
        ld b,TROW
        ld a,TYEL
        call typeblk
        call waitp
        ld a,(hd_note)
        call writenote
        ld a,8              ; she is herself again
        call falter
        ld a,TR_CHOLD
        call spend
        ld hl,(tr_after_hold)
        call setrem
        xor a
        jp showline

flash:  ld b,6              ; the border, red and white
fl1:    halt
        ld a,b
        and 1
        ld a,2
        jr nz,fl2
        ld a,7
fl2:    out (254),a
        djnz fl1
        ld a,(border)
        out (254),a
        ret

falter: ld (fa_o),a         ; A = 0: the faltering cells in; 8: back
        ld hl,TRIAL_FALTER
        ld b,(hl)
        inc hl
fa1:    push bc
        ld a,(hl)           ; the cell's row and column in the portrait
        inc hl
        ld c,(hl)
        inc hl
        push hl
        add a,PROW
        add a,a
        add a,a
        add a,a
        call pxaddr
        ld a,c
        add a,PCOL
        or l
        ld l,a
        ex de,hl
        pop hl
        push hl
        ld a,(fa_o)
        ld c,a
        ld b,0
        add hl,bc
        ld b,8
fa2:    ld a,(hl)
        ld (de),a
        inc hl
        inc d
        djnz fa2
        pop hl
        ld de,16
        add hl,de
        pop bc
        djnz fa1
        ret

; ---- X: let her stand down (carry set: yes) ----
standdown:
        ld a,23
        ld c,1
        call clrrows
        ld hl,txt_sd
        call textat
sd1:    call waitkey
        cp 'N'
        jr z,sd2
        cp 'Y'
        jr nz,sd1
        scf
        ret
sd2:    ld hl,(tr_rem)
        call remark
        or a
        ret

; ---- the clock ----
spend:  push af             ; A minutes pass; the bell on the hour
        ld hl,(tr_t)
        call hours
        ld (sp_h),a
        pop af
        ld hl,(tr_t)
        ld e,a
        ld d,0
        add hl,de
        ld (tr_t),hl
        call hours
        ld hl,sp_h
        cp (hl)
        jr z,sp1
        ld hl,ay_bell
        call aysnd
        call marks
sp1:    call drawtime
        ld hl,(tr_t)
        ld de,TR_END
        or a
        sbc hl,de
        ret c
        ld a,1
        ld (tr_over),a
        ret

hours:  ld c,60             ; A = (tr_t in HL) / 60
divc:   ld b,0              ; A = HL / C (the quotient under 256)
        ld d,b
        ld e,c
        xor a
dv1:    or a
        sbc hl,de
        jr c,dv2
        inc a
        jr dv1
dv2:    add hl,de
        ret

drawtime:                   ; row 1: the time in words
        ld a,1
        ld c,1
        call clrrows
        ld hl,(tr_t)
        ld c,5
        call divc
        add a,a
        ld l,a
        ld h,0
        ld de,tr_time
        add hl,de
        call ldw
        ld bc,1*256+1
        ld a,TYEL
        jp strat

marks:                      ; row 0, cells 26-31: eight candles, one burnt
        ld b,8              ; down to the dish for each hour gone
        ld h,40h
mk1:    push bc
        ld l,26
        ld b,6
mk2:    ld (hl),0
        inc l
        djnz mk2
        inc h
        pop bc
        djnz mk1
        ld hl,ATTR+26
        ld b,6
mk3:    ld (hl),TBYEL
        inc hl
        djnz mk3
        ld hl,(tr_t)
        call hours
        ld (mk_s),a
        xor a
        ld (mk_i),a
mk4:    ld a,(mk_i)         ; x = 210 + 5i
        ld b,a
        add a,a
        add a,a
        add a,b
        add a,210
        ld (mk_x),a
        ld hl,mk_s
        ld a,(mk_i)
        cp (hl)
        jr c,mk_out
        ld e,3              ; lit: wax, pixel rows 3-7, two wide; a flame
mk5:    call mk_pair
        inc e
        ld a,e
        cp 8
        jr c,mk5
        ld a,(mk_x)
        ld d,a
        ld e,1
        call plot
        ld a,(mk_x)
        inc a
        ld d,a
        ld e,2
        call plot
        jr mk6
mk_out: ld e,7              ; out: the dish only
        call mk_pair
mk6:    ld hl,mk_i
        inc (hl)
        ld a,(hl)
        cp 8
        jr c,mk4
        ret

mk_pair:                    ; two pixels at mk_x, row E (keeps E)
        push de
        ld a,(mk_x)
        ld d,a
        call plot
        pop de
        push de
        ld a,(mk_x)
        inc a
        ld d,a
        call plot
        pop de
        ret

plot:   ld a,e              ; set the pixel at x D, y E
        call pxaddr
        ld a,d
        rrca
        rrca
        rrca
        and 1Fh
        or l
        ld l,a
        ld a,d
        and 7
        inc a
        ld b,a
        ld a,1
pt_r:   rrca
        djnz pt_r
        or (hl)
        ld (hl),a
        ret

; ---- row 16: a rule, and which line of how many ----
rule:   ld a,16
        ld c,1
        call clrrows
        ld a,16*8+4
        call pxaddr
        inc l
        ld b,30
rl1:    ld (hl),0AAh
        inc l
        djnz rl1
        ld hl,ATTR+16*32
        ld b,32
rl2:    ld (hl),TYEL
        inc hl
        djnz rl2
        ld bc,0             ; B = this line's place, C = lines shown
        ld e,0
rl3:    ld a,e
        cp TR_NL
        jr nc,rl5
        push bc
        push de
        call lsaddr
        bit 0,(hl)
        pop de
        pop bc
        jr z,rl4
        inc c
        ld a,(tr_cur)
        cp e
        jr c,rl4
        inc b
rl4:    inc e
        jr rl3
rl5:    ld hl,rl_buf
        ld a,b
        call num
        ld de,txt_of
rl6:    ld a,(de)
        ld (hl),a
        inc de
        inc hl
        or a
        jr nz,rl6
        dec hl
        ld a,c
        call num
        ld (hl),0
        ld hl,rl_buf
        ld bc,16*256+13
        ld a,TYEL
        call strat
        jp keysnow

num:    cp 10               ; A (0-99) as digits at HL (HL after them)
        jr c,nm1
        ld b,'0'-1
nm0:    inc b
        sub 10
        jr nc,nm0
        add a,10
        ld (hl),b
        inc hl
nm1:    add a,'0'
        ld (hl),a
        inc hl
        ret

; ---- rows 21 and 23 ----
manner: ld a,21             ; Ormsby's manner, by the bench's patience
        ld c,1
        call clrrows
        ld a,(tr_sil)
        or a
        ld hl,(tr_silent_row)
        jr nz,mn1
        call band
        add a,a
        ld l,a
        ld h,0
        ld de,tr_manner
        add hl,de
        call ldw
mn1:    ld bc,21*256+1
        ld a,TYEL
        jp strat

band:   ld a,(tr_pat)       ; A = 0 (10-12), 1 (6-9), 2 (3-5), 3 (0-2)
        ld b,0
        cp 10
        jr nc,bd_e
        inc b
        cp 6
        jr nc,bd_e
        inc b
        cp 3
        jr nc,bd_e
        inc b
bd_e:   ld a,b
        ret

setrem: ld (tr_rem),hl      ; Ormsby's last remark, row 23
remark: push hl
        ld a,23
        ld c,1
        call clrrows
        pop hl
        ld bc,23*256+1
        ld a,TYEL
        jp strat

waitp:  ld a,23             ; the SPACE prompt over row 23, then the
        ld c,1              ; remark back
        call clrrows
        ld hl,prompt
        call textat
        call waitspace
        ld hl,(tr_rem)
        jp remark

; ---- Lyle's notes, at the end ----
notes:  xor a
        call clsa
        ld hl,nt_head
        call textlist
        ld b,4
        ld a,(tr_nn)
        or a
        jr nz,nt1
        ld hl,txt_nonote
        ld c,1
        ld a,TYEL
        call strat
        jr nt3
nt1:    xor a
        ld (nt_i),a
nt2:    ld a,(nt_i)
        ld e,a
        ld d,0
        ld hl,tr_nord
        add hl,de
        ld a,(hl)
        push bc
        call noteblk
        pop bc
        ld a,TWHT
        call drawclause
        inc b
        ld hl,nt_i
        inc (hl)
        ld a,(tr_nn)
        cp (hl)
        jr nz,nt2
nt3:    ld hl,prompt
        call textat
        jp waitspace

; ---- small helpers (from v0.8's night.asm) ----
typeblk:                    ; type block HL at row B in A (B after: the row below)
        push af
        push bc
        push hl
        call release        ; the key that got us here mustn't skip it
        xor a
        ld (skip),a
        inc a
        ld (typing),a
        pop hl
        pop bc
        pop af
        call drawclause
        xor a
        ld (typing),a
        ret

veil:                       ; blank the screen; text drawn now stays hidden
        xor a
        call clsa
        ld hl,abuf
        ld de,abuf+1
        ld bc,767
        ld (hl),07h
        ldir
        ld hl,abuf
        ld (attrbase),hl
        ret

unveil:                     ; show everything drawn since veil, at once (keeps BC)
        push bc
        ld hl,abuf
        ld de,ATTR
        ld bc,768
        ldir
        ld hl,ATTR
        ld (attrbase),hl
        pop bc
        ret

drawclause:                 ; HL = block (db lines, strings), row B, attr A
        ld (c_attr),a       ; B after = the row below it; C kept
        ld a,c
        ld (dc_c),a
        ld c,(hl)
        inc hl
dcl1:   ld a,b
        ld (c_row),a
        ld a,1
        ld (c_col),a
        push bc
        call textraw
        pop bc
        inc b
        dec c
        jr nz,dcl1
        ld a,(dc_c)
        ld c,a
        ret

strat:  ld (c_attr),a       ; string HL at row B, column C, attr A (keeps BC)
        ld a,b
        ld (c_row),a
        ld a,c
        ld (c_col),a
        push bc
        call textraw
        pop bc
        ret

textlist:                   ; textat records until 0FFh
        ld a,(hl)
        cp 0FFh
        ret z
        call textat
        jr textlist

waitkey:                    ; let go of every key, then A = the next one
        call release
wk2:    halt
        call getkey
        or a
        jr z,wk2
        ret

release:                    ; wait until no key is held
        halt
        call getkey
        or a
        jr nz,release
        ret

bigch:  sub 32              ; char A at t_x, rows bs_row-bs_row+1, doubled
        ld l,a
        ld h,0
        ld d,h
        ld e,l
        add hl,hl
        add hl,hl
        add hl,hl
        sbc hl,de           ; x7: font.inc keeps glyph rows 1-7
        ld de,font
        add hl,de
        ld (bc_g),hl
        ld a,(bs_row)
        add a,a
        add a,a
        add a,a
        add a,2
        ld (bc_y),a
        ld b,7
bc1:    push bc
        ld hl,(bc_g)
        ld a,(hl)
        inc hl
        ld (bc_g),hl
        ld d,a
        ld e,0
        ld a,(t_x)
        and 7
        jr z,bc3
        ld b,a
bc2:    srl d
        rr e
        djnz bc2
bc3:    ld a,(bc_y)
        call bc_put
        ld a,(bc_y)
        inc a
        call bc_put
        ld a,(bc_y)
        add a,2
        ld (bc_y),a
        pop bc
        djnz bc1
        ret

bc_put: call pxaddr         ; OR D, E into pixel row A at t_x
        ld a,(t_x)
        rrca
        rrca
        rrca
        and 1Fh
        or l
        ld l,a
        ld a,(hl)
        or d
        ld (hl),a
        inc l
        ld a,(hl)
        or e
        ld (hl),a
        ret

pxaddr: ld l,a              ; HL = the screen address of pixel row A, column 0
        and 0C0h
        rrca
        rrca
        rrca
        or 40h
        ld h,a
        ld a,l
        and 7
        or h
        ld h,a
        ld a,l
        and 38h
        rlca
        rlca
        ld l,a
        ret

aysnd:  ld a,(hl)           ; AY: register writes, no player (reg, value ..., 0FFh)
        cp 0FFh
        ret z
        inc hl
        ld bc,0FFFDh
        out (c),a
        ld a,(hl)
        inc hl
        ld b,0BFh
        out (c),a
        jr aysnd

; ---- text ----
keys_main:  db 22,1,TWHT,"O P lines   SPACE press   ENTER record",0
keys_last:  db 22,1,TWHT,"O back  SPACE press  ENTER record  X end",0
keys_sil:   db 22,1,TWHT,"O P  lines          X  let her go",0
keys_rec:   db 22,1,TWHT,"Q A  a fact   ENTER  present   X  back",0
txt_record: db 3,1,TBWHT,"THE COURT RECORD",0
txt_sd:     db 23,1,TBWHT,"Let her stand down?  Y  N",0
txt_hold:   db "HOLD, SIR!",0
txt_written: db "Let it be written:",0
txt_of:     db " of ",0
txt_nonote: db "Nothing was written.",0
nt_head:    db 1,1,TBYEL,"JUSTICE LYLE'S NOTES",0
            db 2,1,TWHT,"Margaret Lowry, 31st March 1711",0
            db 0FFh

ay_bell:    db 0,0E0h,1,0,7,3Eh,8,10h,11,0,12,40h,13,0,0FFh
ay_hold:    db 0,70h,1,0,7,3Eh,8,10h,11,0,12,28h,13,0,0FFh
ay_low:     db 0,0,1,3,7,3Eh,8,10h,11,0,12,10h,13,0,0FFh

; ---- state ----
tr_t:       dw 0            ; minutes since the court sat
tr_pat:     db TR_PAT0      ; the bench's patience, 0-12
tr_sil:     db 0            ; Lyle silenced
tr_over:    db 0            ; the bell has rung for the end
tr_cur:     db 0            ; the line
tr_sel:     db 0            ; the fact chosen in the record
tr_reb:     db 0            ; the next rebuke
tr_nn:      db 0            ; notes written
tr_spec:    db 0            ; of them, what only Isobel saw
tr_rem:     dw 0            ; Ormsby's last remark
tr_ls:      ds 16           ; per line: shown, heard, pressed
tr_nflag:   ds 16           ; per note: written
tr_nord:    ds 16           ; the notes, in the order written
pr_rec:     dw 0
pr_mv:      db 0
hd_rec:     dw 0
hd_note:    db 0
wn_i:       db 0
fr_i:       db 0
fr_buf:     ds 42
rl_buf:     ds 10
fa_o:       db 0
sp_h:       db 0
mk_s:       db 0
mk_i:       db 0
mk_x:       db 0
nt_i:       db 0
dc_c:       db 0
bs_row:     db 0
bc_g:       dw 0
bc_y:       db 0

abuf:                       ; colours of a screen being drawn (veil); the
        INCLUDE "boot.asm"  ; boot stub sits here: it runs once, before
        ds 768-($-abuf)     ; abuf is first used
