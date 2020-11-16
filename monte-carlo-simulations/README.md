# Monte Carlo Dice

## Monte Carlo Simulations for Dice-Related Events

This folder contains some materials for a [Python workshop](https://mathspp.com/workshops) I gave.

The focus of this particular workshop was on recursive programming,
among other things,
and that is why you'll see many functions written recursively.

The code written tries to answer the question

 > "On average, how many dice do I have to roll until some rolls add up to 10?"

but the code is factored in a generic way, so that it can answer any question of the form

 > "On average, how many times do I have to do a specific thing until some condition about the outcomes is met?"

For that matter, we abstract away the several components to create:

 - predicate functions, that accept a history of outcomes and determine if the condition is satisfied or not;
 - `Experiment` objects, that
   - define a `.trial()` method that performs a single trial and returns an outcome;
 - the `MCSimulation` object,
   - that accepts an `Experiment` object and a predicate function
   - and provides a `.estimate_average_length(runs)` method that estimates the average number of times `.trial()` has
to be called before the predicate is verified.