from load import *

# for u, i in enumerate(out):
#     print(u,"=>",i)

# 0 => Sometimes, it’s easy for a computer to predict the future
# 1 =>  Simple phenomena, such as how sap flows down a tree trunk, are straightforward and can be captured in a few lines of code using what mathematicians call linear differential equations
# 2 =>  But in nonlinear systems, interactions can affect themselves: When air streams past a jet’s wings, the air flow alters molecular interactions, which alter the air flow, and so on
# 3 =>  This feedback loop breeds chaos, where small changes in initial conditions lead to wildly different behavior later, making predictions nearly impossible — no matter how powerful the computer
# 4 => \n\n“This is part of why it’s difficult to predict the weather or understand complicated fluid flow,” said Andrew Childs, a quantum information researcher at the University of Maryland
# 5 =>  “There are hard computational problems that you could solve, if you could [figure out] these nonlinear dynamics
# 6 => ”\n\nThat may soon be possible
# 7 =>  In separate studies posted in November, two teams — one led by Childs, the other based at the Massachusetts Institute of Technology — described powerful tools that would allow quantum computers to better model nonlinear dynamics
# 8 => \n\nQuantum computers take advantage of quantum phenomena to perform certain calculations more efficiently than their classical counterparts
# 9 =>  Thanks to these abilities, they can already topple complex linear differential equations exponentially faster than classical machines
# 10 =>  Researchers have long hoped they could similarly tame nonlinear problems with clever quantum algorithms
# 11 => \n\nThe new approaches disguise that nonlinearity as a more digestible set of linear approximations, though their exact methods vary considerably
# 12 =>  As a result, researchers now have two separate ways of approaching nonlinear problems with quantum computers
# 13 => \n\n“What is interesting about these two papers is that they found a regime where, given some assumptions, they have an algorithm that is efficient,” said Mária Kieferová, a quantum computing researcher at the University of Technology Sydney who is not affiliated with either study
# 14 =>  “This is really exciting, and [both studies] use really nice techniques
# 15 => ”\n\nQuantum information researchers have tried to use linear equations as a key to unlock nonlinear differential ones for over a decade
# 16 =>  One breakthrough came in 2010, when Dominic Berry, now at Macquarie University in Sydney, built the first algorithm for solving linear differential equations exponentially faster on quantum, rather than on classical, computers
# 17 =>  Soon, Berry’s own focus shifted to nonlinear differential equations as well
# 18 => \n\n“We had done some work on that before,” Berry said
# 19 =>  “But it was very, very inefficient
# 20 => ”\n\nThe problem is, the physics underlying quantum computers is itself fundamentally linear
# 21 =>  “It’s like teaching a car to fly,” said Bobak Kiani, a co-author of the MIT study
# 22 => \n\nSo the trick is finding a way to mathematically convert a nonlinear system into a linear one
# 23 =>  “We want to have some linear system because that’s what our toolbox has in it,” Childs said
# 24 =>  The groups did this in two different ways
# 25 => \n\nChilds’ team used Carleman linearization, an out-of-fashion mathematical technique from the 1930s, to transform nonlinear problems into an array of linear equations
# 26 => \n\nUnfortunately, that list of equations is infinite
# 27 =>  Researchers have to figure where they can cut off the list to get a good-enough approximation
# 28 =>  “Do I stop at equation number 10
# 29 =>  Number 20
# 30 => ” said Nuno Loureiro, a plasma physicist at MIT and a co-author of the Maryland study
# 31 =>  “Do I stop at equation number 10
# 32 =>  Number 20
# 33 => ” said Nuno Loureiro, a plasma physicist at MIT and a co-author of the Maryland study
# 34 =>  The team proved that for a particular range of nonlinearity, their method could truncate that infinite list and solve the equations
# 35 => \n\nThe MIT-led paper took a different approach
# 36 =>  It modeled any nonlinear problem as a Bose-Einstein condensate
# 37 =>  This is a state of matter where interactions within an ultracold group of p

