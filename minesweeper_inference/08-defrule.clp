(defrule unmarkbomb
  ?f <- (bomb (r ?r) (c ?c))
  (number (r ?r) (c ?c) (n ?))
=>
  (retract ?f)
)