(deftemplate number
  (slot r)
  (slot c)
  (slot n)
)
(deftemplate empty
  (slot r)
  (slot c)
  (slot n)
)

(defglobal 
  ?*rsize* = 4
  ?*csize* = 4
)

(deffacts initial-states
  (number (r 0) (c 0) (n 0))
  (number (r 0) (c 1) (n 0))
  (number (r 0) (c 2) (n 0))
  (number (r 0) (c 3) (n 0))
  (number (r 1) (c 0) (n 0))
  (number (r 1) (c 1) (n 1))
  (number (r 1) (c 2) (n 1))
  (number (r 1) (c 3) (n 1))
  (number (r 2) (c 0) (n 0))
  (number (r 2) (c 1) (n 1))
  (number (r 3) (c 0) (n 0))
  (number (r 3) (c 1) (n 1))
  (empty (r 0) (c 0) (n 0))
  (empty (r 0) (c 1) (n 0))
  (empty (r 0) (c 2) (n 0))
  (empty (r 0) (c 3) (n 0))
  (empty (r 1) (c 0) (n 0))
  (empty (r 1) (c 1) (n 1))
  (empty (r 1) (c 2) (n 2))
  (empty (r 1) (c 3) (n 2))
  (empty (r 2) (c 0) (n 0))
  (empty (r 2) (c 1) (n 2))
  (empty (r 2) (c 0) (n 0))
  (empty (r 3) (c 3) (n 2))
)

(deffunction isvalid(?r ?c)
  (return (and(>= ?r 0) (>= ?c 0) (< ?r ?*rsize*) (< ?c ?*csize*)))
)

(defrule markbomb
  (number (r ?r) (c ?c) (n ?num))
  (empty (r ?r) (c ?c) (n ?num))
=>
  (loop-for-count (?i (- ?r 1) (+ ?r 1)) do
    (loop-for-count (?j (- ?c 1) (+ ?c 1)) do
      (if (and 
        (isvalid ?i ?j) 
        (not (and (eq ?i ?r) (eq ?j ?c)))
      ) then
        (assert (bomb ?i ?j))
      )
    )
  )
)

(defrule unmarkbomb
  ?f <- (bomb ?r ?c)
  (number (r ?r) (c ?c) (n ?))
=>
  (retract ?f)
)

; (deffunction bombcount (?r ?c)
;   (bind ?ar (?r-1))
;   (bind ?br (?r+1))
;   (bind ?ac (?c-1))
;   (bind ?bc (?c+1))
;   (return 
;     (length$ (find-all-facts ((?f number))
;       (
;         (!= ?ar ?f:r)
;       )
      
;     ))
;   )
; )

; (defrule markbomb
;   (xpositions $? ?ax ?x ?bx $?)
;   (ypositions $? ?ay ?y ?by $?)
;   (observations (number ?cx ?cy ?num))
;   (eq (bombcount ?ax ?bx ?cx ?cy) ?num)
; =>
;   (loop-for-count (?i ?ax ?bx) do
;     (loop-for-count (?j ?ay ?by) do
;       (or (!= ?i ?x) (!= ?j ?y))
;       (if (not (exists (bomb ?i ?j) (number ?i ?j)))
;         then
;         (assert (bomb ?x ?y))
;       )
;     )
;   )
; )

; (deffacts initial-states
;   (number (r 0) (c 0) (n 0))
; )

; (defrule test
;   ?f <- (number (r ?x) (c ?y) (n ?num))
; =>
;   (retract ?f)
;   (assert (punten 123123123))
; )