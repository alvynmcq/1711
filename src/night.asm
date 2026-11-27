; ============================================================
;  The night's screens (v0.8, stage 2): the orders card, the desk,
;  the parade, the ledger, the clerk's book. The words and the tables
;  come from night.inc (scripts/night.py); this code draws them and
;  keeps what the clerk found, what he wrote, and Mayor Ellis's
;  patience.
;
;  The desk: the witnesses come to the table in a fixed order, one
;  closed case each. The screen is split top and bottom:
;    rows 0-2    the witness, "Sworn ...", the Mayor's manner line;
;                the candle in column 31, rows 0-3
;    rows 3-10   what this witness swore (Q / A a line; over the edge
;                turns the page)
;    row 11      a rule, "The book: n  name" (1-9 turn the book to an
;                earlier statement)
;    rows 12-19  that statement (P / L a line)
;    row 20      the result, what is in hand
;    rows 21-22  keys
;    row 23      Mayor Ellis's last slip
;  SPACE compares the two lines: a boxed word over row 11 at once
;  (THEY DIFFER, THEY AGREE, WORD FOR WORD, NO BEARING), an AY thump,
;  1 unit of candle. ENTER: the stamp list (what is in hand, 1-3 toggle
;  how each is written), ENTER again stamps, X goes back. Writing an
;  item burns 2 more. The case is closed: the witness goes.
;
;  Mayor Ellis's patience (pat, 0-12) is never shown as a number: only
;  by the manner line and his slip after each stamp. At 0 he takes the
;  pen and Mr Agnew stamps the rest of the night.
; ============================================================
TXT     EQU 06h             ; yellow: the witness's statement
SEL     EQU 47h             ; bright white: the line the clerk is on
BTXT    EQU 05h             ; cyan: the statement in the book
KEYC    EQU 05h             ; cyan: keys
MARKA   EQU 42h             ; bright red: a mark in the margin
SELOPT  EQU 57h             ; bright white on red: the chosen way to write it
STAMPC  EQU 42h             ; bright red: the stamp
AGNC    EQU 45h             ; bright cyan: Mr Agnew's hand
TOP0    EQU 3               ; the witness's statement: rows 3-10
BOT0    EQU 12              ; the book: rows 12-19
HROWS   EQU 8
RULEROW EQU 11

; a half of the desk (htop, hbot), pointed to by IX
H_ST    EQU 0               ; statement
H_PG    EQU 1               ; page
H_CL    EQU 2               ; the line the clerk is on
H_FIRST EQU 3               ; the page's first line
H_CNT   EQU 4               ; lines on the page
H_ROW0  EQU 5               ; first screen row
H_TXT   EQU 6               ; text colour
H_SEL   EQU 7               ; the chosen line's colour
H_ROWS  EQU 8               ; each line's screen row (8)
H_LEN   EQU 16              ; each line's rows (8)

