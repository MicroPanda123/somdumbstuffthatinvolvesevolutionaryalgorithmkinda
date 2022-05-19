# Learning or sumtin

## Update
I decided to document this code, idk why but I am bored in class and just got access to my server, so I've got time.

## Based on
This is based on my [markov chain project](https://github.com/MicroPanda123/markov-chains-for-text-in-python-implementation), model_generator is from there, so you can see it's documentation there.

## Preamble
Main part of model_user is also the same as in my [markov chain project](https://github.com/MicroPanda123/markov-chains-for-text-in-python-implementation), but I've added "evolution" algorithm to it, because I wanted to make word generation based on probability sum (higher = better, this is getbest function), but it made an issue that it almost always returned single worded sentences, because they always had prob of 1, I didn't wanted to make them impossible, so I wanted a way to determine what probability should single worded sentences have so that they wouldn't be impossible, but also wouldn't be too often. So there it is, TheMyOwnEvolutionKindaAlgorithmThatIsDumbButItWasFunToMadeSoILikeIt® (not an actual trademark).

## Student class
There is class called student (Hehe, class called student, it's funny), it stores 3 pieces of data: student's setting, student's score and student's iteration. 
Setting is probability to set for single worder sentences. Score is calculated score of how close student was to getting wanted ratio of single worded sentences to multi worded ones. Iteration is just in which iteration student was created.

## Simplified step by step explanation of learning algorithm
1. Selected amount of students is genereted in a list, since this is first iteration student's have random[^1] settings. Iteration is set 0.
2. Function test_student for each student is called.
3. Function test_student measures performance of each student by:
- Uses getbest function with student.
- Checks length of returned sentence.
- If sentence is single worded, it adds 1 to int ones.
- Gets ratio of iterations by dividing ones by total number of iterations.
- Repeat steps from 3.1 to 3.4 until reached iterations specified in testing_steps variable.
- Calculate student's score by forumla 
```
if expected ratio is bigger than actual ratio
score = 100 / (expected - ratio)
if expected ratio is smaller than actual ratio
score = 100 / (ratio - expected)
if expected ratio is equal to actual ratio
score = 100 / (1 / testing_steps)
```
- Set student's score to calculated score
4. Compare students in student list by score.
5. Set student with best score as best_student.
6. Next iteration.
7. Selected amount of students is generated in a list, half students are randomly[^1] generated, other half is generated based on best student setting, randomly[^1] changed by selected amount (step variable). Set iteration value in student to iteration it's currently in.
8. Function test_student again is called for each student.
9. Function test_student again measures performance for each student.
10. Compare students in student list by score again.
11. Set student with best score as best_student, if there isn't student with better score than best_student then best_student stays the same.
12. Check if best_student improves:
- Compare current iteration with best_student iteration.
- If iterations are is the same, save it's values to a file, and continue.
- If iterations aren't the same, count for how long it hasn't been improved, if it didn't improved for 3 break iterations loop.
13. Repeat steps from 7 to 12 until iterations end or best_student weren't improving.
14. Save final best_student to file and return it.



[^1]: It's actually pseudorandom, since computers can't generate true random numbers.