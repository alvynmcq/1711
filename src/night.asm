; ============================================================
;  The night's screens: the hub, the statement reader, compare,
;  the clerk's book. The words and the tables come from night.inc
;  (scripts/night.py); this code only draws them and keeps the
;  clerk's marks and what he has written down.
;
;  Statement reader keys:
;    Q / A   up / down a line        O / P   page back / on
;    M       mark or unmark a line   C       compare two marked lines
;    B       the clerk's book        X       back to the statements
;
;  The candle (v0.5): one a night (NIGHT_CANDLE units). C burns 1,
;  writing a finding out burns 2 more; at 0 nothing more can be
;  compared. Drawn in the top right corner, a pixel of wax a unit.
;
;  Parade (K on the hub, once a night): 1-3 change how the accused is
;  brought, SPACE sends for her, then the scene, then what goes in the
;  book: the fit always (the Mayor's words), each other line Y or N.
; ============================================================
TXT     EQU 06h             ; yellow: statement text
SEL     EQU 47h             ; bright white: the line the clerk is on
MARKA   EQU 42h             ; bright red: the clerk's mark in the margin
ROW0    EQU 3               ; first row of statement text

night:  ld hl,nightz         ; unpack the night's text and tables (ZX0)
        ld de,NBUF
        call dzx0_standard
        xor a               ; a fresh night: no marks, nothing found
        ld (mk_n),a
        ld (par_done),a
        ld (par_wr),a
        ld a,NIGHT_CANDLE
        ld (cdl),a
        xor a
        ld hl,night_fflag
        ld b,NIGHT_NF
nt0:    ld (hl),a
        inc hl
        djnz nt0
hub:    call drawhub
hub_k:  call waitkey
        cp 'X'
        jr nz,hub_0
        ld hl,msg_endq      ; X: ask before the night is over
        call status
hub_x:  call waitkey
        cp 'Y'
        ret z
        cp 'N'
        jr nz,hub_x
        ld a,20
        ld c,2
        call clrrows
        jr hub_k
hub_0:  cp 'B'
        jr nz,hub_1
        call book
        jr hub
hub_1:  cp 'K'
        jr nz,hub_2
        ld a,(par_done)
        or a
        jr nz,hub_1b
        call parade
        jr hub
hub_1b: ld hl,msg_brought
        call status
        jr hub_k
hub_2:  sub '1'
        jr c,hub_k
        ld hl,night_nst
        cp (hl)
        jr nc,hub_k
        ld (cur_st),a
        call reader
        jr hub

drawhub:
        call veil
        ld hl,night_hub
        call textlist
        call unveil
        call candle
        ld a,(mk_n)         ; a mark beside each statement with a marked line
        or a
        ret z
        ld b,a
        ld hl,mk_s
dh1:    push bc
        push hl
        ld a,(hl)
        add a,HUBROW
        ld b,a
        ld a,'*'
        call drawmark
        pop hl
        pop bc
        inc hl
        djnz dh1
        ret

; ---- the statement reader ----
reader: xor a
        ld (cur_pg),a
        call pg_set
        ld a,(pg_first)
        ld (cur_cl),a
rd_redraw:
        call drawpage
rd_key: call waitkey
        cp 'Q'
        jp z,rd_up
        cp 'A'
        jp z,rd_down
        cp 'O'
        jp z,rd_prev
        cp 'P'
        jp z,rd_next
        cp 'M'
        jp z,rd_mark
        cp 'C'
        jp z,rd_comp
        cp 'B'
        jp z,rd_book
        cp 'X'
        ret z
        jr rd_key

rd_up:  ld a,(pg_first)
        ld b,a
        ld a,(cur_cl)
        cp b
        jr z,rd_up2
        call hl_off
        ld hl,cur_cl
        dec (hl)
        call hl_on
        jr rd_key
rd_up2: ld a,(cur_pg)       ; top of the page: back a page, to its last line
        or a
        jr z,rd_key
        dec a
        ld (cur_pg),a
        call pg_set
        call pg_last
        ld (cur_cl),a
        jp rd_redraw

rd_down:
        call pg_last
        ld b,a
        ld a,(cur_cl)
        cp b
        jr z,rd_next
        call hl_off
        ld hl,cur_cl
        inc (hl)
        call hl_on
        jp rd_key

rd_next:                    ; on a page, if there is one, to its first line
        call st_npg
        ld b,a
        ld a,(cur_pg)
        inc a
        cp b
        jp nc,rd_key
        ld (cur_pg),a
        jr rd_newpg
rd_prev:
        ld a,(cur_pg)
        or a
        jp z,rd_key
        dec a
        ld (cur_pg),a
rd_newpg:
        call pg_set
        ld a,(pg_first)
        ld (cur_cl),a
        jp rd_redraw

rd_mark:
        call findmark
        jr nz,rm_add
        or a                ; take off mark A; mark 1 moves down to 0
        jr nz,rm_r1
        ld a,(mk_s+1)
        ld (mk_s),a
        ld a,(mk_c+1)
        ld (mk_c),a
rm_r1:  ld hl,mk_n
        dec (hl)
        ld a,(cur_cl)
        call markrow
        ld a,' '
        call drawmark
        ld hl,msg_unmark
        call status
        call ckeys
        jp rd_key
rm_add: ld a,(mk_n)
        cp 2
        jr c,rm_a2
        ld hl,msg_two
        call status
        jp rd_key
rm_a2:  ld e,a
        ld d,0
        ld hl,mk_s
        add hl,de
        ld a,(cur_st)
        ld (hl),a
        ld hl,mk_c
        add hl,de
        ld a,(cur_cl)
        ld (hl),a
        ld hl,mk_n
        inc (hl)
        ld a,(cur_cl)
        call markrow
        ld a,'*'
        call drawmark
        ld a,(mk_n)
        cp 2
        ld hl,msg_mark1
        jr nz,rm_a3
        ld hl,msg_mark2
rm_a3:  call status
        call ckeys
        jp rd_key

ckeys:                      ; "C  compare" in the key help: flashing bright
        ld a,(mk_n)         ; white once two lines are marked (v0.6: the
        cp 2                ; play-test missed the message) and there is
        ld a,05h            ; candle left to compare by; else as drawn
        jr nz,ck1
        ld a,(cdl)
        or a
        ld a,05h
        jr z,ck1
        ld a,0C7h
ck1:    ld hl,(attrbase)
        ld de,23*32+1       ; row 23, cells 1-8
        add hl,de
        ld b,8
ck2:    ld (hl),a
        inc hl
        djnz ck2
        ret

rd_comp:
        ld a,(mk_n)
        cp 2
        jr z,rc_1
        ld hl,msg_need2
        call status
        jp rd_key
rc_1:   ld a,(cdl)          ; the candle: none left, no compare
        or a
        jr nz,rc_2
        ld hl,msg_dark
        call status
        jp rd_key
rc_2:   dec a
        ld (cdl),a
        call compare
        jp rd_redraw

rd_book:
        call book
        jp rd_redraw

; ---- page bookkeeping ----
pg_set:                     ; pg_first, pg_cnt for cur_st, cur_pg
        ld a,(cur_st)
        call getst
        ld de,8
        add hl,de
        ld a,(cur_pg)
        add a,a
        ld e,a
        ld d,0
        add hl,de
        ld a,(hl)
        ld (pg_first),a
        inc hl
        ld a,(hl)
        ld (pg_cnt),a
        ret

pg_last:                    ; A = last clause on the page
        ld a,(pg_first)
        ld b,a
        ld a,(pg_cnt)
        add a,b
        dec a
        ret

st_npg: ld a,(cur_st)       ; A = pages in this statement
        call getst
        ld de,5
        add hl,de
        ld a,(hl)
        ret

getst:  ld l,a              ; HL = statement record A
        ld h,0
        add hl,hl
        ld de,night_st
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

getclause:                  ; HL = clause C of statement A
        push bc
        call getst
        ld de,6
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        pop bc
        ld b,0
        add hl,bc
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

drawpage:
        call veil
        ld a,(cur_st)
        call getst
        push hl
        ld a,(hl)           ; who
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,0001h
        ld a,SEL
        call strat
        pop hl
        push hl
        inc hl
        inc hl
        ld a,(hl)           ; sworn
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,0101h
        ld a,07h
        call strat
        pop hl
        ld de,5
        add hl,de
        ld a,(hl)           ; pages
        cp 2
        jr c,dp_0
        add a,'0'
        ld (pg_d2),a
        ld a,(cur_pg)
        add a,'1'
        ld (pg_d1),a
        ld hl,pg_s
        ld bc,0116h         ; (col 22: col 31 of rows 0-2 is the candle)
        ld a,05h
        call strat
dp_0:   ld hl,rd_keys
        call textlist
        call ckeys
        xor a
        ld (dp_i),a
        ld a,ROW0
        ld (dp_r),a
dp_l:   ld a,(dp_i)
        ld hl,pg_cnt
        cp (hl)
        jr nc,dp_e
        ld e,a
        ld d,0
        ld hl,pg_row
        add hl,de
        ld a,(dp_r)
        ld (hl),a
        push de
        ld a,(pg_first)
        add a,e
        ld c,a
        ld a,(cur_st)
        call getclause
        pop de
        ld a,(hl)           ; its lines
        push hl
        ld hl,pg_len
        add hl,de
        ld (hl),a
        pop hl
        ld a,(dp_r)
        ld b,a
        ld a,TXT
        call drawclause
        ld a,b
        ld (dp_r),a
        ld hl,dp_i
        inc (hl)
        jr dp_l
dp_e:   call unveil
        call candle
        call hl_on
        ld a,(mk_n)         ; the marks on this page
        or a
        ret z
        ld b,a
        ld hl,mk_s
dm1:    push bc
        push hl
        ld a,(cur_st)
        cp (hl)
        jr nz,dm2
        inc hl
        inc hl
        ld a,(hl)
        call markrow
        jr nc,dm2
        ld a,'*'
        call drawmark
dm2:    pop hl
        pop bc
        inc hl
        djnz dm1
        ret

markrow:                    ; A = clause: carry and B = its row if on this page
        ld hl,pg_first
        sub (hl)
        ccf
        ret nc
        ld hl,pg_cnt
        cp (hl)
        ret nc
        ld e,a
        ld d,0
        ld hl,pg_row
        add hl,de
        ld b,(hl)
        scf
        ret

hl_off: ld a,TXT            ; colour the current line's rows
        jr hl_set
hl_on:  ld a,SEL
hl_set: push af
        ld a,(pg_first)
        ld b,a
        ld a,(cur_cl)
        sub b
        ld e,a
        ld d,0
        ld hl,pg_row
        add hl,de
        ld b,(hl)
        ld hl,pg_len
        add hl,de
        ld c,(hl)
        pop af

setattr:                    ; colour C rows from row B, columns 1-31, with A
        push af
        ld l,b
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld de,ATTR+1
        add hl,de
        pop af
sa1:    ld b,31
sa2:    ld (hl),a
        inc hl
        djnz sa2
        inc hl              ; past column 0 of the next row
        dec c
        jr nz,sa1
        ret

findmark:                   ; Z and A = which mark, if the current line is marked
        ld a,(mk_n)
        or a
        jr z,fm_no
        ld b,a
        ld c,0
fm1:    ld e,c
        ld d,0
        ld hl,mk_s
        add hl,de
        ld a,(cur_st)
        cp (hl)
        jr nz,fm2
        ld hl,mk_c
        add hl,de
        ld a,(cur_cl)
        cp (hl)
        jr nz,fm2
        ld a,c
        cp a
        ret
fm2:    inc c
        djnz fm1
fm_no:  or 1
        ret

; ---- compare the two marked lines ----
compare:
        ld a,(mk_s)         ; put them in order: the table keeps them so
        ld b,a
        ld a,(mk_c)
        ld c,a
        ld a,(mk_s+1)
        ld d,a
        ld a,(mk_c+1)
        ld e,a
        ld a,d
        cp b
        jr c,cm_sw
        jr nz,cm_ok
        ld a,e
        cp c
        jr nc,cm_ok
cm_sw:  push bc
        push de
        pop bc
        pop de
cm_ok:  ld a,b
        ld (cm_s0),a
        ld a,c
        ld (cm_c0),a
        ld a,d
        ld (cm_s1),a
        ld a,e
        ld (cm_c1),a
        ld hl,night_pairs   ; look the pair up
        ld a,(hl)
        inc hl
        or a
        jr z,cm_none
        ld b,a
cm_fl:  push bc
        ld a,(cm_s0)
        cp (hl)
        jr nz,cm_n
        inc hl
        ld a,(cm_c0)
        cp (hl)
        jr nz,cm_n1
        inc hl
        ld a,(cm_s1)
        cp (hl)
        jr nz,cm_n2
        inc hl
        ld a,(cm_c1)
        cp (hl)
        jr nz,cm_n3
        inc hl
        ld a,(hl)
        pop bc
        jr cm_fnd
cm_n:   inc hl
cm_n1:  inc hl
cm_n2:  inc hl
cm_n3:  inc hl
        inc hl
        pop bc
        djnz cm_fl
cm_none:
        ld a,0FFh
cm_fnd: ld (cm_f),a
        xor a               ; the marks are used up
        ld (mk_n),a

        call veil
        ld hl,cm_title
        call textlist
        ld b,2
        ld a,(cm_c0)
        ld c,a
        ld a,(cm_s0)
        call cm_side
        ld a,(cm_c1)
        ld c,a
        ld a,(cm_s1)
        call cm_side
        ld a,(cm_f)
        cp 0FFh
        jr nz,cm_yes
        ld hl,txt_nobear
        ld a,07h
        call drawclause
        call unveil
        call candle
        jp cm_space

cm_yes: call cm_find        ; HL -> seen, book
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ld a,47h
        call drawclause
        call unveil
        call candle
        call cm_flag
        ld a,(hl)
        cp 2
        jr nz,cm_ask
        ld hl,msg_inbook
        call textlist
        jp cm_space
cm_ask: ld hl,msg_yn
        call textlist
cm_k:   call waitkey
        cp 'N'
        jr z,cm_no
        cp 'Y'
        jr nz,cm_k
        call cm_flag        ; Y: write it in the book
        ld (hl),2
        ld a,18
        ld c,6
        call clrrows
        ld hl,msg_write
        call textlist
        call cm_find
        inc hl
        inc hl
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ld a,1
        ld (typing),a
        xor a
        ld (skip),a
        ld b,19
        ld a,TXT
        call drawclause
        xor a
        ld (typing),a
        ld a,(cdl)          ; writing it out burns 2 more (not below 0)
        sub 2
        jr nc,cm_w1
        xor a
cm_w1:  ld (cdl),a
        call candle
        jr cm_space
cm_no:  call cm_flag        ; N: found, but left out
        ld (hl),1
        ld a,18
        ld c,6
        call clrrows
        ld hl,msg_leave
        call textlist
cm_space:
        ld a,(cdl)          ; it went out during this compare (there was
        or a                ; candle when it began)
        jr nz,cm_sp1
        ld hl,msg_out
        call textlist
cm_sp1: ld hl,prompt
        call textat
        jp waitspace

cm_find:                    ; HL -> night_find entry for cm_f
        ld a,(cm_f)
        add a,a
        add a,a
        ld e,a
        ld d,0
        ld hl,night_find
        add hl,de
        ret

cm_flag:                    ; HL -> the flag for cm_f
        ld a,(cm_f)
        ld e,a
        ld d,0
        ld hl,night_fflag
        add hl,de
        ret

cm_side:                    ; who and line C of statement A at row B; B after + 1
        ld (cs_s),a
        ld a,c
        ld (cs_c),a
        ld a,b
        ld (cs_r),a
        ld a,(cs_s)
        call getst
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld a,(cs_r)
        ld b,a
        ld c,1
        ld a,07h
        call strat
        ld a,(cs_c)
        ld c,a
        ld a,(cs_s)
        call getclause
        ld a,(cs_r)
        inc a
        ld b,a
        ld a,TXT
        call drawclause
        inc b
        ret

; ---- the clerk's book: what he wrote down, then the names ----
book:   call veil
        ld hl,night_book
        call textlist
        ld b,3
        xor a
        ld (bk_i),a
        ld (bk_n),a
bk1:    ld a,(bk_i)
        cp NIGHT_NF
        jr nc,bk3
        ld e,a
        ld d,0
        ld hl,night_fflag
        add hl,de
        ld a,(hl)
        cp 2
        jr nz,bk2
        ld (bk_n),a
        ld a,(bk_i)
        ld (cm_f),a
        push bc
        call cm_find
        pop bc
        inc hl
        inc hl
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        call bk_block
bk2:    ld hl,bk_i
        inc (hl)
        jr bk1
bk3:    ld a,(par_done)     ; then the parade: the fit, and what else he wrote
        or a
        jr z,bk3b
        ld hl,par_fit       ; the Mayor's words, under a heading, bright
        ld a,(hl)
        inc a
        call bk_room
        ld hl,txt_mayor
        ld c,1
        ld a,07h
        call strat
        inc b
        ld hl,par_fit
        ld a,47h
        call drawclause
        inc b
        ld a,(par_wr)
        ld (pa_m),a
        xor a
        ld (pa_i),a
bkp1:   ld a,(pa_m)
        or a
        jr z,bk3b
        srl a
        ld (pa_m),a
        jr nc,bkp2
        ld hl,par_rec
        call pa_get
        call bk_block
bkp2:   ld hl,pa_i
        inc (hl)
        jr bkp1
bk3b:   ld a,(bk_n)
        or a
        jr nz,bk4
        ld hl,msg_empty
        call textlist
bk4:    call unveil
        ld hl,prompt
        call textat
        call waitspace
        call veil
        ld hl,night_people
        call textlist
        call unveil
        ld hl,prompt
        call textat
        jp waitspace

bk_block:                   ; block HL at row B, a new page if it won't fit
        ld a,(hl)
        push hl
        call bk_room
        pop hl
        ld a,TXT
        call drawclause
        inc b
        ret

bk_room:                    ; A lines are to go at row B: a new page if they won't fit
        ld c,a
        ld a,1              ; the book is not empty
        ld (bk_n),a
        ld a,c
        add a,b
        cp 22
        ret c
        call unveil
        ld hl,prompt
        call textat
        call waitspace
        call veil
        ld hl,night_book
        call textlist
        ld b,3
        ret

; ---- the parade ----
parade: xor a
        ld (par_sel),a
        ld (par_sel+1),a
        ld (par_sel+2),a
        call veil
        ld hl,par_screen
        call textlist
        ld c,0              ; each choice's two options, at rows 8+4i, 9+4i
pa_o:   ld a,c
        cp PAR_NC
        jr nc,pa_od
        push bc
        ld a,c
        add a,a
        add a,a
        ld (pa_r),a
        add a,8
        ld b,a
        ld a,(pa_r)
        ld e,a
        ld d,0
        ld hl,par_opt
        add hl,de
        push hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        push bc
        ld c,2
        ld a,07h
        call strat
        pop bc
        pop hl
        inc hl
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        inc b
        ld c,2
        ld a,07h
        call strat
        pop bc
        inc c
        jr pa_o
pa_od:  call unveil
        ld c,0
pa_m1:  ld a,c
        cp PAR_NC
        jr nc,pa_k
        push bc
        call pa_show
        pop bc
        inc c
        jr pa_m1
pa_k:   call waitkey
        cp 'X'
        ret z
        cp ' '
        jr z,pa_go
        sub '1'
        jr c,pa_k
        cp PAR_NC
        jr nc,pa_k
        ld c,a
        ld b,0
        ld hl,par_sel
        add hl,bc
        ld a,(hl)
        xor 1
        ld (hl),a
        call pa_show
        jr pa_k

pa_show:                    ; choice C: the chosen option bright, with a mark
        ld a,c
        add a,a
        add a,a
        add a,8
        ld (pa_r),a
        ld hl,par_sel
        ld b,0
        add hl,bc
        ld a,(hl)
        ld (pa_s),a
        xor a
        call pa_row
        ld a,1
pa_row: ld e,a              ; option A of the choice in pa_r / pa_s
        ld a,(pa_r)
        add a,e
        ld b,a
        ld a,(pa_s)
        cp e
        ld a,07h
        ld d,' '
        jr nz,pr1
        ld a,47h
        ld d,'*'
pr1:    push de
        push bc
        ld c,1
        call setattr
        pop bc
        pop de
        ld a,d
        jp drawmark

pa_go:  ld a,(par_sel+2)    ; the arrangement: bit i = option of choice i
        add a,a
        ld b,a
        ld a,(par_sel+1)
        or b
        add a,a
        ld b,a
        ld a,(par_sel)
        or b
        add a,a
        ld e,a
        ld d,0
        ld hl,par_combo
        add hl,de
        ld a,(hl)
        ld (pa_sm),a
        inc hl
        ld a,(hl)
        ld (pa_rm),a
        ld a,1
        ld (par_done),a

        call release        ; or the SPACE still held would skip the typing
        ld a,07h            ; the scene, typed
        call clsa
        ld hl,par_brought
        call textlist
        ld a,1
        ld (typing),a
        xor a
        ld (skip),a
        ld b,2
        ld c,0
sc1:    ld a,c
        cp PAR_NC
        jr nc,sc2
        push bc
        ld e,c
        ld d,0
        ld hl,par_sel
        add hl,de
        ld a,c
        add a,a
        add a,(hl)
        ld (pa_i),a
        ld hl,par_scene
        call pa_get
        pop bc
        push bc
        ld a,TXT
        call drawclause
        ld a,b
        pop bc
        ld b,a
        inc c
        jr sc1
sc2:    inc b
        ld hl,par_always
        ld a,47h
        call drawclause
        inc b
        ld hl,par_spoken    ; what she says, in her own words
        ld a,07h
        call drawclause
        inc b
        ld a,(pa_sm)
        ld (pa_m),a
        xor a
        ld (pa_i),a
sn1:    ld a,(pa_m)
        or a
        jr z,sn3
        srl a
        ld (pa_m),a
        jr nc,sn2
        ld hl,par_seen
        call pa_get
        ld a,07h
        call drawclause
        inc b
sn2:    ld hl,pa_i
        inc (hl)
        jr sn1
sn3:    xor a
        ld (typing),a
        ld hl,prompt
        call textat
        call waitspace

        call veil           ; the record: the Mayor's words, then the rest
        ld hl,pr_hdr
        call textlist
        ld b,3
        ld hl,par_fit
        ld a,47h
        call drawclause
        ld a,'*'
        push bc
        ld b,3
        call drawmark
        call unveil
        pop bc
        ld a,(pa_rm)
        or a
        jp z,rc_end
        inc b
        ld hl,pr_more
        ld c,1
        ld a,07h
        call strat
        inc b
        ld a,(pa_rm)
        ld (pa_m),a
        xor a
        ld (pa_i),a
        inc a
        ld (pa_bit),a
rc1:    ld a,(pa_m)
        or a
        jp z,rc_end
        srl a
        ld (pa_m),a
        jr nc,rc3
        ld hl,par_rec
        call pa_get
        ld a,(hl)
        ld (pa_n),a
        ld a,b
        ld (pa_r),a
        ld a,TXT
        call drawclause
        push bc
        ld hl,msg_yn
        call textlist
rc_k:   call waitkey
        cp 'N'
        ld e,07h            ; left out: plain white, a dash in the margin
        ld d,'-'
        jr z,rc2
        cp 'Y'
        jp nz,rc_k
        ld a,(pa_bit)
        ld hl,par_wr
        or (hl)
        ld (hl),a
        ld e,47h
        ld d,'*'
rc2:    push de
        ld a,(pa_r)
        ld b,a
        ld a,(pa_n)
        ld c,a
        ld a,e
        call setattr
        pop de
        ld a,(pa_r)
        ld b,a
        ld a,d
        call drawmark
        ld a,21
        ld c,2
        call clrrows
        pop bc
        inc b
rc3:    ld hl,pa_i
        inc (hl)
        ld hl,pa_bit
        sla (hl)
        jp rc1
rc_end: ld hl,prompt
        call textat
        jp waitspace

pa_get:                     ; HL = word pa_i of the table at HL
        ld a,(pa_i)
        add a,a
        ld e,a
        ld d,0
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

; ---- small helpers ----
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

drawmark:                   ; char A in column 0 of row B, in red
        push af
        ld a,b
        ld (c_row),a
        xor a
        ld (c_col),a
        ld a,MARKA
        ld (c_attr),a
        call clearcell
        ld a,1
        ld (t_x),a
        pop af
        jp putch

; ---- the candle, top right: column 31, pixel rows 0-23 ----
;  a dish at row 22, (cdl) pixels of wax above it, a flame above that
candle: ld hl,cdl_buf
        ld b,24
cn0:    ld (hl),0
        inc hl
        djnz cn0
        ld a,7Eh            ; the dish
        ld (cdl_buf+22),a
        ld a,(cdl)
        or a
        jr z,cn_draw        ; burnt out: the dish only
        ld b,a
        ld a,22
        sub b               ; A = the top of the wax
        ld c,a
        ld e,a
        ld d,0
        ld hl,cdl_buf
        add hl,de
cn1:    ld (hl),3Ch         ; wax
        inc hl
        djnz cn1
        ld a,c
        sub 5
        ld e,a
        ld hl,cdl_buf
        add hl,de
        ex de,hl
        ld hl,cn_flame
        ld bc,5
        ldir
cn_draw:
        ld hl,cdl_buf       ; three cells of column 31, rows 0-2
        ld de,401Fh
        ld c,3
cn2:    ld b,8
        push de
cn3:    ld a,(hl)
        ld (de),a
        inc hl
        inc d
        djnz cn3
        pop de
        ld a,e
        add a,32
        ld e,a
        dec c
        jr nz,cn2
        ld hl,581Fh         ; colours: bright yellow where the flame is
        ld b,3
        ld c,0              ; C = the pixel row of this cell
cn4:    ld (hl),07h
        ld a,(cdl)
        or a
        jr z,cn5
        ld d,a
        ld a,17             ; the flame's top row: 22 - cdl - 5
        sub d               ; its rows: A to A+4
        add a,4
        cp c                ; flame bottom < cell top: not in this cell
        jr c,cn5
        sub 4
        ld d,a
        ld a,c
        add a,7
        cp d                ; cell bottom < flame top: not in this cell
        jr c,cn5
        ld (hl),46h
cn5:    ld de,32
        add hl,de
        ld a,c
        add a,8
        ld c,a
        djnz cn4
        ret
cn_flame:   db 10h,18h,38h,38h,10h

status:                     ; a message (textlist) in rows 20-21
        push hl
        ld a,20
        ld c,2
        call clrrows
        pop hl
        jp textlist

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

; ---- text ----
rd_keys:    db 22,1,05h,"Q A  line     O P  page     M  mark",0
            db 23,1,05h,"C  compare    B  book       X  back",0
            db 0FFh
pg_s:       db "page "
pg_d1:      db "1 of "
pg_d2:      db "1",0
msg_mark1:  db 20,1,TXT,"Marked. Mark a second line to set",0
            db 21,1,TXT,"beside it, here or in another statement.",0
            db 0FFh
msg_mark2:  db 20,1,47h,"Two lines marked. C compares them.",0
            db 0FFh
msg_two:    db 20,1,TXT,"Two lines are marked already. C compares",0
            db 21,1,TXT,"them; M on a marked line takes it off.",0
            db 0FFh
msg_unmark: db 20,1,TXT,"Mark taken off.",0
            db 0FFh
msg_need2:  db 20,1,TXT,"Mark two lines first, then C compares",0
            db 21,1,TXT,"them.",0
            db 0FFh
pr_hdr:     db 0,1,46h,"For the clerk's book",0
            db 2,1,07h,"Mayor Ellis gives you the words:",0
            db 0FFh
pr_more:    db "What else you saw, you may write:",0
txt_mayor:  db "In Mayor Ellis's words:",0
msg_endq:   db 20,1,47h,"End the night?  Y  yes    N  not yet",0
            db 21,1,TXT,"Mayor Ellis will take the book with him.",0
            db 0FFh
cm_title:   db 0,1,46h,"Two lines set side by side",0
            db 0FFh
msg_yn:     db 21,1,47h,"Y  Write it in the clerk's book",0
            db 22,1,47h,"N  Leave it out",0
            db 0FFh
msg_inbook: db 19,1,TXT,"It is in the book already.",0
            db 0FFh
msg_write:  db 18,1,07h,"You write:",0
            db 0FFh
msg_leave:  db 19,1,TXT,"You leave it out of the book.",0
            db 20,1,TXT,"Mayor Ellis does not ask what you found.",0
            db 0FFh
msg_dark:   db 20,1,TXT,"The candle is out. By the fire you can",0
            db 21,1,TXT,"still read, but not compare.",0
            db 0FFh
msg_out:    db 22,1,47h,"The candle has burnt down to nothing.",0
            db 0FFh
msg_empty:  db 3,1,TXT,"Nothing is written in it yet.",0
            db 0FFh

; ---- state ----
cur_st:     db 0
cur_pg:     db 0
cur_cl:     db 0
pg_first:   db 0
pg_cnt:     db 0
pg_row:     ds 16
pg_len:     ds 16
dc_c:       db 0
dp_i:       db 0
dp_r:       db 0
mk_n:       db 0            ; marks: up to two (statement, clause)
mk_s:       ds 2
mk_c:       ds 2
cm_s0:      db 0
cm_c0:      db 0
cm_s1:      db 0
cm_c1:      db 0
cm_f:       db 0
cs_s:       db 0
cs_c:       db 0
cs_r:       db 0
bk_i:       db 0
bk_n:       db 0
par_done:   db 0            ; the parade has been held
par_wr:     db 0            ; bit i: record line i written
par_sel:    ds 3            ; option chosen, per choice
pa_r:       db 0
pa_s:       db 0
pa_i:       db 0
pa_m:       db 0
pa_n:       db 0
pa_bit:     db 0
pa_sm:      db 0
pa_rm:      db 0
cdl:        db 0            ; the candle: units left this night
cdl_buf:    ds 24           ; its column of pixels, top to bottom
night_fflag: ds 16          ; per finding: 0 not found, 1 left out, 2 written
abuf:       ds 768          ; colours of a screen being drawn (veil)
