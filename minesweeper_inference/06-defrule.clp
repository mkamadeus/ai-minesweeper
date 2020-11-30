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