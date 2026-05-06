# Push to GitHub - Step by Step

## Prerequisites

1. GitHub account (https://github.com)
2. Git installed locally
3. Project code complete ✅

## Steps

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `phishing-detection-system`
   - **Description:** `ML-powered phishing website detection system using Flask`
   - **Public or Private:** Your choice
   - **Add .gitignore:** Python (already have .gitignore)
   - **Add License:** MIT (already have LICENSE)
3. Click "Create repository"
4. Copy the HTTPS URL (looks like: `https://github.com/yourusername/phishing-detection-system.git`)

### 2. Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"
```

### 3. Add Remote Origin

```bash
git remote add origin https://github.com/yourusername/phishing-detection-system.git
```

### 4. Push to GitHub

```bash
# First push with all history
git branch -M main
git push -u origin main
```

### 5. Done! ✅

Your code is now on GitHub at:
```
https://github.com/yourusername/phishing-detection-system
```

---

## If Repository Already Exists

```bash
# Check existing remote
git remote -v

# Update remote if needed
git remote set-url origin https://github.com/yourusername/phishing-detection-system.git

# Push
git push -u origin main
```

---

## Alternative: Push All Branches

```bash
git push --all origin
git push --tags origin
```

---

## After Each Update

```bash
git add .
git commit -m "Your message here"
git push
```

---

## Verify Push

1. Visit: `https://github.com/yourusername/phishing-detection-system`
2. You should see all your files
3. Check README.md, requirements.txt, etc.

---

**Done! Your project is on GitHub! 🎉**
