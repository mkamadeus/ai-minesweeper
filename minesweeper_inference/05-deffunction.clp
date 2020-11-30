(deffunction isaround(?r ?c ?br ?bc)
  (return (and (and (>= ?br (- ?r 1)) (<= ?br (+ ?r 1))) (and (>= ?bc (- ?c 1)) (<= ?bc (+ ?c 1)))))
)