night:  ld a,NIGHTBANK        ; the night's text and tables, read in place
        call page           ; (op_night's LOAD pages the scripts back)
        ld a,NIGHT_N        ; Mayor Ellis's patience: Night One starts it,
        cp 1                ; later nights add 2 overnight (at most PATMAX)
        ld a,(pat)
        jr nz,nt_on
        xor a
        ld (dismissed),a
        ld a,PAT0-2
nt_on:  add a,2
        cp PATMAX+1
        jr c,nt_p
        ld a,PATMAX
nt_p:   ld (pat),a
        xor a
        ld (gains),a
        ld (par_wr),a
        ld (par_ag),a
        ld (case),a
        ld hl,0
        ld (lastslip),hl
        ld hl,slip_ctr      ; the slips and cold lines start again each night
        ld b,6
nt_s:   ld (hl),a
        inc hl
        djnz nt_s
        ld a,0FFh
        ld (agnew),a        ; the first case Mr Agnew stamped: none yet
        ld a,NIGHT_CANDLE
        ld (cdl),a
        xor a
        ld hl,night_fflag
        ld b,16
nt0:    ld (hl),a
        inc hl
        djnz nt0
        call orders
nt_c:   ld a,(case)         ; the witnesses, one by one
        cp NIGHT_NST
        jr nc,nt_par
        ld a,(dismissed)
        or a
        jr nz,nt_ag
        call desk
        ld hl,case
        inc (hl)
        jr nt_c
nt_ag:  call agnew_rest     ; dismissed: Mr Agnew stamps the rest
nt_par: call parade         ; then the parade, last
        call barebook
        call ledger
        jp book

orders: call veil           ; the Mayor's orders, and how the desk works
        ld hl,night_orders
        call textlist
        call unveil
        ld hl,prompt
        call textat
        jp waitspace

; ============================================================
;  The desk: one witness, until the stamp
; ============================================================
desk:   xor a
        ld (hand_n),a
        ld (box_up),a
        ld ix,htop
        ld a,(case)
        ld (ix+H_ST),a
        call h_open
        ld a,(case)         ; the book opens at the statement before
        or a
        jr z,dk0
        dec a
        ld ix,hbot
        ld (ix+H_ST),a
        call h_open
dk0:    call d_draw
dk_k:   call waitkey
        ld (dk_key),a
        call box_off        ; the compare's box goes at the next key
        ld a,(dk_key)
        ld ix,htop
        cp 'Q'
        jr nz,dk1
        call h_up
        jr dk_k
dk1:    cp 'A'
        jr nz,dk2
        call h_down
        jr dk_k
dk2:    ld ix,hbot
        ld b,a
        ld a,(case)         ; the book's keys, if there is a book
        or a
        ld a,b
        jr z,dk4
        cp 'P'
        jr nz,dk3
        call h_up
        jr dk_k
dk3:    cp 'L'
        jr nz,dk4
        call h_down
        jr dk_k
dk4:    cp ' '
        jr nz,dk5
        call d_comp
        jr dk_k
dk5:    cp 13
        jr nz,dk6
        call d_stamp        ; carry: stamped, the case is closed
        jr nc,dk_k
        ret
dk6:    sub '1'             ; 1-9: the book at an earlier statement
        jr c,dk_k
        ld hl,case
        cp (hl)
        jr nc,dk_k
        ld (ix+H_ST),a
        call h_open
        call h_draw
        call d_rule
        jr dk_k

d_draw:                     ; the whole desk, drawn hidden, shown at once
        call veil
        call d_head
        ld ix,htop
        call h_text
        ld a,(case)
        or a
        jr nz,dd1
        ld hl,msg_bempty    ; the first witness: nothing in the book
        call textlist
        jr dd2
dd1:    ld ix,hbot
        call h_text
dd2:    call d_rule
        ld hl,desk_keys
        call textlist
        call d_hand
        call d_slip
        call unveil
        call candle
        ld ix,htop
        call h_fin
        ld a,(case)
        or a
        ret z
        ld ix,hbot
        jp h_fin

d_head: ld a,(case)         ; rows 0-2: who, sworn, the Mayor's manner
        call getst
        push hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,0001h
        ld a,SEL
        call strat
        pop hl
        inc hl
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,0101h
        ld a,07h
        call strat
d_manner:                   ; row 2: how Mayor Ellis stands, by his patience
        ld a,2
        call rowclr
        call band
        add a,a
        ld e,a
        ld d,0
        ld hl,man_tab
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,0201h
        ld a,KEYC
        jp strat

band:   ld a,(pat)          ; A = 0 (10-12), 1 (6-9), 2 (3-5), 3 (0-2)
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

d_rule:                     ; row 11: a rule, then "The book: n  name"
        ld a,RULEROW
        call rowclr
        ld hl,4860h         ; row 11, its top pixel line
        ld b,32
dr1:    ld (hl),0EEh
        inc l
        djnz dr1
        ld hl,txt_book
        ld bc,RULEROW*256+1
        ld a,KEYC
        call strat
        ld a,(case)
        or a
        jr nz,dr2
        ld hl,txt_bnone
        ld bc,RULEROW*256+9
        ld a,07h
        jp strat
dr2:    ld a,(hbot+H_ST)
        add a,'1'
        ld (dr_n),a
        ld hl,dr_n
        ld bc,RULEROW*256+9
        ld a,SEL
        call strat
        ld a,(hbot+H_ST)
        call getst
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,RULEROW*256+11
        ld a,07h
        jp strat

d_hand: ld a,(hand_n)       ; row 20: what is in hand (the latest)
        or a
        jr nz,dh1
        ld hl,msg_nohand
        jp stat20
dh1:    ld e,a
        ld d,0
        ld hl,hand_f-1
        add hl,de
        ld a,(hl)
        ld e,TXT
d_inhand:                   ; row 20: "In hand: <label of finding A>" (label in E)
        push de
        push af
        ld a,20
        call rowclr
        ld hl,txt_inhand
        ld bc,20*256+1
        ld a,TXT
        call strat
        pop af
        call fr_get
        inc hl
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        pop de
        ld a,e
        ld bc,20*256+8
        jp strat

d_slip: ld a,23             ; row 23: the Mayor's last slip
        call rowclr
        ld hl,(lastslip)
        ld a,h
        or l
        ret z
        ld bc,23*256+1
        ld a,TXT
        jp strat

stat20: push hl             ; a one-row message (a textlist) in row 20
        ld a,20
        call rowclr
        pop hl
        jp textlist

; ---- compare: the line at the table against the line in the book ----
d_comp: ld a,(case)
        or a
        jr nz,dc1
        ld hl,msg_nobook
        jp stat20
dc1:    ld a,(cdl)          ; the candle: none left, no compare
        or a
        jr nz,dc2
        ld hl,msg_dark
        jp stat20
dc2:    dec a
        ld (cdl),a
        ld a,(hbot+H_ST)    ; look the pair up (book, table)
        ld b,a
        ld a,(hbot+H_CL)
        ld c,a
        ld a,(case)
        ld d,a
        ld a,(htop+H_CL)
        ld e,a
        call lookup
        ld (cm_f),a
        cp 0FFh             ; the box first: within 2 frames of the key
        ld a,3
        jr z,dc3
        ld a,(cm_f)
        call fr_get
        ld a,(hl)           ; its kind
dc3:    call box
        ld hl,ay_thump
        call aysnd
        call candle
        ld a,(cm_f)
        cp 0FFh
        jr nz,dc4
        ld hl,msg_nobear
        jp stat20
dc4:    ld e,a              ; found: in hand, if it isn't already
        ld d,0
        ld hl,night_fflag
        add hl,de
        ld a,(hl)
        or a
        ld e,TXT
        jr nz,dc5
        ld (hl),1
        ld a,(hand_n)
        ld e,a
        ld d,0
        ld hl,hand_f
        add hl,de
        ld a,(cm_f)
        ld (hl),a
        ld hl,hand_o
        add hl,de
        ld (hl),0
        ld hl,hand_n
        inc (hl)
        ld e,SEL
dc5:    ld a,(cm_f)
        jp d_inhand

lookup:                     ; B, C (book) D, E (table): A = finding, 0FFh none
        ld hl,night_pairs
        ld a,(hl)
        inc hl
        or a
        jr z,lk_no
        ld (lk_n),a
lk1:    ld a,(hl)
        cp b
        jr nz,lk_n0
        inc hl
        ld a,(hl)
        cp c
        jr nz,lk_n1
        inc hl
        ld a,(hl)
        cp d
        jr nz,lk_n2
        inc hl
        ld a,(hl)
        cp e
        jr nz,lk_n3
        inc hl
        ld a,(hl)
        ret
lk_n0:  inc hl
lk_n1:  inc hl
lk_n2:  inc hl
lk_n3:  inc hl
        inc hl
        ld a,(lk_n)
        dec a
        ld (lk_n),a
        jr nz,lk1
lk_no:  ld a,0FFh
        ret

fr_get: ld l,a              ; HL = the record of finding A
        ld h,0
        add hl,hl
        ld de,night_find
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

box:    ld l,a              ; the boxed word (kind A, 3 = no bearing) over
        ld h,0              ; row 11, cells 9-22, straight to the screen
        ld e,l
        ld d,h
        add hl,hl
        add hl,de
        ld de,box_tab
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)
        inc hl
        ld a,(hl)
        ld (bx_at),a
        push de
        ld hl,4869h         ; row 11, column 9, pixel line 0
        ld c,0
bx1:    push hl
        ld a,c              ; the top and bottom lines solid, else the sides
        or a
        jr z,bx_s
        cp 7
        jr z,bx_s
        ld (hl),80h
        inc l
        ld b,12
bx2:    ld (hl),0
        inc l
        djnz bx2
        ld (hl),01h
        jr bx3
bx_s:   ld b,14
bx4:    ld (hl),0FFh
        inc l
        djnz bx4
bx3:    pop hl
        inc h
        inc c
        ld a,c
        cp 8
        jr nz,bx1
        ld hl,ATTR+RULEROW*32+9
        ld a,(bx_at)
        ld b,14
bx5:    ld (hl),a
        inc hl
        djnz bx5
        pop hl              ; the word, centred
        push hl
        ld b,0
bx6:    ld a,(hl)
        or a
        jr z,bx7
        inc hl
        inc b
        jr bx6
