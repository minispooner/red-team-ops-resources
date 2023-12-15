# Elastic Kubernetes Services (EKS)

## EKS Cluster Hacking Game

Fun game to learn and practice hacking kubernetes pods and clusters in an AWS environment.

<details closed>
<summary>Step 1 (spoilers!)</summary>
<br>
  list secrets: `kubectl get secrets` and `kubectl get secret SECRETNAME -o json`
</details>

<details closed>
<summary>Step 2 (spoilers!)</summary>
<br>
  Describe the pod to see the registry info (-o yaml to see more data), get the secret, docker login with creds, pull image, review docker image layers for creds
</details>

<details closed>
<summary>Step 3 (spoilers!)</summary>
<br>
  3. Use AWS keys to `aws ecr describe-repositories ...`, generate cred and pipe to docker login `aws ecr get-login-password...|docker login...`, `docker pull REGISTRY/REPO:IMAGE_ID
</details>

<details closed>
<summary>Step 4 (spoilers!)</summary>
<br>
  4. Extract cluster name from ~/.kube/config or AWS IAM role name, run `aws eks get-token --cluster-name CLUSTERNAME` to get node token, then pass into `kubectl auth can-i --list --token=k8s-aws-v1.aHR...redacted...` 
</details>

<details closed>
<summary>Step 5 (spoilers!)</summary>
<br>
  TODO
</details>

## References
- https://eksclustergames.com/
- https://medium.com/@jason133337/eks-cluster-game-challenge-walkthrough-9110343c24ce
