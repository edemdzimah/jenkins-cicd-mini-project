# CI/CD Mini Project: Your First Jenkins Pipeline

A hands-on starter project for learning Continuous Integration and Continuous Delivery with Jenkins. You will run Jenkins yourself, point it at a small Python web app, and build a pipeline that automatically installs dependencies, runs tests, and packages the app into a Docker image.

By the end you will understand what a pipeline actually does, because you will have built one that works.

## Part 0: Read this first (the concepts)

If the words below are new to you, read this section once before touching anything. Five minutes here saves an hour of confusion later. See `pipeline-diagram.svg` for a picture of the whole loop.

### What is CI/CD?

CI/CD is a way of working where, every time you change your code, a set of checks and steps runs automatically to confirm the change is safe and ready to ship.

- **CI (Continuous Integration):** every time you push code, it is automatically built and tested. If you broke something, you find out in minutes, not days.
- **CD (Continuous Delivery):** once the code passes, it is automatically packaged and made ready to release.

The plain idea: a tireless assistant that, every time you change your code, runs the same checks a careful engineer would run by hand, every single time, without ever forgetting a step.

### What is Jenkins?

Jenkins is that assistant. It is a free, open-source automation server. You give it your code and a list of steps, and it runs those steps for you, whenever you ask or whenever your code changes. In this project you run your own Jenkins on your machine using Docker.

### What is a pipeline?

A pipeline is the ordered list of steps Jenkins runs. Each step is called a **stage**. This project has four stages: get the code, install dependencies, run the tests, build a Docker image. If any stage fails, the pipeline stops, so a broken change never moves forward.

### What is a Jenkinsfile?

A `Jenkinsfile` is a plain text file that holds your pipeline written as code. It lives in your repository, right next to your app. Instead of clicking buttons inside Jenkins to define the steps, you write them once in the `Jenkinsfile` and Jenkins reads it. That means your pipeline is version-controlled and shared with the whole team, exactly like your source code.

### How they fit together

You push code to GitHub. Jenkins notices, reads the `Jenkinsfile` from your repo, and runs each stage in order. You watch it pass or fail in your browser. That single loop is the entire thing you are about to build.

## Learning objectives

After completing this project you will be able to:

1. Explain what CI/CD is and why teams use it.
2. Run a Jenkins server locally using Docker.
3. Read and understand a declarative `Jenkinsfile`.
4. Create a Jenkins pipeline job that pulls code from a Git repository.
5. Trace a build through four stages: `Checkout`, `Build`, `Test`, `Docker Build`.
6. Diagnose a failing pipeline by reading the console output.

## The core idea

A pipeline is just automation of the steps you would otherwise run by hand every time you change your code:

| You would normally type | The pipeline stage that does it |
| --- | --- |
| `git pull` | `Checkout` |
| `pip install -r requirements.txt` | `Build` |
| `pytest` | `Test` |
| `docker build` | `Docker Build` |

Jenkins runs these steps for you, the same way every time, and tells you immediately if something breaks. That is the whole value: fast, repeatable feedback.

## Prerequisites

- Docker and Docker Compose installed (Docker Desktop on macOS or Windows, Docker Engine on Linux).
- A free GitHub account.
- Basic command line comfort.
- About 60 to 90 minutes.

## Project structure

```
jenkins-cicd-mini-project/
├── app/
│   ├── app.py             # The Flask web app
│   ├── test_app.py        # Unit tests (run by the pipeline)
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # How to package the app into an image
├── Jenkinsfile            # The pipeline definition (the heart of this project)
├── jenkins/
│   ├── Dockerfile         # Custom Jenkins image with Python + Docker CLI
│   └── docker-compose.yml # Starts Jenkins and a Docker daemon
└── README.md              # This file
```

## Step 0: Put this project on GitHub

Jenkins pulls your code from a Git repository, so the project needs to live on GitHub.

1. Create a new public repository on GitHub, for example `jenkins-cicd-mini-project`.
2. From inside this project folder, run:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: CI/CD mini project"
   git branch -M main
   git remote add origin https://github.com/<your-username>/jenkins-cicd-mini-project.git
   git push -u origin main
   ```

Keep the repository URL handy. You will paste it into Jenkins later.

## Step 1: Run the app and tests on your own machine first

Before automating anything, do it manually once so you know what the pipeline is automating.

```bash
cd app
python3 -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

You should see four passing tests. You can also run the app directly with `python app.py` and open `http://localhost:5000` in a browser.