bx7:    ld a,b              ; t_x = 128 - 3 * length
        add a,a
        add a,b
        ld b,a
        ld a,128
        sub b
        ld (t_x),a
        ld a,RULEROW
        ld (c_row),a
        pop hl
bx8:    ld a,(hl)
        or a
        jr z,bx9
        inc hl
        push hl
        call putch
        pop hl
        ld a,(t_x)
        add a,FONTW
        ld (t_x),a
        jr bx8
bx9:    ld a,1
        ld (box_up),a
        ret

box_off:
        ld a,(box_up)
        or a
        ret z
        xor a
        ld (box_up),a
        jp d_rule

; ---- the stamp ----
d_stamp:                    ; carry set if stamped (the case is closed)
        call st_list
sk_k:   call waitkey
        cp 'X'
        jr z,sk_back
        cp 13
        jp z,st_do
        sub '1'
        jr c,sk_k
        ld hl,hand_n
        cp (hl)
        jr nc,sk_k
        ld c,a              ; item C: the next way, Let it lie last
        ld e,a
        ld d,0
        ld hl,hand_f
        add hl,de
        ld a,(hl)
        push de
        call fr_get
        pop de
        inc hl
        ld b,(hl)           ; B = ways to write it (B itself: let it lie)
        ld hl,hand_o
        add hl,de
        ld a,(hl)
        inc a
        cp b
        jr c,sk1
        jr z,sk1
        xor a
sk1:    ld (hl),a
        call st_opts
        jr sk_k
sk_back:                    ; X: back to the desk, nothing stamped
        ld a,12
        ld c,11
        call clrrows
        ld a,(case)
        or a
        jr nz,sb1
        ld hl,msg_bempty
        call textlist
        jr sb2
sb1:    ld ix,hbot
        call h_draw
sb2:    ld hl,desk_keys
        call textlist
        call d_hand
        or a
        ret

st_list:                    ; rows 12-22: what is in hand, and how it goes in
        ld a,12
        ld c,11
        call clrrows
        ld a,(hand_n)
        or a
        jr nz,sl1
        ld hl,msg_nothing
        call textlist
        jr sl3
sl1:    ld hl,msg_hand
        call textlist
        xor a
        ld (sl_i),a
sl2:    ld a,(sl_i)
        ld hl,hand_n
        cp (hl)
        jr nc,sl3
        add a,'1'           ; "1  label"
        ld (dr_n),a
        ld a,(sl_i)
        add a,a
        add a,13
        ld b,a
        ld c,1
        ld hl,dr_n
        ld a,46h
        call strat
        push bc
        ld a,(sl_i)
        ld e,a
        ld d,0
        ld hl,hand_f
        add hl,de
        ld a,(hl)
        call fr_get
        inc hl
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        pop bc
        ld c,3
        ld a,07h
        call strat
        ld a,(sl_i)
        ld c,a
        call st_opts
        ld hl,sl_i
        inc (hl)
        jr sl2
sl3:    ld hl,st_keys
        jp textlist

st_opts:                    ; item C's ways side by side, the chosen one lit
        ld a,c
        add a,a
        add a,14
        ld (so_r),a
        ld e,c
        ld d,0
        ld hl,hand_o
        add hl,de
        ld a,(hl)
        ld (so_sel),a
        ld hl,hand_f
        add hl,de
        ld a,(hl)
        call fr_get
        ld (so_rec),hl
        inc hl
        ld a,(hl)
        ld (so_nw),a
        xor a
        ld (so_j),a
so1:    ld a,(so_j)
        ld hl,so_nw
        cp (hl)
        jr z,so_let
        ret nc
        call way            ; HL = way j's record: its menu first
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        jr so4
so_let: ld hl,txt_letlie
so4:    push hl
        ld hl,(so_rec)      ; its column
        ld de,4
        add hl,de
        ld a,(so_j)
        ld e,a
        add hl,de
        ld c,(hl)
        ld a,(so_r)
        ld b,a
        ld a,(so_sel)
        ld e,a
        ld a,(so_j)
        cp e
        ld a,07h
        jr nz,so5
        ld a,SELOPT
so5:    pop hl
        call strat
        ld hl,so_j
        inc (hl)
        jr so1

way:    ld hl,(so_rec)      ; HL = way (so_j) of the record at so_rec
        ld a,(so_j)
waya:   ld de,7             ; (or: way A of the record at HL)
        add hl,de
        or a
        ret z
        ld de,9
wy1:    add hl,de
        dec a
        jr nz,wy1
        ret

st_do:  xor a               ; ENTER: stamp it, with what is in hand
        ld (st_d),a
        ld (st_q),a
        ld (st_sc),a
        ld (sd_i),a
        ld hl,0
        ld (st_w),hl
        ld a,(cdl)
        ld (st_c0),a
sd1:    ld a,(sd_i)
        ld hl,hand_n
        cp (hl)
        jp nc,sd_go
        ld e,a
        ld d,0
        ld hl,hand_o
        add hl,de
        ld a,(hl)
        ld (sd_o),a
        ld hl,hand_f
        add hl,de
        ld a,(hl)
        ld (sd_f),a
        call fr_get
        inc hl
        ld b,(hl)
        dec hl
        ld a,(sd_o)
        cp b
        jp z,sd_n           ; let it lie: found, not written (flag stays 1)
        push hl
        ld a,(sd_f)         ; written: flag = 2 + the way
        ld e,a
        ld d,0
        ld hl,night_fflag
        add hl,de
        ld a,(sd_o)
        add a,2
        ld (hl),a
        pop hl
        ld a,(sd_o)
        call waya
        ld (sd_w),hl
        ld a,(cdl)          ; writing it out burns 2 (not below 0)
        sub 2
        jr nc,sd_c
        xor a
sd_c:   ld (cdl),a
        ld hl,(sd_w)        ; a question, if it has an answer
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        or (hl)
        jr z,sd_nq
        ld a,1
        ld (st_q),a
sd_nq:  ld hl,(sd_w)
        ld de,8
        add hl,de
        ld a,(hl)
        ld (sd_p),a
        bit 7,a             ; which item speaks for the slip: costs
        jr z,sd_g           ; first (2|p|+1), then gains (2p)
        neg
        add a,a
        inc a
        jr sd_s
sd_g:   add a,a
sd_s:   ld hl,st_sc
        cp (hl)
        jr c,sd_cap
        jr z,sd_cap
        ld (hl),a
        ld hl,(sd_w)
        ld (st_w),hl
sd_cap: ld a,(sd_p)         ; desk gains: at most GAIN_MAX a night
        bit 7,a
        jr nz,sd_add
        or a
        jr z,sd_add
        ld b,a
        ld hl,gains
        ld a,GAIN_MAX
        sub (hl)
        cp b
        jr nc,sd_cp1
        ld b,a
