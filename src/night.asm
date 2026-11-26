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
; ============================================================
TXT     EQU 06h             ; yellow: statement text
SEL     EQU 47h             ; bright white: the line the clerk is on
MARKA   EQU 42h             ; bright red: the clerk's mark in the margin
ROW0    EQU 3               ; first row of statement text

night:  xor a               ; a fresh night: no marks, nothing found
        ld (mk_n),a
        ld hl,night_fflag
        ld b,NIGHT_NF
nt0:    ld (hl),a
        inc hl
        djnz nt0
hub:    call drawhub
hub_k:  call waitkey
        cp 'X'
        ret z
        cp 'B'
        jr nz,hub_1
        call book
        jr hub
hub_1:  cp 'K'
        jr nz,hub_2
        ld hl,msg_parade
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
        jp rd_key

rd_comp:
        ld a,(mk_n)
        cp 2
        jr z,rc_1
        ld hl,msg_need2
        call status
        jp rd_key
rc_1:   call compare
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
        ld bc,0117h
        ld a,05h
        call strat
dp_0:   ld hl,rd_keys
        call textlist
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
        jp cm_space

cm_yes: call cm_find        ; HL -> seen, book
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ld a,47h
        call drawclause
        call unveil
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
        jr cm_space
cm_no:  call cm_flag        ; N: found, but left out
        ld (hl),1
        ld a,18
        ld c,6
        call clrrows
        ld hl,msg_leave
        call textlist
cm_space:
        ld hl,prompt
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
        ld a,TXT
        call drawclause
        inc b
bk2:    ld hl,bk_i
        inc (hl)
        jr bk1
bk3:    ld a,(bk_n)
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

unveil:                     ; show everything drawn since veil, at once
        ld hl,abuf
        ld de,ATTR
        ld bc,768
        ldir
        ld hl,ATTR
        ld (attrbase),hl
        ret

drawclause:                 ; HL = block (db lines, strings), row B, attr A; B after
        ld (c_attr),a
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
        ret

strat:  ld (c_attr),a       ; string HL at row B, column C, attr A
        ld a,b
        ld (c_row),a
        ld a,c
        ld (c_col),a
        jp textraw

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

status:                     ; a message (textlist) in rows 20-21
        push hl
        ld a,20
        ld c,2
        call clrrows
        pop hl
        jr textlist

waitkey:                    ; let go of every key, then A = the next one
wk1:    halt
        call getkey
        or a
        jr nz,wk1
wk2:    halt
        call getkey
        or a
        jr z,wk2
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
msg_mark2:  db 20,1,TXT,"Two lines marked. C compares them.",0
            db 0FFh
msg_two:    db 20,1,TXT,"Two lines are marked already. C compares",0
            db 21,1,TXT,"them; M on a marked line takes it off.",0
            db 0FFh
msg_unmark: db 20,1,TXT,"Mark taken off.",0
            db 0FFh
msg_need2:  db 20,1,TXT,"Mark two lines first, then C compares",0
            db 21,1,TXT,"them.",0
            db 0FFh
msg_parade: db 20,1,TXT,"The parade is not in this build yet.",0
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
night_fflag: ds 16          ; per finding: 0 not found, 1 left out, 2 written
abuf:       ds 768          ; colours of a screen being drawn (veil)
