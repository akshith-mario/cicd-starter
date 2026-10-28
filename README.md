# CI/CD Starter: Learn by Doing

A tiny Python API with a full **CI/CD pipeline** on GitHub Actions:
**Test → Build Docker image → Scan → Push to registry → Deploy to Kubernetes → Smoke test**

Everything runs free on GitHub. No Azure account needed to start.

---

## Part 1: The concepts (10 minutes)

**CI (Continuous Integration)** means every time someone pushes code, a machine automatically
*tests* it and *builds* it. Broken code gets caught in minutes instead of in production.

**CD (Continuous Delivery/Deployment)** means once the build passes, the machine automatically
*deploys* it to an environment (test, pre-prod, prod).

You already know the **last half** of this from work: images, registries, `kubectl apply`,
rollouts, pods. CI/CD is just **automating the steps you do by hand**.

| What you do manually today | What the pipeline does |
|---|---|
| Someone builds an image | `docker build` in the `build` job |
| Push to the registry | `docker push` to GHCR |
| `kubectl apply -f ...` | `deploy` job |
| `kubectl rollout status`, check pods | rollout + smoke test step |
| Check the image is trusted/secure | Trivy scan step |

### Key vocabulary (interviewers ask these)
- **Pipeline**: the whole automated flow, defined in a YAML file in the repo.
- **Trigger**: what starts it (push to `main`, a pull request, a schedule).
- **Job**: a group of steps that runs on one machine. Jobs can depend on each other (`needs:`).
- **Step**: one command or one reusable action.
- **Runner / agent**: the machine that executes the job (GitHub-hosted Ubuntu VM here).
- **Artifact**: the output of a build. Here, the Docker image.
- **Secret**: a password/token stored safely in the CI tool, never in code.
- **Environment + approval gate**: a rule like "prod deploy needs a manager's approval".

---

## Part 2: Run it on GitHub (30 minutes)

1. Create a free account at github.com, then create a **public** repo called `cicd-starter`.
2. Upload this whole folder (keep the hidden `.github` folder!). Easiest with git:
   ```bash
   cd cicd-starter
   git init
   git add .
   git commit -m "first pipeline"
   git branch -M main
   git remote add origin https://github.com/<your-username>/cicd-starter.git
   git push -u origin main
   ```
3. Open the repo → **Actions** tab. You'll see the pipeline running. Click into it and watch
   the three jobs go green: `test` → `build` → `deploy`.
4. Open the `deploy` job logs: you'll see `kubectl get pods` showing your 2 pods Running in
   a real Kubernetes cluster that the pipeline created.

## Part 3: Break it on purpose (the best way to learn)

1. **Fail CI:** edit `tests/test_main.py`, change `== 5` to `== 6`, push.
   The `test` job goes red and **build/deploy never run**. That's the whole point of CI.
   Fix it and push again.
2. **Ship a change:** edit the message in `app/main.py`, push. Watch the new image get a
   new tag (the commit ID) and roll out. Every deploy is traceable to a commit.
3. **Try a pull request:** create a branch, change something, open a PR.
   Only `test` and `build` run, **not deploy**. Look at the `if:` lines in the YAML to see why.
4. **Break the deployment:** change `/health` to `/healthz` in `k8s/deployment.yaml` only.
   Probes fail, `rollout status` times out, the pipeline goes red. Exactly the kind of
   issue you debug at work, now caught *before* it reaches users.
5. **Security gate:** in the Trivy step, change `exit-code: "0"` to `"1"`.
   Now a HIGH/CRITICAL vulnerability blocks the release. This ties directly to your
   container security remediation work.

## Part 4: Read the pipeline file line by line

Open `.github/workflows/pipeline.yml`. Every section is commented. Make sure you can
explain, without looking:
- why `build` has `needs: test`
- why the image tag is the commit SHA and not `latest`
- where the registry password comes from (`secrets.GITHUB_TOKEN`) and why it's not in the code
- why `deploy` has `if: github.event_name == 'push'`

## Part 5: Level up (next 2–4 weeks)

1. **Same pipeline in GitLab CI** (`.gitlab-ci.yml`): stages, jobs, `needs`, variables.
   Concepts are identical, only syntax changes.
2. **Same pipeline in Azure DevOps** (`azure-pipelines.yml`): stages/jobs/steps, service
   connections, ACR. Most Azure job posts ask for this one.
3. **Deploy to real AKS**: create a small AKS cluster (Azure free credit), uncomment the
   `deploy-aks` job, add the `AZURE_CREDENTIALS` secret, add a `production` environment
   with yourself as required reviewer = manual approval gate.
4. **Helm**: turn `k8s/deployment.yaml` into a Helm chart and deploy with `helm upgrade --install`.
5. **GitOps (Argo CD)**: pipeline updates the image tag in git; Argo CD syncs it to the cluster.

## How to talk about it honestly (CV / LinkedIn / interview)

Once you've done Parts 2–4, you can truthfully say:

> Built an end-to-end CI/CD pipeline (GitHub Actions) for a containerised Python service:
> automated tests, Docker build, Trivy image scanning, push to container registry and
> automated Kubernetes deployment with rollout verification and smoke tests.

Put it under **Projects** with the GitHub link, not under your 6D job. Interviewers can open it,
and you can walk them through every line.

## Run locally (optional)
```bash
pip install -r requirements.txt
pytest -v
docker build -t cicd-starter . && docker run -p 8080:8080 cicd-starter
# open http://localhost:8080
```