sd_cp1: ld a,(hl)
        add a,b
        ld (hl),a
        ld a,b
        ld (sd_p),a
sd_add: ld a,(st_d)
        ld hl,sd_p
        add a,(hl)
        ld (st_d),a
sd_n:   ld hl,sd_i
        inc (hl)
        jp sd1

sd_go:  ld a,12             ; the stamp, in large letters (rows 12-23
        ld c,12             ; cleared: the old slip goes too)
        call clrrows
        ld hl,stamp_sworn
        ld a,(st_q)
        or a
        jr z,sg1
        ld hl,stamp_q
sg1:    ld b,12
        ld a,STAMPC
        call bigstamp
        ld hl,ay_stamp
        call aysnd
        ld b,15
sg1w:   halt
        djnz sg1w
        ld a,1              ; the answers, typed, one under another
        ld (typing),a
        xor a
        ld (skip),a
        ld (sd_i),a
        ld b,14
sg2:    ld a,(sd_i)
        ld hl,hand_n
        cp (hl)
        jr nc,sg4
        ld e,a
        ld d,0
        ld hl,hand_o
        add hl,de
        ld c,(hl)
        ld hl,hand_f
        add hl,de
        ld a,(hl)
        push bc
        call fr_get
        pop bc
        inc hl
        ld a,c
        cp (hl)             ; let it lie: nothing to answer
        jr z,sg3
        dec hl
        push bc
        call waya
        pop bc
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        jr z,sg3
        ld a,07h
        call drawclause
sg3:    ld hl,sd_i
        inc (hl)
        jr sg2
sg4:    xor a
        ld (typing),a
        ld a,(st_d)         ; his patience, and his manner at once
        call pat_add
        call d_manner
        ld hl,(st_w)        ; the slip: the item that speaks, or by the cost
        ld a,h
        or l
        jr z,sg_b
        ld de,6
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        jr nz,sg_s
sg_b:   ld a,(st_d)
        call slip_band
sg_s:   ld (lastslip),hl
        ld bc,20*256+1
        ld a,TXT
        call strat
        ld a,(st_d)
        call cold_note      ; a cold line above it, and the note
        call candle
        ld a,(st_c0)        ; the candle went out with this stamp
        or a
        jr z,sg_p
        ld a,(cdl)
        or a
        jr nz,sg_p
        ld hl,msg_out
        call textlist
sg_p:   ld hl,prompt
        call textat
        call waitspace
        ld a,(pat)
        or a
        call z,dismiss
        scf
        ret

cold_note:                  ; A = the change: a cost that leaves him at 5 or
        ld (cn_d),a         ; less puts a cold line on row 19; then the note
        bit 7,a
        jr z,cn_n
        ld a,(pat)
        or a
        jr z,cn_n
        cp 6
        jr nc,cn_n
        ld hl,cold_tab
        ld a,(cold_ctr)
        cp (hl)
        jr c,cnl1
        xor a
cnl1:   ld e,a
        inc a
        ld (cold_ctr),a
        inc hl
        ld d,0
        add hl,de
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,19*256+1
        ld a,07h
        call strat
cn_n:   ld a,(cn_d)         ; a low note for a cost, a brighter one for a gain
        or a
        ret z
        ld hl,ay_low
        bit 7,a
        jr nz,cnl2
        ld hl,ay_high
cnl2:   jp aysnd

slip_band:                  ; A = the change: HL = the next slip of its band
        ld b,0              ; (0 gain, 1 none, 2 -1, 3 -2, 4 -3 or worse)
        bit 7,a
        jr nz,sb_neg
        or a
        jr nz,sb_i
        inc b
        jr sb_i
sb_neg: neg
        inc a
        cp 5
        jr c,sb_ng
        ld a,4
sb_ng:  ld b,a
sb_i:   ld a,b
        ld (sb_k),a
        add a,a
        ld e,a
        ld d,0
        ld hl,slip_tab
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld c,(hl)           ; how many in this band
        inc hl
        push hl
        ld a,(sb_k)
        ld e,a
        ld d,0
        ld hl,slip_ctr
        add hl,de
        ld a,(hl)
        cp c
        jr c,sbd2
        xor a
sbd2:   ld b,a
        inc a
        ld (hl),a
        pop hl
        ld e,b
        ld d,0
        add hl,de
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

pat_add:                    ; patience + A (signed), kept within 0-PATMAX
        ld b,a
        ld a,(pat)
        add a,b
        bit 7,a
        jr z,pd1
        xor a
pd1:    cp PATMAX+1
        jr c,pd2
        ld a,PATMAX
pd2:    ld (pat),a
        ret

; ---- dismissal: Mayor Ellis takes the pen ----
dismiss:
        ld a,1
        ld (dismissed),a
        ld a,07h
        call clsa
        ld hl,msg_pen
        call textlist
        ld b,8
        ld hl,txt_dismiss
        ld a,SEL
        call drawclause
        ld hl,ay_low
        call aysnd
        ld hl,prompt
        call textat
        jp waitspace

agnew_rest:                 ; Mr Agnew stamps the rest, faster and faster
        ld a,(case)
        cp NIGHT_NST
        ret nc
        ld (agnew),a
        ld a,07h
        call clsa
        ld hl,msg_agnew
        call textlist
        ld a,48
        ld (ag_w),a
ag1:    ld a,8
        ld c,6
        call clrrows
        ld a,(case)
        call getst
        push hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,8*256+1
        ld a,SEL
        call strat
        pop hl
        inc hl
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,9*256+1
        ld a,07h
        call strat
        ld hl,stamp_sworn
        ld b,11
        ld a,AGNC
        call bigstamp
        ld hl,ay_thump
        call aysnd
        ld a,(ag_w)
        ld b,a
ag2:    halt
        djnz ag2
        ld a,(ag_w)
        srl a
        cp 6
        jr nc,ag3
        ld a,6
ag3:    ld (ag_w),a
        ld hl,case
        inc (hl)
        ld a,(hl)
        cp NIGHT_NST
        jr c,ag1
        ld hl,prompt
        call textat
        jp waitspace

barebook:                   ; only the fit in the book at the night's end
        ld a,(dismissed)
        or a
        ret nz
        ld a,(par_wr)
        or a
        ret nz
        ld hl,night_fflag
        ld b,NIGHT_NF
bbk1:   ld a,(hl)
        cp 2
        ret nc
        inc hl
        djnz bbk1
        ld a,256-BARE
        call pat_add
        ld a,(pat)
        or a
        ret nz
        ld a,1
        ld (dismissed),a
        ret

