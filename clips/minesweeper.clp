(deftemplate number
  (slot r)
  (slot c)
  (slot n)
)

(deffacts initial-states
  (rpositions nil 0 1 2 3 nil)
  (cpositions nil 0 1 2 3 nil)
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

; (do-for-all-facts ((?f number)) ()
;   (printout t ?f:r ?f:c)
; )
; (deffunction bombcount (?r ?c)
;   (bind ?count 0)
;   (return exists (number (r ?r) (c ?c)))
; )

(defrule checknumber
  (number (r 0) (c 0))
  =>
  (printout t "ada woi" crlf)
)

(defrule mark-bomb
  (new-xpositions $? ?ax ?x ?bx $?)
  (new-ypositions $? ?ay ?y ?by $?)
  (number ?x ?y ?num)
=>
  (loop-for-count (?i ?ax ?bx) do
    (loop-for-count (?j ?ay ?by) do
      (or (!= ?i ?x) (!= ?j ?y))
        (if (not (exists (bomb ?i ?j) (number ?i ?j)))
          then
        (assert (bomb ?x ?y))
        )
    )
  )
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

