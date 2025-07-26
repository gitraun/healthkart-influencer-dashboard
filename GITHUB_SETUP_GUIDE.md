# GitHub Setup Guide: HealthKart Influencer Dashboard

## Step 1: Prepare Your Project

Before uploading to GitHub, let's ensure your project is clean and organized:

### Files to Include:
```
healthkart-influencer-dashboard/
├── src/
│   ├── calculations.py
│   ├── dashboard.py
│   ├── data_generator.py
│   ├── insights.py
│   └── upload.py
├── data/
│   ├── influencers.csv
│   ├── posts.csv
│   ├── tracking_data.csv
│   └── payouts.csv
├── app.py
├── pyproject.toml
├── README.md
├── replit.md
├── TESTING_GUIDE.md
├── INSTAGRAM_TESTING_GUIDE.md
├── PHASE_2_PLAN.md
└── GITHUB_SETUP_GUIDE.md
```

### Files to Exclude (Create .gitignore):
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Replit specific
.replit
.upm/
.pythonlibs/
replit.nix
```

## Step 2: Create GitHub Repository

### Option A: From GitHub Website
1. Go to [github.com](https://github.com)
2. Click **"New repository"** (green button)
3. **Repository name**: `healthkart-influencer-dashboard`
4. **Description**: `Instagram Influencer Campaign ROI Dashboard for HealthKart with analytics, ROAS tracking, and insights`
5. Choose **Public** or **Private**
6. ✅ **Add README file**
7. ✅ **Add .gitignore** → Choose **Python**
8. **License**: MIT License (recommended)
9. Click **"Create repository"**

### Option B: From Command Line (if you prefer)
```bash
# Create new repo on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/healthkart-influencer-dashboard.git
cd healthkart-influencer-dashboard
```

## Step 3: Upload Your Project

### Method A: GitHub Web Interface (Easiest)

1. **Go to your new repository on GitHub**
2. **Click "uploading an existing file"**
3. **Drag and drop all your project files** OR click "choose your files"
4. **Add commit message**: `Initial commit: Instagram influencer dashboard with ROI analytics`
5. **Click "Commit changes"**

### Method B: Git Commands (Advanced)

```bash
# In your project directory
git init
git add .
git commit -m "Initial commit: Instagram influencer dashboard with ROI analytics"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/healthkart-influencer-dashboard.git
git push -u origin main
```

## Step 4: Update README.md

Replace the generated README with this content:

```markdown
# HealthKart Influencer Campaign ROI Dashboard

A comprehensive Streamlit dashboard for tracking, analyzing, and optimizing Instagram influencer marketing campaigns for HealthKart brands (MuscleBlaze, HKVitals, Gritzo).

## 🚀 Features

- **Campaign Performance Tracking**: Monitor reach, engagement, and revenue metrics
- **ROI & ROAS Analysis**: Calculate regular and incremental return on ad spend
- **Influencer Insights**: Identify top performers and optimization opportunities  
- **Payout Management**: Track influencer compensation and cost efficiency
- **Export Functionality**: Download data and analytics reports

## 📊 Current Scope

**Platform Focus**: Instagram influencers only (simplified for reliability)
- 50 Instagram influencers across 6 categories
- Real-time engagement and revenue analytics
- ROAS calculations with baseline assumptions
- Cost per order and performance scoring

## 🛠 Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Replit-ready

## 🚀 Quick Start

### Run on Replit
1. Fork this repository
2. Open in Replit
3. Run: `streamlit run app.py --server.port 5000`
4. Generate sample data and explore

### Run Locally
```bash
pip install streamlit pandas plotly numpy
streamlit run app.py
```

## 📱 Dashboard Pages

1. **Data Upload**: Generate sample Instagram campaign data
2. **Campaign Performance**: KPIs, charts, top performer analysis
3. **ROI Analysis**: ROAS distributions, cost analysis, profitability
4. **Insights**: Automated recommendations and performance insights
5. **Export**: Download data and analytics reports

## 📈 Key Metrics

- **Regular ROAS**: Revenue ÷ Marketing Cost
- **Incremental ROAS**: (Revenue - Baseline) ÷ Marketing Cost  
- **Engagement Rate**: (Likes + Comments) ÷ Reach
- **Cost Per Order**: Marketing Cost ÷ Total Orders

## 🎯 Use Cases

- Marketing ROI optimization
- Influencer performance evaluation
- Budget allocation decisions
- Campaign effectiveness analysis
- Payout and cost management

## 📋 Testing

See `INSTAGRAM_TESTING_GUIDE.md` for step-by-step testing instructions.

## 🔧 Architecture

- **Modular Design**: Separate modules for calculations, dashboard, insights
- **CSV-Based**: File storage for easy data management
- **Session State**: Persistent data across dashboard pages
- **Error Handling**: Graceful handling of data issues

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

For questions or issues, please open a GitHub issue.
```

## Step 5: Add a Professional .gitignore

Create a `.gitignore` file with this content:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
env/
venv/
ENV/
env.bak/
venv.bak/

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Replit specific
.replit
.upm/
.pythonlibs/
replit.nix
uv.lock

# Data (optional - remove if you want to include sample data)
# data/*.csv

# Logs
*.log
```

## Step 6: Set Up Repository Topics and Description

1. **Go to your repository settings**
2. **Add topics/tags**:
   - `streamlit`
   - `dashboard`
   - `influencer-marketing`
   - `roi-analysis`
   - `python`
   - `data-analytics`
   - `healthkart`
   - `instagram`

3. **Update repository description**:
   `Instagram Influencer Campaign ROI Dashboard for HealthKart with analytics, ROAS tracking, and insights`

## Step 7: Enable GitHub Pages (Optional)

If you want to showcase your project:

1. **Go to Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: main
4. **Folder**: / (root)
5. **Save**

Note: This won't run the Streamlit app but will display your README.

## Step 8: Add Deployment Badge

Add this to your README.md to show it's Replit-ready:

```markdown
[![Run on Replit](https://replit.com/badge/github/YOUR_USERNAME/healthkart-influencer-dashboard)](https://replit.com/new/github/YOUR_USERNAME/healthkart-influencer-dashboard)
```

## 🎯 Repository Best Practices

### Commit Message Format:
- `feat: add new dashboard feature`
- `fix: resolve ROI calculation issue`  
- `docs: update testing guide`
- `refactor: improve data processing`

### Branch Strategy:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/feature-name`: New features
- `fix/issue-description`: Bug fixes

### Documentation:
- Keep README.md updated
- Document major changes in replit.md
- Include testing guides
- Add code comments

## ✅ Verification Checklist

After uploading to GitHub:

- [ ] Repository is public/private as intended
- [ ] All project files are uploaded
- [ ] README.md displays correctly
- [ ] .gitignore excludes unnecessary files
- [ ] Repository description and topics are set
- [ ] License is included
- [ ] Code runs without errors

Your Instagram Influencer Dashboard is now professionally hosted on GitHub and ready for collaboration, deployment, and showcasing!