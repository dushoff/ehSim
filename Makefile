## This is ehSim; developing new simulations for emergent heterogeneity
## 2025 Nov 27 (Thu)

current: target
-include target.mk
Ignore = target.mk

vim_session:
	bash -cl "vmt"

-include makestuff/python.def

######################################################################

Sources += $(wildcard *.R)

autopipeR = defined

## Not really tried; I think python will be much more efficient.
## But worth testing this
sim.Rout: sim.R

######################################################################

Sources += $(wildcard *.py *.md)
Ignore += *.out

sim.out: sim.py
	$(PITH)

nofilter.out: nofilter.py
	$(PITH)

######################################################################

### Makestuff

Sources += Makefile

Ignore += makestuff
msrepo = https://github.com/dushoff

## ln -s ../makestuff . ## Do this first if you want a linked makestuff
Makefile: makestuff/00.stamp
makestuff/%.stamp: | makestuff
	- $(RM) makestuff/*.stamp
	cd makestuff && $(MAKE) pull
	touch $@
makestuff:
	git clone --depth 1 $(msrepo)/makestuff

-include makestuff/os.mk

-include makestuff/pipeR.mk

-include makestuff/git.mk
-include makestuff/visual.mk
