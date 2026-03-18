# 🚀 AWS DevOps Hands-On Lab

## Docker + EC2: Build, Ship, and Run Your Application

---

> **Lab Duration:** ~90 minutes  
> **Level:** Beginner  
> **Prerequisites:** Basic Linux commands, AWS account access

---

## 📋 Table of Contents

1. [Lab Overview](#-lab-overview)
2. [Architecture Diagram](#-architecture-diagram)
3. [Part 1: EC2 Instance Setup (Instructor)](#-part-1-ec2-instance-setup-instructor)
4. [Part 2: Understanding the Application](#-part-2-understanding-the-application)
5. [Part 3: Write the Dockerfile (Exercise)](#-part-3-write-the-dockerfile-exercise)
6. [Part 4: Write the Deployment Script (Exercise)](#-part-4-write-the-deployment-script-exercise)
7. [Part 5: Deploy to AWS EC2](#-part-5-deploy-to-aws-ec2)
8. [Part 6: Verify Your Deployment](#-part-6-verify-your-deployment)
9. [Port Assignment Table](#-port-assignment-table)
10. [Troubleshooting](#-troubleshooting)
11. [Cleanup](#-cleanup)
12. [Bonus Challenges](#-bonus-challenges)

---

## 🎯 Lab Overview

### What You Will Learn
- ✅ How to containerize a web application using **Docker**
- ✅ How to write a **Dockerfile** from scratch
- ✅ How to build and save Docker images
- ✅ How to transfer files to a remote server using **SCP**
- ✅ How to deploy containers on **AWS EC2**
- ✅ How a real-world **CI/CD pipeline** works

### What You Will Build
A personalized web application that says **"Hello from [Your Name]"** running inside a Docker container on an AWS EC2 instance.

### Lab Flow
```
Your Laptop                          AWS EC2 Instance
┌──────────────┐                     ┌──────────────────┐
│              │                     │                  │
│  1. Write    │   3. SCP (copy)     │  4. Load image   │
│     Code     │ ──────────────────> │  5. Run container│
│              │                     │                  │
│  2. Build    │                     │  🌐 App is Live! │
│     Docker   │                     │  Port 3001-3030  │
│     Image    │                     │                  │
└──────────────┘                     └──────────────────┘
```

---

## 🏗 Architecture Diagram

```
                        ┌─────────────────────────────────────────┐
                        │         AWS EC2 Instance                │
                        │         (Amazon Linux 2)                │
                        │                                         │
   Student 1 ──────────>│  ┌─────────────────┐  Port 3001       │
   http://IP:3001       │  │  Container:      │ ◄───────────────  │
                        │  │  lab-ahmed        │                  │
                        │  └─────────────────┘                   │
                        │                                         │
   Student 2 ──────────>│  ┌─────────────────┐  Port 3002       │
   http://IP:3002       │  │  Container:      │ ◄───────────────  │
                        │  │  lab-sara         │                  │
                        │  └─────────────────┘                   │
                        │                                         │
   Student 3 ──────────>│  ┌─────────────────┐  Port 3003       │
   http://IP:3003       │  │  Container:      │ ◄───────────────  │
                        │  │  lab-omar         │                  │
                        │  └─────────────────┘                   │
                        │                                         │
                        │        ... more students ...            │
                        └─────────────────────────────────────────┘
```

---

## 🖥 Part 1: EC2 Instance Setup (Instructor)

> ⚠️ **This section is for the instructor.** Students can skip to [Part 2](#-part-2-understanding-the-application).

### Step 1.1: Launch an EC2 Instance

1. Go to **AWS Console** → **EC2** → **Launch Instance**
2. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `devops-lab-server` |
| **AMI** | Amazon Linux 2023 |
| **Instance Type** | `t2.medium` (or `t2.large` for 15+ students) |
| **Key Pair** | Create or select a `.pem` key pair |
| **Storage** | 30 GB gp3 |

### Step 1.2: Configure Security Group

Create a security group with the following **Inbound Rules**:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | Your IP / 0.0.0.0/0 | SSH access |
| Custom TCP | TCP | 3001-3030 | 0.0.0.0/0 | Student apps |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web access (optional) |

> 💡 **Why ports 3001-3030?** Each student runs their container on a unique port within this range.

### Step 1.3: Install Docker on EC2

After the instance is running, SSH into it and install Docker:

```bash
# Connect to EC2
ssh -i "devops-lab-key.pem" ec2-user@<EC2_PUBLIC_IP>

# Update the system
sudo yum update -y

# Install Docker
sudo yum install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group (optional, avoids using sudo)
sudo usermod -aG docker ec2-user

# Verify Docker is running
sudo docker --version
sudo docker ps
```

### Step 1.4: Share with Students

Give each student:
1. ✅ The EC2 **public IP address**
2. ✅ The `.pem` **key file** (or share securely)
3. ✅ Their assigned **port number**
4. ✅ The lab files (this repository)

---

## 📱 Part 2: Understanding the Application

### Project Structure

```
devops-lab/
├── app/
│   ├── app.py              # Flask application (main code)
│   ├── requirements.txt    # Python dependencies
│   └── templates/
│       └── index.html      # HTML template (the web page)
├── Dockerfile              # ✅ Solution (don't peek!)
├── Dockerfile.student      # 📝 Your exercise file
├── deploy.sh               # ✅ Solution (don't peek!)
├── deploy-student.sh       # 📝 Your exercise file
└── LAB-INSTRUCTIONS.md     # This file
```

### Step 2.1: Personalize the Application

Open `app/app.py` and change the `STUDENT_NAME` variable to your name:

```python
# ============================================================
# STUDENT: Change STUDENT_NAME to your own name!
# ============================================================
STUDENT_NAME = os.environ.get("STUDENT_NAME", "Your Name Here")
```

> 💡 You can either change the default value in the code, **or** pass your name as an environment variable when running the container (recommended).

### Step 2.2: Test Locally (Optional)

If you have Python installed on your laptop, you can test the app locally:

```bash
cd devops-lab/app
pip install -r requirements.txt
python app.py
```

Then open your browser at: http://localhost:5000

---

## 🐳 Part 3: Write the Dockerfile (Exercise)

### What is a Dockerfile?

A Dockerfile is a text file that contains **instructions** for building a Docker image. Think of it like a **recipe** that tells Docker how to package your application.

### Common Dockerfile Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Set the base image | `FROM python:3.11-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files into image | `COPY . .` |
| `RUN` | Execute a command | `RUN pip install -r requirements.txt` |
| `EXPOSE` | Document the port | `EXPOSE 5000` |
| `ENV` | Set environment variable | `ENV PORT=5000` |
| `CMD` | Default command to run | `CMD ["python", "app.py"]` |

### Exercise: Complete the Dockerfile

Open `Dockerfile.student` and fill in the blanks:

```dockerfile
# Step 1: Use a Python base image (hint: python:3.11-slim)
FROM ???

# Step 2: Set the working directory to /app
WORKDIR ???

# Step 3: Copy the requirements.txt file
COPY ???

# Step 4: Install the Python dependencies
RUN pip install ???

# Step 5: Copy the application source code
COPY ???

# Step 6: Expose the port (hint: Flask runs on port 5000)
EXPOSE ???

# Step 7: Set the environment variable for Flask
ENV FLASK_APP=???

# Step 8: Run the application
CMD ???
```

### 💡 Hints

1. The base image for Python 3.11 (slim version) is `python:3.11-slim`
2. The working directory should be `/app`
3. Copy requirements first for Docker layer caching: `COPY app/requirements.txt .`
4. Install with no cache: `pip install --no-cache-dir -r requirements.txt`
5. Copy the app directory: `COPY app/ .`
6. Flask default port is `5000`
7. For production, use gunicorn: `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]`

### ✅ Check Your Solution

After completing the Dockerfile, compare it with `Dockerfile` (the solution file).

<details>
<summary>Click to reveal the complete solution</summary>

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV PORT=5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

</details>

---

## 📜 Part 4: Write the Deployment Script (Exercise)

### What Does the Deployment Script Do?

The bash script automates the entire deployment process:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. BUILD    │     │  2. SAVE     │     │  3. COPY     │     │  4. DEPLOY   │
│  Docker      │────>│  Image to    │────>│  to EC2      │────>│  Load &      │
│  Image       │     │  .tar file   │     │  via SCP     │     │  Run on EC2  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Exercise: Complete the Deployment Script

Open `deploy-student.sh` and fill in the missing commands.

### Key Commands You'll Need

#### Build a Docker Image
```bash
docker build -t <image_name>:<tag> <build_context_path>
```

#### Save an Image to a .tar File
```bash
docker save -o <output_file.tar> <image_name>:<tag>
```

#### Copy a File to EC2 with SCP
```bash
scp -i <key_file.pem> <local_file> <user>@<ec2_ip>:<remote_path>
```

#### SSH into EC2 and Run Commands
```bash
ssh -i <key_file.pem> <user>@<ec2_ip> << 'EOF'
    # Remote commands go here
    sudo docker load -i /tmp/<file.tar>
    sudo docker run -d --name <name> -p <host_port>:5000 <image>
EOF
```

#### Run a Container with Port Mapping
```bash
docker run -d \
    --name <container_name> \
    -p <host_port>:<container_port> \
    -e STUDENT_NAME="<your_name>" \
    --restart unless-stopped \
    <image_name>:<tag>
```

### ✅ Check Your Solution

Compare your script with `deploy.sh` (the solution file).

---

## 🚀 Part 5: Deploy to AWS EC2

### Step 5.1: Update Your Configuration

In your deployment script (`deploy.sh` or your completed `deploy-student.sh`), update these values:

```bash
STUDENT_NAME="ahmed"               # Your name
PORT="3001"                        # Your assigned port
EC2_IP="54.123.45.67"             # EC2 public IP (from instructor)
KEY_FILE="devops-lab-key.pem"      # Path to .pem file
```

### Step 5.2: Set Key File Permissions

```bash
chmod 400 devops-lab-key.pem
```

> ⚠️ AWS requires strict permissions on the .pem file. If you skip this, SSH will refuse to connect.

### Step 5.3: Run the Deployment Script

```bash
./deploy.sh
```

Expected output:
```
============================================
  AWS DevOps Lab - Deployment
  Student: ahmed
  Port: 3001
  EC2: 54.123.45.67
============================================

📦 Step 1: Building Docker image...
✅ Image built successfully: devops-lab-ahmed:latest

💾 Step 2: Saving Docker image to tar file...
✅ Image saved to: devops-lab-ahmed.tar
   Size: 128M

📤 Step 3: Copying image to EC2 instance...
✅ Image copied to EC2 successfully!

🚀 Step 4: Deploying on EC2...
--- Loading Docker image ---
--- Running new container ---

============================================
  ✅ DEPLOYMENT COMPLETE!
============================================

  🌐 Your app is now live at:
     http://54.123.45.67:3001
============================================
```

### Step 5.4: Manual Deployment (Alternative)

If you prefer to run commands one by one:

```bash
# 1. Build the image
docker build -t devops-lab-ahmed:latest .

# 2. Save it
docker save -o devops-lab-ahmed.tar devops-lab-ahmed:latest

# 3. Copy to EC2
scp -i devops-lab-key.pem devops-lab-ahmed.tar ec2-user@54.123.45.67:/tmp/

# 4. SSH into EC2
ssh -i devops-lab-key.pem ec2-user@54.123.45.67

# 5. On EC2, load and run
sudo docker load -i /tmp/devops-lab-ahmed.tar
sudo docker run -d --name lab-ahmed -p 3001:5000 -e STUDENT_NAME="ahmed" devops-lab-ahmed:latest

# 6. Verify
sudo docker ps
```

---

## ✅ Part 6: Verify Your Deployment

### Open in Browser

Visit your application at:

```
http://<EC2_PUBLIC_IP>:<YOUR_PORT>
```

Example: `http://54.123.45.67:3001`

You should see a beautiful page with:
- ✅ "Hello from **[Your Name]**"
- ✅ Container ID
- ✅ Timestamp
- ✅ Status indicators

### Check from Terminal

```bash
# Test with curl
curl http://<EC2_PUBLIC_IP>:<YOUR_PORT>

# Test health endpoint
curl http://<EC2_PUBLIC_IP>:<YOUR_PORT>/health
```

Expected health response:
```json
{"status": "healthy", "student": "ahmed"}
```

---

## 📊 Port Assignment Table

| Student | Name | Port | URL |
|---------|------|------|-----|
| Sondos | | 3001 | `http://EC2_IP:3001` |
| Reem   | |3002 | `http://EC2_IP:3002` |
| Nada   | | 3003 | `http://EC2_IP:3003` |
| Ledia  | | 3004 | `http://EC2_IP:3004` |
| Manar  | | 3005 | `http://EC2_IP:3005` |
| Israa  | | 3006 | `http://EC2_IP:3006` |
| Raneem | | 3007 | `http://EC2_IP:3007` |
| Hazem Emad  | | 3008 | `http://EC2_IP:3008` |
| Hazem El-Nashar | | 3009 | `http://EC2_IP:3009` |
| Nour | | 3010 | `http://EC2_IP:3010` |
| Eslam | | 3011 | `http://EC2_IP:3011` |
| Mostafa Ahmed | | 3012 | `http://EC2_IP:3012` |
| Ahmed Hussien  | | 3013 | `http://EC2_IP:3013` |
| Abdullah  | | 3014 | `http://EC2_IP:3014` |
| Baraa | | 3015 | `http://EC2_IP:3015` |
| Mohamed El-Sayed | | 3016 | `http://EC2_IP:3016` |
| Mahmoud Reda | | 3017 | `http://EC2_IP:3017` |
| Mostafa Mahmoud | | 3018 | `http://EC2_IP:3018` |
| El Gazzar | | 3019 | `http://EC2_IP:3019` |
| Kiro | | 3020 | `http://EC2_IP:3020` |
| Raouf | | 3016 | `http://EC2_IP:3016` |
| Khaled | | 3017 | `http://EC2_IP:3017` |
| Hosny | | 3018 | `http://EC2_IP:3018` |
| 3lwan | | 3019 | `http://EC2_IP:3019` |
| Mahmoud Adel | | 3020 | `http://EC2_IP:3019` |

> 📝 **Instructor:** Fill in student names and share the EC2_IP before the lab.

---

## 🔧 Troubleshooting

### ❌ Problem: "Permission denied" when running deploy.sh

**Cause:** The script doesn't have execute permissions.

```bash
# Fix:
chmod +x deploy.sh
```

---

### ❌ Problem: "Permission denied (publickey)" on SSH/SCP

**Cause:** Wrong key file permissions or wrong key file.

```bash
# Fix: Set correct permissions
chmod 400 devops-lab-key.pem

# Verify you're using the right key
ls -la devops-lab-key.pem
```

---

### ❌ Problem: "Connection timed out" on SSH/SCP

**Possible Causes:**
1. Wrong EC2 public IP
2. Security group doesn't allow SSH (port 22)
3. EC2 instance is not running

```bash
# Verify the IP is correct
ping <EC2_IP>

# Check: Go to AWS Console → EC2 → Security Groups → Verify port 22 is open
```

---

### ❌ Problem: "Cannot connect to the Docker daemon"

**Cause:** Docker is not running on EC2.

```bash
# Fix: Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

### ❌ Problem: Website not loading in browser

**Possible Causes:**

1. **Container is not running:**
```bash
# Check on EC2
sudo docker ps -a
# If status is "Exited", check logs:
sudo docker logs <container_name>
```

2. **Wrong port in security group:**
```bash
# AWS Console → EC2 → Security Groups
# Verify your port (e.g., 3001) is in the inbound rules
```

3. **Port conflict (another student used your port):**
```bash
# Check which ports are in use
sudo docker ps --format "table {{.Names}}\t{{.Ports}}"
```

---

### ❌ Problem: "Port is already allocated"

**Cause:** Another container is using that port.

```bash
# Find what's using the port
sudo docker ps --filter "publish=3001"

# If it's your old container, remove it first:
sudo docker stop <container_name>
sudo docker rm <container_name>
```

---

### ❌ Problem: "No space left on device" on EC2

**Cause:** Too many Docker images/containers.

```bash
# Clean up unused images and containers
sudo docker system prune -a -f
```

---

### ❌ Problem: Page shows "Your Name Here" instead of your name

**Cause:** STUDENT_NAME environment variable not set.

```bash
# Fix: Run container with the -e flag
sudo docker run -d --name lab-ahmed -p 3001:5000 -e STUDENT_NAME="Ahmed" devops-lab-ahmed:latest
```

---

### ❌ Problem: "docker: command not found" on your laptop

**Cause:** Docker Desktop not installed locally.

**Fix:** Install Docker Desktop from https://www.docker.com/products/docker-desktop/

---

## 🧹 Cleanup

After the lab, clean up resources to avoid unnecessary charges.

### On EC2 (run as instructor):

```bash
# Stop all lab containers
sudo docker stop $(sudo docker ps -q)

# Remove all containers
sudo docker rm $(sudo docker ps -aq)

# Remove all images
sudo docker rmi $(sudo docker images -q)

# Clean up everything
sudo docker system prune -a -f
```

### On AWS Console:

1. **Terminate the EC2 instance** (EC2 → Instances → Actions → Terminate)
2. **Delete the security group** (if created specifically for this lab)
3. **Delete the key pair** (optional)

---

## 🏆 Bonus Challenges

Once you've completed the main lab, try these extra challenges!

### Challenge 1: Add a Custom Background Color 🎨
Modify `app/templates/index.html` to use your favorite color scheme, rebuild, and redeploy.

### Challenge 2: Add a Counter 🔢
Add a page visit counter to the Flask app using a global variable. Show it on the webpage.

### Challenge 3: Add Your Photo 📸
Add an image of yourself to the web page. (Hint: create a `static/` folder in the app)

### Challenge 4: Multi-Stage Docker Build 📦
Optimize your Dockerfile using a multi-stage build to reduce the image size.

### Challenge 5: Docker Compose 🐳
Write a `docker-compose.yml` file that runs multiple student containers at once.

---

## 📚 Key Concepts Summary

| Concept | What it is | Why it matters |
|---------|------------|----------------|
| **Docker Image** | A packaged snapshot of your app + dependencies | Ensures "it works on my machine" everywhere |
| **Docker Container** | A running instance of an image | Lightweight, isolated, reproducible |
| **Dockerfile** | Recipe for building an image | Automating the packaging process |
| **SCP** | Secure Copy Protocol | Transfer files between machines securely |
| **SSH** | Secure Shell | Remote login to servers |
| **EC2** | Elastic Compute Cloud | Virtual servers in AWS |
| **Security Group** | Virtual firewall for EC2 | Controls network access |
| **Port Mapping** | `-p host:container` | Connects external ports to container ports |

---

## 🔑 Quick Reference Commands

```bash
# Docker
docker build -t <name> .              # Build image
docker images                          # List images
docker run -d -p 3001:5000 <image>     # Run container
docker ps                              # List running containers
docker ps -a                           # List all containers
docker logs <container>                # View container logs
docker stop <container>                # Stop container
docker rm <container>                  # Remove container
docker rmi <image>                     # Remove image

# SSH/SCP
ssh -i key.pem user@ip                 # Connect to server
scp -i key.pem file user@ip:/path      # Copy file to server

# File Permissions
chmod 400 key.pem                      # Secure key file
chmod +x script.sh                     # Make script executable
```

---

> 🎓 **Congratulations!** You've just completed a real-world DevOps workflow:
> Build → Package → Ship → Deploy. This is the foundation of CI/CD pipelines
> used by companies like Amazon, Netflix, and Google every day!

---

*Lab created for NTI AWS Cloud Fundamentals course*
