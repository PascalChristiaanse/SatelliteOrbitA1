 	   AE4872 (2024) – SATELLITE ORBIT DETERMINATION


 Assignment 1 – Dynamics

Instructor: 	Dr. Christian Siemes
Email: 	C.Siemes@tudelft.nl 
Group size:	1-2 students
Due:	Wednesday, 4 December 2024, 18:00
Page limit: 	2 pages
Estimated time:	6 hours


In your report, explain how you solve the tasks and use figures where appropriate. Describe the intermediate steps and give the intermediate results so we may award partial points (no intermediate results = no full score). Attach your code in the appendix of your report. We will check the code for plagiarism but not grade it.

This assignment is not graded. We use it to give you feedback before the grading starts.

In this assignment, you will evaluate the acceleration due to several sources and quantify the effect on the integrated orbit. You will use the CHAMP satellite as a test case. You are provided with the precise orbit for one day in September 2010 when the altitude was about 250 km. Use the parameters specified on the instruction slides and know that the precise orbit has an accuracy of a few cm in position and a few mm/s in velocity.

a) Calculate the acceleration due to the following effects:
i)	Centrifugal and Coriolis effects due to frame rotation
ii)	Earth’s flattening (C20 gravity field coefficient)
iii)	Atmospheric drag
Report the accelerations for the first epoch and briefly discuss them.

b) Use the first position and velocity of the precise orbit as the initial state and integrate the CHAMP orbit using four different dynamical models:
i)	No perturbing forces and ignore the frame rotation
ii)	No perturbing forces and account for the frame rotation
iii)	Account for Earth’s flattening and the frame rotation, but not atmospheric drag
iv)	Account for Earth’s flattening, the frame rotation, and atmospheric drag

•	Show the error of the integrated orbits in a figure. Describe qualitatively how the position and velocity errors evolve over time. (‘qualitatively’ means that you do not have to state values)
•	Report the position error at the last epoch and explain if you expect this error size based on the acceleration reported in task (a). Support your answer with a simplified estimation of the error size.
•	When accounting for Earth’s flattening, the frame rotation, and atmospheric drag, what causes the remaining position errors, and which is likely the dominating error source? Justify your answer.

Please mention how many hours you spent approximately on the assignment. We will use the information to improve the assignments for next year.

