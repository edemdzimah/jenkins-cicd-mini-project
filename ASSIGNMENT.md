# Assignment: Your First Jenkins Pipeline

**Due: 2026-06-14 by 11:59 PM**

Follow the `README.md` to build and run the pipeline, then complete the tasks below and submit the evidence listed.

## What to do

1. Get the project running in your own GitHub repo and create the Jenkins pipeline job from SCM (README Steps 0 to 3).
2. Run the pipeline until you get one fully green build that produces a Docker image (Step 4).
3. Complete Exercise 1: break a test on purpose, run the pipeline, then fix it.
4. Complete Exercise 2: add a `subtract` function and a `/subtract/<int:a>/<int:b>` route with a passing test.

## What to submit

Submit the following by the deadline:

1. The link to your GitHub repository.
2. A screenshot of a green pipeline run showing all four stages passing (`Checkout`, `Build`, `Test`, `Docker Build`).
3. A screenshot from Exercise 1 showing the `Test` stage failed (red) and `Docker Build` did not run, plus a screenshot of the green run after you fixed it.
4. A screenshot from Exercise 2 showing the pipeline passing with your new `subtract` test visible in the test results.

## Bonus (optional)

5. Complete Exercise 3: add a `Lint` stage using `flake8` between `Build` and `Test`, and include a screenshot of it passing.

## Grading (100 points)

- Repo set up and pipeline job configured from SCM: 20
- First fully green build producing a Docker image: 30
- Exercise 1 evidence (red `Test`, skipped `Docker Build`, then fixed): 25
- Exercise 2 evidence (new feature and passing test): 25
- Bonus, Exercise 3 `Lint` stage passing: up to 10

## How to submit

Reply to the assignment email with your repository link and the screenshots attached.