; ---- the big stamp: HL -> db x, first cell, last cell, string; row B,
;  colour A. Letters twice as tall (rows B and B+1), in a ruled box.
bigstamp:
        ld (bs_at),a
        ld a,b
        ld (bs_row),a
        ld a,(hl)
        ld (t_x),a
        inc hl
        ld a,(hl)
        ld (bs_c0),a
        inc hl
        ld a,(hl)
        ld (bs_c1),a
        inc hl
        push hl
        ld a,(bs_row)       ; its colours, two rows
        ld l,a
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld de,(attrbase)
        add hl,de
        ld a,(bs_c0)
        ld e,a
        ld d,0
        add hl,de
        push hl
        call bs_n
        pop hl
        ld de,32
        add hl,de
        call bs_n
        ld a,(bs_row)       ; the box: top and bottom lines, the sides
        add a,a
        add a,a
        add a,a
        ld (bs_y),a
        call bs_line
        ld a,(bs_y)
        add a,15
        call bs_line
        ld b,16
bs1:    push bc
        ld a,(bs_y)
        call pxaddr
        push hl
        ld a,(bs_c0)
        or l
        ld l,a
        ld a,(hl)
        or 80h
        ld (hl),a
        pop hl
        ld a,(bs_c1)
        or l
        ld l,a
        ld a,(hl)
        or 01h
        ld (hl),a
        ld hl,bs_y
        inc (hl)
        pop bc
        djnz bs1
        pop hl
bs2:    ld a,(hl)           ; the letters
        or a
        ret z
        inc hl
        push hl
        call bigch
        pop hl
        ld a,(t_x)
        add a,FONTW
        ld (t_x),a
        jr bs2

bs_n:   ld a,(bs_c0)        ; colour the box's cells along a row at HL
        ld b,a
        ld a,(bs_c1)
        sub b
        inc a
        ld b,a
        ld a,(bs_at)
bsn1:   ld (hl),a
        inc hl
        djnz bsn1
        ret

bs_line:                    ; a solid line at pixel row A across the box
        call pxaddr
        ld a,(bs_c0)
        or l
        ld l,a
        ld a,(bs_c0)
        ld b,a
        ld a,(bs_c1)
        sub b
        inc a
        ld b,a
bl1:    ld (hl),0FFh
        inc l
        djnz bl1
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

; ---- AY: a few register writes, no player (HL -> reg, value ..., 0FFh) ----
aysnd:  ld a,(hl)
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

; ============================================================
;  The desk's halves (IX = htop or hbot)
; ============================================================
h_open: xor a               ; at the statement's first page and line
        ld (ix+H_PG),a
        call h_pgset
        ld a,(ix+H_FIRST)
        ld (ix+H_CL),a
        ret

h_pgset:                    ; H_FIRST, H_CNT for H_ST, H_PG
        ld a,(ix+H_ST)
        call getst
        ld de,10
        add hl,de
        ld a,(ix+H_PG)
        add a,a
        ld e,a
        ld d,0
        add hl,de
        ld a,(hl)
        ld (ix+H_FIRST),a
        inc hl
        ld a,(hl)
        ld (ix+H_CNT),a
        ret

h_last: ld a,(ix+H_FIRST)   ; A = the page's last line
        add a,(ix+H_CNT)
        dec a
        ret

h_draw: ld a,(ix+H_ROW0)    ; redraw the half, hidden, then shown at once
        ld c,HROWS
        call clrrows
        call h_off          ; its colours black while it is drawn
        ld de,ATTR
        add hl,de
        ld b,0              ; HROWS * 32 = 256
hd1:    ld (hl),0
        inc hl
        djnz hd1
        call h_off
        ld de,abuf
        add hl,de
        ld b,0
hd2:    ld (hl),07h
        inc hl
        djnz hd2
        ld hl,abuf
        ld (attrbase),hl
        call h_text
        call h_off          ; shown: its rows of abuf to the screen
        push hl
        ld de,abuf
        add hl,de
        ex (sp),hl
        ld de,ATTR
        add hl,de
        ex de,hl
        pop hl
        ld bc,HROWS*32
        ldir
        ld hl,ATTR
        ld (attrbase),hl
        call h_fin
        ld a,(ix+H_ROW0)
        cp TOP0
        ret nz
        jp candle           ; row 3 holds the candle's foot

h_off:  ld a,(ix+H_ROW0)    ; HL = the half's first row * 32
        ld l,a
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ret

h_text: ld a,(ix+H_ROW0)    ; the page's lines, from H_ROW0
        ld (dp_r),a
        xor a
        ld (dp_i),a
ht1:    ld a,(dp_i)
        cp (ix+H_CNT)
        ret nc
        push ix
        pop hl
        ld e,a
        ld d,0
        add hl,de
        ld de,H_ROWS
        add hl,de
        ld a,(dp_r)
        ld (hl),a
        ld a,(dp_i)
        add a,(ix+H_FIRST)
        ld c,a
        ld a,(ix+H_ST)
        call getclause
        ld a,(hl)           ; its rows
        push hl
        push ix
        pop hl
        ld a,(dp_i)
        ld e,a
        ld d,0
        add hl,de
        ld de,H_LEN
        add hl,de
        pop de
        ld a,(de)
        ld (hl),a
        ex de,hl
        ld a,(dp_r)
        ld b,a
        ld a,(ix+H_TXT)
        call drawclause
        ld a,b
        ld (dp_r),a
        ld hl,dp_i
        inc (hl)
        jr ht1

h_fin:  ld a,(ix+H_ROW0)    ; '^' / 'v' in the margin when there is more,
        ld b,a              ; then the clerk's line lit
        ld e,KEYC
        ld a,(ix+H_PG)
        or a
        ld a,' '
        jr z,hf1
        ld a,'^'
hf1:    call drawch
        ld a,(ix+H_ST)
        call getst
        ld de,9
        add hl,de
        ld a,(ix+H_PG)
        inc a
        cp (hl)
        ld a,' '
        jr nc,hf2
        ld a,'v'
hf2:    ld b,a
        ld a,(ix+H_ROW0)
        add a,HROWS-1
        ld c,b
        ld b,a
        ld a,c
        ld e,KEYC
        call drawch
        ld a,(ix+H_SEL)
h_hl:   push af             ; colour the clerk's line with A
        ld a,(ix+H_CL)
        sub (ix+H_FIRST)
        ld e,a
        ld d,0
        push ix
        pop hl
        add hl,de
        ld de,H_ROWS
        add hl,de
        ld b,(hl)
        ld de,8
        add hl,de
        ld c,(hl)
        pop af
        jp setattr

