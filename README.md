# Drone-delivery
## Introduction
In this exercise, you assume the role of a head of a drone delivery agency. Your main goal is to
deliver the packages to your clients in the shortest time possible. To achieve this most efficiently,
you must make use of the search algorithms shown in class, with the first task being modeling
the problem precisely.

## Environment
The environment is a rectangular grid - given as a list of lists (exact representation can be found
in the “Input” section). Each point on a grid represents an area. An area can be either passable
or impassable for the delivery drones. Moreover, there are packages lying in different locations
around the grid. The packages can be picked up by drones and delivered to clients.
Clients can move on a pre-determined and known path, and each client has a list of required
packages. In general, the client can request non-existing packages (then the problem is
unsolvable). Moreover, there could be packages that no one needs. One drone can carry up to
two packages at once.
The task is done in timestamps (or turns), so the environment changes only after you apply an
action.
