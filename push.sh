#!/bin/bash
# Automated push script for Law Analyse MVP

set -e

echo "🚀 Law Analyse MVP - Push to GitHub"
echo "===================================="
echo ""

# Check if repository exists on GitHub
echo "📋 Checking GitHub repository..."
if git ls-remote origin &> /dev/null; then
    echo "✅ Repository exists on GitHub"
else
    echo "❌ Repository not found on GitHub"
    echo ""
    echo "Please create repository first:"
    echo "1. Open: https://github.com/new"
    echo "2. Repository name: law-analyse"
    echo "3. Public, no README/gitignore/license"
    echo "4. Create repository"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check git config
echo ""
echo "📋 Checking git configuration..."
GIT_USER=$(git config user.name)
GIT_EMAIL=$(git config user.email)
echo "   User: $GIT_USER <$GIT_EMAIL>"

if [ "$GIT_USER" != "nposeo" ]; then
    echo "⚠️  Warning: Git user is not 'nposeo'"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Show statistics
echo ""
echo "📊 Project statistics:"
echo "   Commits: $(git rev-list --count HEAD)"
echo "   Files: $(find . -type f ! -path './.git/*' ! -path './.venv/*' ! -path './node_modules/*' ! -path './.claude/*' | wc -l)"
echo "   Author: $(git log --format='%an <%ae>' | sort | uniq)"

# Confirm push
echo ""
read -p "🚀 Push to GitHub? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Push cancelled"
    exit 1
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Next steps:"
    echo "1. Open: https://github.com/nposeo/law-analyse"
    echo "2. Add Topics: legal-tech, ai, nlp, ukrainian-law"
    echo "3. Configure Secrets: OPENAI_API_KEY"
    echo "4. Create Release v1.0.0"
    echo ""
    echo "See GITHUB_SETUP.md for details"
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Common issues:"
    echo "- Authentication failed: Use Personal Access Token"
    echo "- Repository not found: Create repository on GitHub first"
    echo "- Permission denied: Check you're logged in as nposeo"
    echo ""
    echo "See PUSH_INSTRUCTIONS.md for troubleshooting"
    exit 1
fi
