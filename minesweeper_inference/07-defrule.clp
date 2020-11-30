(defrule countbombaround
  (number (r ?r) (c ?c) (n ?num))
=>
  (if (!= ?num 0) then
    (bind ?count (length$ (find-all-facts ((?f bomb)) (isaround ?r ?c ?f:r ?f:c) )))
    (if (!= ?count 0) then
      (assert (bombaround ?r ?c ?count))
    )
  )
)