This is the manual version of what Jenkins will soon do for you.

## Step 2: Start Jenkins

From the `jenkins/` folder, start the stack:

```bash
cd jenkins
docker compose up -d --build
```

The first build takes a few minutes because it downloads images and installs tools. When it finishes, get the one-time unlock password:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Now open `http://localhost:8080` in your browser.

1. Paste the unlock password.
2. Choose **Install suggested plugins** and wait for it to finish.
3. Create your admin user (remember the username and password).
4. Accept the default Jenkins URL and finish setup.

## Step 3: Create the pipeline job

1. On the Jenkins dashboard, click **New Item**.
2. Enter a name like `cicd-mini-project`, select **Pipeline**, click **OK**.
3. Scroll down to the **Pipeline** section.
4. Set **Definition** to **Pipeline script from SCM**.
5. Set **SCM** to **Git**.
6. Paste your GitHub repository URL in **Repository URL**.
7. Set **Branch Specifier** to `*/main`.
8. Leave **Script Path** as `Jenkinsfile`.
9. Click **Save**.

This tells Jenkins: pull the code from this repo, then run the instructions in the `Jenkinsfile`.

## Step 4: Run the pipeline

Click **Build Now**. Watch the **Stage View** appear, with one column per stage. Click on a running or finished build, then **Console Output** to read exactly what Jenkins is doing.

A green run means all four stages passed and your Docker image was built. Confirm the image exists inside the Docker daemon container:

```bash
docker exec jenkins-docker docker images | grep cicd-mini-project
```

You just ran your first CI/CD pipeline.

## Understanding the Jenkinsfile

Open `Jenkinsfile` and read it alongside this explanation.

- `agent any` tells Jenkins to run on any available worker.
- `environment { ... }` defines variables. `IMAGE_TAG` uses `BUILD_NUMBER`, so each build tags a uniquely numbered image.
- `stage('Checkout')` pulls your code with `checkout scm`.
- `stage('Build')` creates a Python virtualenv and installs dependencies, isolated from the system Python.
- `stage('Test')` runs `pytest` and writes a `test-results.xml` report that Jenkins displays in the UI.
- `stage('Docker Build')` packages the tested app into a Docker image.
- The `post` block runs after the stages and reports success or failure.

The key insight: if the `Test` stage fails, the pipeline stops and never builds a broken image. That is continuous integration protecting you.

## Exercises

Work through these in order. Each one is a small, real change.

1. **Break a test on purpose.** Change `assert add(2, 3) == 5` to `== 6` in `test_app.py`, push, and run the pipeline. Watch the `Test` stage go red and the `Docker Build` stage never run. Then fix it.
2. **Add a feature with a test.** Add a `subtract(a, b)` function and a `/subtract/<int:a>/<int:b>` route, write a test for it, push, and watch the pipeline validate your change.
3. **Add a Lint stage.** Add `flake8` to `requirements.txt` and a new `stage('Lint')` between `Build` and `Test` that runs `flake8 app.py`. Fix any style errors it reports.
4. **Trigger builds automatically.** In the job configuration, enable **Poll SCM** with the schedule `H/2 * * * *` so Jenkins checks GitHub for changes every two minutes. Push a commit and watch a build start on its own.

## Troubleshooting

- **`docker: command not found` in the pipeline.** The Jenkins image build did not finish. Run `docker compose up -d --build` again from the `jenkins/` folder.
- **Cannot reach `http://localhost:8080`.** Check the containers are up with `docker compose ps`. Give Jenkins a minute to start after `up`.
- **`Cannot connect to the Docker daemon` in the `Docker Build` stage.** The `jenkins-docker` container is not ready. Confirm both containers are running and rerun the build.
- **Test stage cannot find `pytest`.** Make sure the `Build` stage ran and succeeded first, since it installs the dependencies the `Test` stage uses.
- **Lost the admin password.** Re-read it with the `docker exec jenkins cat ...` command from Step 2, or reset everything with `docker compose down -v` and start fresh.

## Cleanup

When you are done:

```bash
cd jenkins
docker compose down        # Stops Jenkins, keeps your data
docker compose down -v     # Stops Jenkins and deletes all data for a clean reset
```

## What comes next

This pipeline stops at building the image. The natural next step is **continuous delivery**: pushing that image to a registry such as Docker Hub, then deploying it. That is the focus of the follow-up project once these four stages feel comfortable.