h_up:   ld a,(ix+H_CL)
        cp (ix+H_FIRST)
        jr z,hu_pg
        ld a,(ix+H_TXT)
        call h_hl
        dec (ix+H_CL)
        ld a,(ix+H_SEL)
        jp h_hl
hu_pg:  ld a,(ix+H_PG)      ; top of the page: back a page, to its last line
        or a
        ret z
        dec (ix+H_PG)
        call h_pgset
        call h_last
        ld (ix+H_CL),a
        jp h_draw

h_down: call h_last
        cp (ix+H_CL)
        jr z,hd_pg
        ld a,(ix+H_TXT)
        call h_hl
        inc (ix+H_CL)
        ld a,(ix+H_SEL)
        jp h_hl
hd_pg:  ld a,(ix+H_ST)      ; foot of the page: on a page, if there is one
        call getst
        ld de,9
        add hl,de
        ld a,(ix+H_PG)
        inc a
        cp (hl)
        ret nc
        ld (ix+H_PG),a
        call h_pgset
        ld a,(ix+H_FIRST)
        ld (ix+H_CL),a
        jp h_draw

getst:  ld l,a              ; HL = statement record A:
        ld h,0              ; dw who, sworn, short, clauses; db n, pages; pages
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

rowclr:                     ; clear row A, columns 0-30 (31: the candle), and
        push af             ; colour it white through attrbase
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
rw1:    push hl
        ld b,31
rw2:    ld (hl),0
        inc l
        djnz rw2
        pop hl
        inc h
        dec c
        jr nz,rw1
        pop af
        ld l,a
        ld h,0
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        add hl,hl
        ld de,(attrbase)
        add hl,de
        ld b,31
rw3:    ld (hl),07h
        inc hl
        djnz rw3
        ret

; ============================================================
;  The ledger, at the night's end: what the clerk did, never what
;  there was
; ============================================================
ledger: xor a
        ld (lg_q),a
        ld (lg_n),a
        ld (lg_i),a
lg1:    ld a,(lg_i)         ; questions put, agreements noted
        cp NIGHT_NF
        jr nc,lg3
        ld e,a
        ld d,0
        ld hl,night_fflag
        add hl,de
        ld a,(hl)
        sub 2
        jr c,lg2
        push af
        ld a,(lg_i)
        call fr_get
        pop af
        call waya
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        or (hl)
        ld hl,lg_n
        jr z,lg1b
        ld hl,lg_q
lg1b:   inc (hl)
lg2:    ld hl,lg_i
        inc (hl)
        jr lg1
lg3:    call veil
        ld hl,night_ledger
        call textlist
        ld a,(agnew)        ; statements the clerk entered
        cp NIGHT_NST
        jr c,lg4
        ld a,NIGHT_NST
lg4:    push af
        ld e,TXT
        ld a,e
        ld (lg_at),a
        pop af
        push af
        ld hl,lt_ent
        ld b,3
        call lg_row
        ld a,(lg_q)
        ld hl,lt_q
        ld b,4
        call lg_row
        ld a,(lg_n)
        ld hl,lt_n
        ld b,5
        call lg_row
        ld a,(par_ag)       ; the parade's lines (none in Mr Agnew's hand)
        or a
        ld a,0
        jr nz,lg5
        ld a,(par_wr)
        ld c,0
lg4b:   or a
        jr z,lg4c
        srl a
        jr nc,lg4b
        inc c
        jr lg4b
lg4c:   ld a,c
lg5:    ld hl,lt_par
        ld b,6
        call lg_row
        pop af
        ld b,a
        ld a,NIGHT_NST
        sub b
        jr z,lg6
        ld hl,lt_ag         ; Mr Agnew's, in his colour
        ld b,7
        ld e,a
        ld a,AGNC
        ld (lg_at),a
        ld a,e
        call lg_row
lg6:    ld hl,lt_cdl        ; the candle, in words
        ld bc,8*256+1
        ld a,TXT
        call strat
        ld a,(cdl)
        ld hl,lc_0
        or a
        jr z,lg7
        ld hl,lc_1
        cp CDL_Q+1
        jr c,lg7
        ld hl,lc_2
        cp CDL_H+1
        jr c,lg7
        ld hl,lc_3
lg7:    ld bc,8*256+18
        ld a,07h
        call strat
        ld hl,lt_mayor      ; his goodnight, by his patience
        ld bc,10*256+1
        ld a,07h
        call strat
        ld a,(dismissed)
        or a
        jr z,lg8
        ld b,11
        ld hl,txt_dismiss
        ld a,SEL
        call drawclause
        jr lg9
lg8:    call band
        ld b,11
        add a,a
        ld e,a
        ld d,0
        ld hl,good_tab
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld a,TXT
        call drawclause
lg9:    ld hl,lt_next       ; and the next night's order
        ld bc,15*256+1
        ld a,46h
        call strat
        ld b,16
        ld hl,txt_next
        ld a,07h
        call drawclause
        call unveil
        ld hl,prompt
        call textat
        jp waitspace

lg_row: push af             ; label HL at row B in colour lg_at, the
        ld c,1              ; number A at column 28, bright
        ld a,(lg_at)
        call strat
        pop af
        add a,'0'
        ld (dr_n),a
        ld hl,dr_n
        ld c,28
        ld a,(lg_at)
        or 40h
        jp strat

; ============================================================
;  The clerk's book: what was written, case by case, then the parade,
;  then the names
; ============================================================
book:   call veil
        ld hl,night_book
        call textlist
        ld b,3
        xor a
        ld (bk_n),a
        ld (bk_c),a
bk_cs:  ld a,(bk_c)
        cp NIGHT_NST
        jp nc,bk_par
        ld hl,agnew
        cp (hl)
        jr c,bk_cl
        ld a,1              ; Mr Agnew's: one line, in his colour
        call bk_room
        ld a,(bk_c)
        push bc
        call getst
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        pop bc
        ld c,1
        ld a,AGNC
        call strat
        ld hl,txt_asworn
        ld c,17
        ld a,AGNC
        call strat
        inc b
        jr bk_nx
bk_cl:  xor a               ; the clerk's: each finding of this case written
        ld (bk_i),a
bk_f:   ld a,(bk_i)
        cp NIGHT_NF
        jr nc,bk_nx
        ld e,a
        ld d,0
        ld hl,night_fcase
        add hl,de
        ld a,(bk_c)
        cp (hl)
        jr nz,bk_f2
        ld hl,night_fflag
        add hl,de
        ld a,(hl)
        sub 2
        jr c,bk_f2
        push bc
        push af
        ld a,(bk_i)
        call fr_get
        pop af
        call waya
        ld (bk_wp),hl
        pop bc
        inc hl              ; the book text
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld a,(hl)           ; it and its answer must fit together
        ld (bk_ln),a
        push hl
        ld hl,(bk_wp)
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        jr z,bk_f1
        ld a,(bk_ln)
        add a,(hl)
        ld (bk_ln),a
