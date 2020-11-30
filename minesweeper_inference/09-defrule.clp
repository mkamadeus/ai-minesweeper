(defrule marksafe
  (number (r ?r) (c ?c) (n ?num))
  (bombaround ?r ?c ?num)
  (test (> ?num 0))
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