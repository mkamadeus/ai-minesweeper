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

(deftemplate bomb
  (slot r)
  (slot c)
)

(defglobal
  ?*rsize* = 7
  ?*csize* = 7
)

(deffacts initial-states
  (number (r 0) (c 0) (n 0))
  (number (r 0) (c 1) (n 0))
  (number (r 0) (c 2) (n 0))
  (number (r 0) (c 3) (n 1))
  (number (r 1) (c 0) (n 0))
  (number (r 1) (c 1) (n 0))
  (number (r 1) (c 2) (n 1))
  (number (r 1) (c 3) (n 2))
  (number (r 2) (c 0) (n 0))
  (number (r 2) (c 1) (n 0))
  (number (r 2) (c 2) (n 1))
  (number (r 3) (c 0) (n 0))
  (number (r 3) (c 1) (n 0))
  (number (r 3) (c 2) (n 1))
  (number (r 3) (c 3) (n 1))
  (number (r 3) (c 4) (n 2))
  (number (r 4) (c 0) (n 0))
  (number (r 4) (c 1) (n 0))
  (number (r 4) (c 2) (n 0))
  (number (r 4) (c 3) (n 0))
  (number (r 4) (c 4) (n 1))
  (number (r 5) (c 0) (n 0))
  (number (r 5) (c 1) (n 0))
  (number (r 5) (c 2) (n 0))
  (number (r 5) (c 3) (n 0))
  (number (r 5) (c 4) (n 1))
  (number (r 6) (c 0) (n 0))
  (number (r 6) (c 1) (n 0))
  (number (r 6) (c 2) (n 0))
  (number (r 6) (c 3) (n 0))
  (number (r 6) (c 4) (n 1))

  (unknown (r 0) (c 3) (n 2))
  (unknown (r 1) (c 2) (n 1))
  (unknown (r 1) (c 3) (n 4))
  (unknown (r 2) (c 2) (n 1))
  (unknown (r 3) (c 2) (n 1))
  (unknown (r 3) (c 3) (n 2))
  (unknown (r 3) (c 4) (n 5))
  (unknown (r 4) (c 4) (n 3))
  (unknown (r 5) (c 4) (n 3))
  (unknown (r 6) (c 4) (n 2))

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
        (assert (bomb (r ?i) (c ?j)))
      )
    )
  )
)

(defrule countbombaround
  (number (r ?r) (c ?c) (n ?num))
=>
  (if (!= ?num 0) then
    (bind ?count (length$ (find-all-facts ((?f bomb)) (isaround ?r ?c ?f:r ?f:c) )))
    (printout t ?count " " ?r " " ?c crlf)
    (if (!= ?count 0) then
      (assert (bombaround ?r ?c ?count))
    )
  )
)

(defrule unmarkbomb
  ?f <- (bomb (r ?r) (c ?c))
  (number (r ?r) (c ?c) (n ?))
=>
  (retract ?f)
)

(defrule marksafe
  (number (r ?r) (c ?c) (n ?num))
  (bombaround ?r ?c ?num)
=>
  (loop-for-count (?i (- ?r 1) (+ ?r 1)) do
    (loop-for-count (?j (- ?c 1) (+ ?c 1)) do
      (if (and 
        (isvalid ?i ?j) 
        (not (and (eq ?i ?r) (eq ?j ?c)))
      ) then
        (assert (safe ?i ?j))
      )
    )
  )
)

(defrule umarksafe
  ?f <- (safe ?r ?c)
  (
    or
    (bomb (r ?r) (c ?c))
    (number (r ?r) (c ?c) (n ?))
  )
=>
  (retract ?f)
)  