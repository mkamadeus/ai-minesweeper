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