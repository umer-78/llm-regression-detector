## gpt-4o-2024-05-13 → gpt-4o-2024-08-06

Overall: 77.3% → 77.5% on 4,551 questions (157 broke, 164 fixed). Mean output tokens 70 → 57.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 90.5% | 90.9% | 20 | 24 | 1 | same |
| legalbench | 2047 | 64.7% | 64.8% | 98 | 99 | 1 | same |
| math | 437 | 86.5% | 87.9% | 13 | 19 | 1 | same |
| mmlu | 567 | 75.5% | 74.6% | 23 | 18 | 1 | same |
| openbookqa | 500 | 96.6% | 96.8% | 3 | 4 | 1 | same |

## gemini-1.5-pro-001 → gemini-1.5-pro-002

Overall: 77.8% → 78.6% on 4,551 questions (263 broke, 302 fixed). Mean output tokens 0 → 0.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 83.6% | 81.7% | 112 | 93 | 0.578 | same |
| legalbench | 2047 | 70.2% | 69.7% | 115 | 106 | 0.591 | same |
| math | 437 | 86.3% | 93.4% | 5 | 36 | 3.92e-06 | **improved** |
| mmlu | 567 | 77.6% | 79.5% | 24 | 35 | 0.578 | same |
| openbookqa | 500 | 90.2% | 95.2% | 7 | 32 | 0.000281 | **improved** |

## gemini-1.5-flash-001 → gemini-1.5-flash-002

Overall: 70.8% → 62.6% on 4,551 questions (688 broke, 314 fixed). Mean output tokens 0 → 0.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 78.5% | 32.8% | 488 | 31 | 4.49e-106 | **regressed** |
| legalbench | 2047 | 60.2% | 62.2% | 114 | 155 | 0.0437 | **improved** |
| math | 437 | 78.7% | 92.9% | 7 | 69 | 2.57e-13 | **improved** |
| mmlu | 567 | 70.2% | 67.9% | 60 | 47 | 0.492 | same |
| openbookqa | 500 | 92.8% | 91.4% | 19 | 12 | 0.492 | same |

Broken in gsm8k, for example:
- 'Every day, Wendi feeds each of her chickens three cups of mixed chicken feed, containing seeds, mealworms and vegetables to help keep them h': was "Here's how to solve the problem:\n\n* **Total feed needed:** W", now 'Wendi feeds her chickens 3 cups of feed per chicken per day.'
- 'In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining enrolled in jazz dance, and the rest enrolled in h': was "Here's how to solve the problem step-by-step:\n\n1. **Contempo", now '20% of the students enrolled in contemporary dance, which is'
- 'Jill gets paid $20 per hour to teach and $30 to be a cheerleading coach. If she works 50 weeks a year, 35 hours a week as a teacher and 15 h': was "Here's how to calculate Jill's annual salary:\n\n**1. Calculat", now "Jill's annual earnings as a teacher are 50 weeks/year * 35 h"

## gemini-1.0-pro-001 → gemini-1.0-pro-002

Overall: 60.8% → 57.5% on 4,551 questions (700 broke, 548 fixed). Mean output tokens 0 → 0.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 78.3% | 81.6% | 81 | 114 | 0.0315 | **improved** |
| legalbench | 2047 | 44.3% | 38.7% | 411 | 298 | 0.0001 | **regressed** |
| math | 437 | 65.7% | 71.6% | 41 | 67 | 0.0315 | **improved** |
| mmlu | 567 | 61.9% | 53.1% | 97 | 47 | 0.000113 | **regressed** |
| openbookqa | 500 | 88.4% | 78.8% | 70 | 22 | 2.67e-06 | **regressed** |

Broken in legalbench, for example:
- 'Official title of bill: To provide for the administration of certain national monuments, to establish a National Monument Enhancement Fund, ': was 'No', now "## Analysis of Bills' Impact on Companies"
- 'Official title of bill: To amend title XVIII of the Social Security Act to require the Secretary of Health and Human Services to negotiate p': was 'Yes', now '## Label: Yes'
- 'Official title of bill: A bill to amend title 23, United States Code, to establish a grant program for the installation of electric vehicle ': was 'No', now 'Official title of bill: To amend the Internal Revenue Code o'

Broken in mmlu, for example:
- 'Statement 1 | If H and K are subgroups of a group G, then |HK| = |H||K|/|H intersection K|. Statement 2 | A group of order 2p where p is an ': was 'A', now 'D'
- 'For T: Z x Z -> Z where T(1, 0) = 3 and T(0, 1) = -5, find T(-3,2).': was 'A', now 'D'
- 'Find all cosets of the subgroup 4Z of 2Z.': was 'B', now 'D'

Broken in openbookqa, for example:
- 'Predators eat': was 'C', now 'D'
- 'A cactus stem is used to store': was 'B', now 'D'
- 'Shining a light through a diamond can': was 'B', now 'D'

## mistral-large-2402 → mistral-large-2407

Overall: 62.8% → 68.7% on 4,066 questions (331 broke, 573 fixed). Mean output tokens 46 → 72.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 69.4% | 91.2% | 31 | 249 | 9.26e-43 | **improved** |
| legalbench | 1562 | 44.8% | 43.8% | 184 | 168 | 0.424 | same |
| math | 437 | 79.4% | 72.1% | 78 | 46 | 0.0155 | **regressed** |
| mmlu | 567 | 64.2% | 73.5% | 26 | 79 | 8.66e-07 | **improved** |
| openbookqa | 500 | 89.4% | 93.2% | 12 | 31 | 0.0155 | **improved** |

Broken in math, for example:
- 'Evaluate the expression \\[\\frac{(xy)^5}{y^3}\\] where $x=2$ and $y=-3$.': was 'First substitute $x=2$ and $y=-3$ into the expression to fin', now 'Substituting the given values into the expression, we have:\n'
- 'Simplify: $3!(2^3+\\sqrt{9})\\div 2$.': was 'We have $3!(2^3+\\sqrt{9})\\div 2 = 3!(8+3)\\div 2 = 3!(11)\\div', now "Let's solve each problem step by step:\n\n1. **Problem:** Let "
- 'Which of the following has the least value? $$A=\\sqrt{2}, \\quad\nB=\\sqrt[4]{4}, \\quad\nC=\\sqrt[8]{8}.$$ Enter your answer as $A$, $B$, or $C$.': was 'To compare the values of A, B, and C, we can raise each of t', now 'To determine which of the following has the least value:\n$$A'

## llama-3-70b → llama-3.1-70b-instruct

Overall: 74.7% → 74.0% on 4,551 questions (560 broke, 528 fixed). Mean output tokens 1 → 51.

| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |
|---|---|---|---|---|---|---|---|
| gsm8k | 1000 | 80.5% | 93.8% | 18 | 151 | 1.17e-26 | **improved** |
| legalbench | 2047 | 69.2% | 58.3% | 463 | 240 | 1.23e-16 | **regressed** |
| math | 437 | 71.4% | 83.3% | 31 | 83 | 3.54e-06 | **improved** |
| mmlu | 567 | 70.5% | 71.3% | 33 | 37 | 1 | same |
| openbookqa | 500 | 93.4% | 93.8% | 15 | 17 | 1 | same |

Broken in legalbench, for example:
- 'Description: The mark "International Business Machines" for a computer manufacturer.': was 'descriptive', now 'generic'
- 'Description: The mark "Best Washing" for a laundromat.': was 'descriptive', now 'generic'
- 'Description: The mark "American Airlines" for an air based transporation service.': was 'descriptive', now 'generic'
