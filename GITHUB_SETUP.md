# 🚀 GitHub Upload Guide

## Step-by-Step Instructions to Upload Your Trading Bot to GitHub

### Prerequisites
- Git installed on your computer
- GitHub account
- Your testnet credentials configured in `.env`

---

## Method 1: Using the Automated Script (Recommended)

I've created an automated setup script for you:

```bash
# Run the setup script
bash setup_github.sh
```

This script will:
1. Initialize Git repository
2. Add all files
3. Create initial commit
4. Prompt for your GitHub username and repo name
5. Push to GitHub

---

## Method 2: Manual Git Commands

If you prefer to do it manually, follow these steps:

### 1. Open PowerShell/Terminal in the project folder

```powershell
cd C:\Users\HP\Coding\assignment
```

### 2. Initialize Git Repository

```bash
git init
```

### 3. Add All Files

```bash
git add .
```

### 4. Create Initial Commit

```bash
git commit -m "Initial commit: Binance Futures Testnet Trading Bot

- Complete trading bot implementation
- Market & Limit order support  
- BUY/SELL functionality
- Enhanced CLI with interactive mode
- Comprehensive logging
- Input validation
- Error handling
- Documentation and website"
```

### 5. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `binance-trading-bot` (or your choice)
3. Description: `Python trading bot for Binance Futures Testnet`
4. Choose **Public**
5. **DO NOT** check "Initialize with README"
6. Click **Create repository**

### 6. Link Local Repository to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/binance-trading-bot.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 7. Rename Branch to Main

```bash
git branch -M main
```

### 8. Push to GitHub

```bash
git push -u origin main
```

You'll be prompted for your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (PAT) from GitHub

---

## Step 9: Enable GitHub Pages (Website)

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**
6. Wait 2-3 minutes for deployment
7. Your site will be live at: `https://YOUR_USERNAME.github.io/binance-trading-bot/`

---

## Step 10: Create Personal Access Token (PAT)

GitHub no longer accepts passwords. You need a PAT:

1. Go to GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Note: `trading-bot-token`
5. Expiration: Choose your preference
6. Scopes: Check `repo`
7. Click **Generate token**
8. **COPY THE TOKEN IMMEDIATELY** (you won't see it again)

Use this token as your password when pushing to GitHub.

---

## Verification

After setup, verify everything:

```bash
# Check remote is set
git remote -v

# Check status
git status

# View commit history
git log --oneline
```

You should see output like:
```
origin  https://github.com/YOUR_USERNAME/binance-trading-bot.git (fetch)
origin  https://github.com/YOUR_USERNAME/binance-trading-bot.git (push)
```

---

## Troubleshooting

### Error: "remote: Repository not found"
- **Solution**: Make sure you created the repo on GitHub first
- Check your username in the remote URL

### Error: " Authentication failed"
- **Solution**: Use Personal Access Token instead of password
- Or configure SSH keys: https://docs.github.com/en/authentication

### Error: "Everything up-to-date"
- **Solution**: Files already pushed, check GitHub repository

---

## What Gets Uploaded

✅ **Included:**
- All Python source code
- Documentation (README.md, QUICKSTART.md)
- requirements.txt
- `.env.example` (template)
- `.gitignore` (protects sensitive files)
- Website files (docs/index.html)
- CI/CD workflow
- Sample log files

❌ **Excluded (via .gitignore):**
- `.env` (your actual credentials)
- `__pycache__/`
- `.gitignore` itself
- IDE files

---

## Bonus: Update Your Website Link

After uploading, the GitHub link in your website won't work yet. To fix:

1. Edit `docs/index.html`
2. Replace `YOUR_USERNAME` with your actual GitHub username:
   ```html
   <a href="https://github.com/YOUR_USERNAME/binance-trading-bot" class="btn">View on GitHub</a>
   ```
3. Commit and push the change:
   ```bash
   git add docs/index.html
   git commit -m "Update GitHub links"
   git push
   ```

---

## 🎉 Final Steps

1. **Verify GitHub**: https://github.com/YOUR_USERNAME/binance-trading-bot
2. **Verify Website**: https://YOUR_USERNAME.github.io/binance-trading-bot/
3. **Share the link** with your hiring team!

---

## Notes for Assignment Submission

As per the assignment instructions:
- Submit through Google Form (not email)
- Include GitHub repository link
- Ensure logs are included in the repository

Your repository will contain:
- ✅ Source code
- ✅ README.md with setup steps
- ✅ requirements.txt
- ✅ Log files from sample orders

Good luck with your application! 🚀