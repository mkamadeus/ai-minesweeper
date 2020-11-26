(deftemplate number
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
)

(deffunction isvalid(?r ?c)
  (return (and(>= ?r 0) (>= ?c 0) (< ?r ?*rsize*) (< ?c ?*csize*)))
)

(defrule markbomb
  (number (r ?r) (c ?c) (n ?num))
  (number (r ?i) (c ?j) (n ?))
=>
  (bind ?count 0)
  (loop-for-count (?i (- ?r 1) (+ ?r 1)) do
    (loop-for-count (?j (- ?c 1) (+ ?c 1)) do
      (if (and 
        (isvalid ?i ?j) 
        (not (and (eq ?i ?r) (eq ?j ?c)))
      ) then
        (bind ?count (+ ?count 1))
      )
    )
  )
  (assert (punten ?r ?c ?count))
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

