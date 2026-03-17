# 📝 AWS Security & Monitoring — MCQ Quiz

**Total Questions:** 15  
**Covers:** Data Protection Workshop (Labs 1–7) + Logging & Incident Response Workshop (Labs 1–6)  
**Time:** 20 minutes

---

### Q1. When you upload a file to an S3 bucket configured with SSE-KMS encryption, which KMS API call does S3 make behind the scenes?

A) `kms:Encrypt`  
B) `kms:GenerateDataKey`  
C) `kms:CreateKey`  
D) `kms:Sign`

---

### Q2. An IAM policy has the following statement. What happens when the user tries to call `s3:DeleteBucket`?

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

A) Denied — because `s3:*` only covers object-level actions  
B) Allowed — because `s3:*` matches all S3 actions including `DeleteBucket`  
C) Denied — because `DeleteBucket` requires a resource-level condition  
D) Allowed — but only if MFA is enabled on the IAM user

---

### Q3. In AWS Secrets Manager, what is the primary security advantage of using IAM roles on EC2 instead of storing access keys in environment variables?

A) IAM roles are faster than access keys  
B) IAM roles provide automatic credential rotation and eliminate hardcoded secrets  
C) IAM roles allow unlimited API calls  
D) IAM roles bypass all IAM policies

---

### Q4. When you scan a Docker image in Amazon ECR using "Scan on push", which base image approach results in the fewest vulnerabilities?

A) `FROM ubuntu:20.04`  
B) `FROM centos:7`  
C) `FROM nginx:alpine`  
D) `FROM node:18`

---

### Q5. In AWS WAF, what does a **rate-based rule** protect against?

A) SQL injection attacks  
B) Cross-site scripting (XSS)  
C) DDoS and brute-force attacks by limiting requests per IP  
D) Man-in-the-middle attacks

---

### Q6. When evaluating IAM permissions, what is the order of precedence?

A) Allow → Deny → Implicit Deny  
B) Implicit Deny → Allow → Explicit Deny  
C) Explicit Deny → Explicit Allow → Implicit Deny  
D) Resource Policy → Identity Policy → SCP

---

### Q7. You create a multi-region CloudTrail trail. An attacker compromises credentials and launches EC2 instances in `ap-southeast-2`. Will your trail capture this activity?

A) No — CloudTrail only monitors the region it was created in  
B) Yes — a multi-region trail captures events from ALL AWS regions  
C) Only if you manually enable CloudTrail in `ap-southeast-2`  
D) Only if the attacker uses the AWS Console (not CLI)

---

### Q8. A GuardDuty finding of type `Stealth:IAMUser/CloudTrailLoggingDisabled` has a severity of 8.9. What does this indicate?

A) CloudWatch Logs has a transient delivery error  
B) An attacker is likely covering their tracks by disabling audit logging  
C) CloudTrail needs a software update  
D) A billing alarm has been triggered

---

### Q9. In AWS Config, what is the difference between a **Managed Rule** and a **Custom Rule**?

A) Managed rules are free; custom rules cost extra  
B) Managed rules are pre-built by AWS; custom rules use your own Lambda function for evaluation logic  
C) Custom rules run faster than managed rules  
D) Managed rules only apply to S3; custom rules apply to all services

---

### Q10. You create a CloudWatch Metric Filter with the pattern `{ $.eventName = "DeleteBucket" }` on a CloudTrail log group. What does this produce?

A) A CloudWatch Log Group  
B) A numeric CloudWatch metric that increments by 1 each time a `DeleteBucket` event is logged  
C) An SNS notification  
D) An EventBridge rule

---

### Q11. What is the purpose of a **quarantine security group** in an incident response playbook?

A) To allow only SSH traffic to the instance for investigation  
B) To isolate a compromised instance by removing ALL inbound and outbound network access  
C) To redirect the instance's traffic to a SIEM for analysis  
D) To terminate the instance automatically

---

### Q12. In CloudWatch, what advantage does a **Composite Alarm** provide over individual alarms?

A) It is cheaper than individual alarms  
B) It combines multiple alarm states with AND/OR logic, reducing false positives  
C) It replaces the need for SNS topics  
D) It automatically fixes the issue that caused the alarm

---

### Q13. When enabling **Detailed Monitoring** on an EC2 instance, what changes compared to Basic Monitoring?

A) CloudWatch collects more metric types (disk, memory)  
B) The metric reporting interval changes from 5 minutes to 1 minute  
C) The instance type is automatically upgraded  
D) CloudTrail begins logging EC2 API calls

---

### Q14. In the end-to-end encryption pipeline lab, the Lambda function uses `kms:GenerateDataKey` instead of `kms:Encrypt`. Why?

A) `GenerateDataKey` is cheaper than `Encrypt`  
B) `GenerateDataKey` implements the envelope encryption pattern — it creates a unique data key for each object, reducing KMS API calls and improving performance  
C) `Encrypt` is deprecated in KMS  
D) `GenerateDataKey` does not require IAM permissions

---

### Q15. An SSM Automation document is used in the IR playbook to orchestrate containment. What is the correct execution order for a compromised EC2 instance?

A) Terminate instance → Notify team → Take snapshot  
B) Notify team → Isolate instance (quarantine SG) → Take forensic EBS snapshot → Revoke IAM credentials → Send final report  
C) Revoke credentials → Delete instance → Create new instance  
D) Notify team → Terminate instance → Rotate all KMS keys

---

> ✏️ **Finished?** Check your answers in [quiz-answers.md](quiz-answers.md).

*NTI AWS Cloud Fundamentals — Security & Monitoring Quiz*