bk_f1:  ld a,(bk_ln)
        call bk_room
        pop hl
        ld a,TXT
        call drawclause
        ld hl,(bk_wp)       ; the answer under it, in white
        ld de,4
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        jr z,bk_f3
        ld a,07h
        call drawclause
bk_f3:  inc b
bk_f2:  ld hl,bk_i
        inc (hl)
        jr bk_f
bk_nx:  ld hl,bk_c
        inc (hl)
        jp bk_cs

bk_par: ld a,(bk_n)         ; nothing written from the desk
        or a
        jr nz,bk_p1
        ld hl,txt_bare
        ld c,1
        ld a,TXT
        call strat
        inc b
        inc b
bk_p1:  ld hl,par_fit       ; then the parade: the Mayor's words, bright
        ld a,(hl)           ; (Mr Agnew's colour if he wrote it)
        inc a
        call bk_room
        ld hl,txt_mayor
        ld c,1
        ld a,07h
        call strat
        inc b
        ld hl,par_fit
        ld a,(par_ag)
        or a
        ld a,SEL
        jr z,bk_p2
        ld a,AGNC
bk_p2:  call drawclause
        inc b
        ld a,(par_wr)
        ld (pa_m),a
        xor a
        ld (pa_i),a
bkp1:   ld a,(pa_m)
        or a
        jr z,bk_end
        srl a
        ld (pa_m),a
        jr nc,bkp2
        ld hl,par_rec
        call pa_get
        ld a,(hl)
        push hl
        call bk_room
        pop hl
        ld a,TXT
        call drawclause
        inc b
bkp2:   ld hl,pa_i
        inc (hl)
        jr bkp1
bk_end: call unveil
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

; ============================================================
;  The parade, last: the clerk arranges how the accused is brought
;  (1-3, SPACE sends for her), the scene, then what goes in the book:
;  the fit always (the Mayor's words), each other line Y or N, each
;  with its cost to the Mayor's patience. Dismissed, the Mayor
;  arranges it himself (the first option of each choice: told, alone,
;  into the room) and the fit is all that is written, by Mr Agnew.
; ============================================================
parade: xor a
        ld (par_sel),a
        ld (par_sel+1),a
        ld (par_sel+2),a
        ld (par_d),a
        ld a,(dismissed)
        or a
        jp nz,pa_go
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
pa_od:  ld a,(par_port)     ; the accused's face, cols 22-31, rows 6-17
        cp 0FFh             ; (drawn while veiled: shown with the rest)
        jr z,pa_od2
        ld bc,6*256+22
        call portrait
pa_od2: call unveil
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

        call release        ; or the SPACE still held would skip the typing
        ld a,07h            ; the scene, typed
        call clsa
        ld hl,par_brought
        ld a,(dismissed)
        or a
        jr z,sc0
        ld hl,par_mayor
sc0:    call textlist
        ld a,1
        ld (typing),a
        xor a
        ld (skip),a
        ld b,3
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
        ld a,(dismissed)    ; Mr Agnew writes the fit, and nothing else
        or a
        jr z,pa_rec
        ld a,1
        ld (par_ag),a
        ret

pa_rec: call veil           ; the record: the Mayor's words, then the rest
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
        ld a,(pa_i)         ; its cost to his patience
        ld e,a
        ld d,0
        ld hl,par_pat
        add hl,de
        ld a,(par_d)
        add a,(hl)
        ld (par_d),a
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
rc_end: ld a,(par_d)        ; his patience, and what he says
        call pat_add
        ld a,(par_d)
        call slip_band
        ld (lastslip),hl
        ld bc,22*256+1
        ld a,TXT
        call strat
        ld a,(par_d)
        ld (cn_d),a
        bit 7,a             ; a cold line, on row 21 here
        jr z,rc_e1
        ld a,(pat)
        or a
        jr z,rc_e1
        cp 6
        jr nc,rc_e1
        ld hl,cold_tab
        ld a,(cold_ctr)
        cp (hl)
        jr c,rc_e0
        xor a
rc_e0:  ld e,a
        inc a
        ld (cold_ctr),a
        inc hl
        ld d,0
        add hl,de
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld bc,21*256+1
        ld a,07h
        call strat
rc_e1:  ld a,(cn_d)
        or a
        jr z,rc_e2
        ld hl,ay_low
        bit 7,a
        jr nz,rc_e3
        ld hl,ay_high
rc_e3:  call aysnd
rc_e2:  ld hl,prompt
        call textat
        call waitspace
        ld a,(pat)
        or a
        ret nz
        jp dismiss

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
        ld e,MARKA
drawch: push af             ; char A in column 0 of row B, colour E
        ld a,b
        ld (c_row),a
        xor a
        ld (c_col),a
        ld a,e
        ld (c_attr),a
        call clearcell
        ld a,1
        ld (t_x),a
        pop af
        jp putch

setattr:                    ; colour C rows from row B, columns 1-30, with A
        push af             ; (column 31 is the candle's in rows 0-3)
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
sa1:    ld b,30
sa2:    ld (hl),a
        inc hl
        djnz sa2
        inc hl              ; past columns 31 and 0
        inc hl
        dec c
        jr nz,sa1
        ret

; ---- the candle, top right: column 31, pixel rows 0-31 ----
;  a dish at pixel row 30, (cdl) pixels of wax above it, a flame above
;  that (at most 25 units)
candle: ld hl,cdl_buf
        ld b,32
cn0:    ld (hl),0
        inc hl
        djnz cn0
        ld a,7Eh            ; the dish
        ld (cdl_buf+30),a
        ld a,(cdl)
        or a
        jr z,cn_draw        ; burnt out: the dish only
        ld b,a
        ld a,30
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
        ld hl,cdl_buf       ; four cells of column 31, rows 0-3
        ld de,401Fh
        ld c,4
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
        ld b,4
        ld c,0              ; C = the pixel row of this cell
cn4:    ld (hl),07h
        ld a,(cdl)
        or a
        jr z,cn5
        ld d,a
        ld a,25             ; the flame's top row: 30 - cdl - 5
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
desk_keys:  db 21,1,KEYC,"Q A  line   P L  book line   1-6  book",0
            db 22,1,KEYC,"SPACE  compare           ENTER  stamp",0
            db 0FFh
st_keys:    db 21,1,KEYC,"1 2 3  change          ENTER  stamp it",0
            db 22,1,KEYC,"X  not yet",0
            db 0FFh
msg_hand:   db 12,1,46h,"In hand, for the book:",0
            db 0FFh
msg_nothing: db 12,1,46h,"Nothing in hand.",0
            db 14,1,TXT,"It goes into the book as sworn.",0
            db 0FFh
msg_nohand: db 20,1,TXT,"Nothing in hand.",0
            db 0FFh
msg_bempty: db 13,1,BTXT,"Nothing is in the book yet. This is",0
            db 14,1,BTXT,"the first statement of the night.",0
            db 0FFh
msg_nobook: db 20,1,TXT,"Nothing in the book to set it beside.",0
            db 0FFh
msg_nobear: db 20,1,TXT,"They do not bear on one another.",0
            db 0FFh
msg_dark:   db 20,1,TXT,"The candle is out. You read by the fire.",0
            db 0FFh
msg_out:    db 21,1,47h,"The candle has burnt down to nothing.",0
            db 0FFh
msg_pen:    db 4,1,46h,"Mayor Ellis holds out his hand.",0
            db 0FFh
msg_agnew:  db 1,1,46h,"Mr Agnew writes.",0
            db 3,1,TXT,"You sit by the fire.",0
            db 0FFh
txt_book:   db "The book:",0
txt_bnone:  db "empty",0
txt_inhand: db "In hand:",0
txt_letlie: db "Let it lie",0
txt_asworn: db "Entered as sworn.",0
txt_bare:   db "Nothing but what was sworn.",0
dr_n:       db "0",0
stamp_sworn: db 80,9,22,"ENTERED AS SWORN",0
stamp_q:    db 62,6,25,"ENTERED. QUESTION PUT.",0
box_tab:    dw bw_differ
            db 57h          ; bright white on red
            dw bw_agree
            db 78h          ; black on bright white
            dw bw_copy
            db 70h          ; black on bright yellow
            dw bw_none
            db 07h          ; plain
bw_differ:  db "THEY DIFFER",0
bw_agree:   db "THEY AGREE",0
bw_copy:    db "WORD FOR WORD",0
bw_none:    db "NO BEARING",0
lt_ent:     db "Statements entered",0
lt_q:       db "Questions put",0
lt_n:       db "Agreements noted",0
lt_par:     db "Lines of the parade written",0
lt_ag:      db "Entered by Mr Agnew",0
lt_cdl:     db "The candle",0
lc_0:       db "burnt to the dish",0
lc_1:       db "a stub left",0
lc_2:       db "half left",0
lc_3:       db "more than half left",0
lt_mayor:   db "Mayor Ellis, taking the book:",0
lt_next:    db "His order for tomorrow:",0
pr_hdr:     db 0,1,46h,"For the clerk's book",0
            db 2,1,07h,"Mayor Ellis gives you the words:",0
            db 0FFh
pr_more:    db "What else you saw, you may write:",0
txt_mayor:  db "In Mayor Ellis's words:",0
msg_yn:     db 21,1,47h,"Y  Write it in the clerk's book",0
            db 22,1,47h,"N  Leave it out",0
            db 0FFh

; AY register writes: a thump (the compare), the stamp, a low note (a
; cost), a brighter one (a gain). Channel A, the envelope decaying.
ay_thump:   db 0,0,1,6,6,1Fh,7,36h,8,10h,11,0,12,3,13,0,0FFh
ay_stamp:   db 0,0,1,9,6,1Fh,7,36h,8,10h,11,0,12,7,13,0,0FFh
ay_low:     db 0,0,1,3,7,3Eh,8,10h,11,0,12,10h,13,0,0FFh
ay_high:    db 0,0,1,1,7,3Eh,8,10h,11,0,12,0Ch,13,0,0FFh

; ---- state ----
; Kept below C000h, so they outlive the night's bank (for the trial):
pat:        db PAT0         ; Mayor Ellis's patience, 0-PATMAX
dismissed:  db 0            ; he took the pen (for good)
night_fflag: ds 16          ; per finding: 0 not found, 1 found and let lie,
                            ; 2 + the way it was written
par_wr:     db 0            ; bit i: parade record line i written
par_ag:     db 0            ; Mr Agnew wrote the parade
agnew:      db 0FFh         ; the first case Mr Agnew stamped (0FFh: none)
; The night's working state:
case:       db 0            ; the witness at the table
gains:      db 0            ; desk gains to his patience this night
lastslip:   dw 0
slip_ctr:   ds 5            ; the next slip of each band
cold_ctr:   db 0
hand_n:     db 0            ; in hand: up to three findings, and the way
hand_f:     ds 3            ; each is to be written (its count: let it lie)
hand_o:     ds 3
htop:       db 0,0,0,0,0,TOP0,TXT,SEL
            ds 16
hbot:       db 0,0,0,0,0,BOT0,BTXT,SEL
            ds 16
dk_key:     db 0
box_up:     db 0
bx_at:      db 0
cm_f:       db 0
lk_n:       db 0
dp_i:       db 0
dp_r:       db 0
dc_c:       db 0
sl_i:       db 0
so_r:       db 0
so_sel:     db 0
so_nw:      db 0
so_j:       db 0
so_rec:     dw 0
st_d:       db 0            ; the stamp: the change to his patience,
st_q:       db 0            ; a question put, which item speaks, its score
st_w:       dw 0
st_sc:      db 0
st_c0:      db 0
sd_i:       db 0
sd_o:       db 0
sd_f:       db 0
sd_p:       db 0
sd_w:       dw 0
sb_k:       db 0
cn_d:       db 0
ag_w:       db 0
bs_at:      db 0
bs_row:     db 0
bs_c0:      db 0
bs_c1:      db 0
bs_y:       db 0
bc_g:       dw 0
bc_y:       db 0
lg_q:       db 0
lg_at:      db 0
lg_n:       db 0
lg_i:       db 0
bk_i:       db 0
bk_n:       db 0
bk_c:       db 0
bk_ln:      db 0
bk_wp:      dw 0
par_sel:    ds 3            ; option chosen, per choice
par_d:      db 0            ; the record's change to his patience
pa_r:       db 0
pa_s:       db 0
pa_i:       db 0
pa_m:       db 0
pa_n:       db 0
pa_bit:     db 0
pa_sm:      db 0
pa_rm:      db 0
cdl:        db 0            ; the candle: units left this night
cdl_buf:    ds 32           ; its column of pixels, top to bottom
abuf:                       ; colours of a screen being drawn (veil); the
        INCLUDE "boot.asm"  ; boot stub sits here: it runs once, before
        ds 768-($-abuf)     ; abuf is first used
