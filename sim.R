library(heap)

set.seed(1047)

pop <- 1e4
beta <- 2

C <- 0
I <- 0

# Min-heap for events
queue <- heap("min")

# Transmission records
trans <- list(list())  # zero-th transmitter placeholder

# Push initial contact event
queue$push(list(time = 0, event = list(type = "contact", primary = 0, filter = pop)))

while (queue$size() > 0) {
	# Pop next event
	item <- queue$pop()
	time <- item$time
	ev <- item$event

	if (ev$type == "contact") {
		# Is target still susceptible?
		S <- pop - C
		if (runif(1) < S / ev$filter) {
			C <- C + 1
			I <- I + 1

			# Create new infector and pre-calculate events
			trans[[length(trans) + 1]] <- list(`in` = time, out = c())
			Re <- beta * S / pop
			pInf <- Re / (Re + 1)
			delta <- 1 / (Re + 1)
			next <- ifelse(runif(1) < pInf, "contact", "recover")
			time <- time + delta * rexp(1, rate = 1)

			while (next == "contact") {
				queue$push(list(time = time, event = list(type = "contact", primary = C, filter = S)))
				trans[[C]]$out <- c(trans[[C]]$out, time)
				next <- ifelse(runif(1) < pInf, "contact", "recover")
				time <- time + delta * rexp(1, rate = 1)
			}

			queue$push(list(time = time, event = list(type = "recover", focus = ev$primary)))
			trans[[C]]$recover <- time
		}
	} else if (ev$type == "recover") {
		I <- I - 1
	}
}

