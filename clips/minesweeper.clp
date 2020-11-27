(deftemplate number
  (slot r)
  (slot c)
  (slot n)
)
(deftemplate unknown
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
  (unknown (r 1) (c 1) (n 1))
  (unknown (r 1) (c 2) (n 2))
  (unknown (r 1) (c 3) (n 2))
  (unknown (r 2) (c 1) (n 2))
  (unknown (r 3) (c 1) (n 2))
)

(deffunction isvalid(?r ?c)
  (return (and(>= ?r 0) (>= ?c 0) (< ?r ?*rsize*) (< ?c ?*csize*)))
)

; ([r-1..r+1], [c-1..c+1])
(deffunction isaround(?r ?c ?br ?bc)
  (return (and (and (>= ?br (- ?r 1)) (<= ?br (+ ?r 1))) (and (>= ?bc (- ?c 1)) (<= ?bc (+ ?c 1)))))
)

(defrule markbomb
  (number (r ?r) (c ?c) (n ?num))
  (unknown (r ?r) (c ?c) (n ?num))
  (test (> ?num 0))
=>
  (loop-for-count (?i (- ?r 1) (+ ?r 1)) do
    (loop-for-count (?j (- ?c 1) (+ ?c 1)) do
      (if (and 
        (isvalid ?i ?j) 
        (not (and (eq ?i ?r) (eq ?j ?c)))
      ) then
        (printout t ?i " " ?j crlf)
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

(defrule updateunknown
  ?f <- (unknown (r ?r) (c ?c) (n ?num))
  (bomb ?br ?bc)
  (not (checked ?r ?c))
=>
  (if (isaround ?br ?bc ?r ?c) then 
    (retract ?f)
    (bind ?newnum (- ?num 1))
    (if (> ?newnum 0) then
      (assert (unknown (r ?r) (c ?c) (n ?newnum)))
      (assert (checked ?r ?c))
    )
  )
)
