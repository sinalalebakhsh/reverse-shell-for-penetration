#!/bin/bash

# Function to get the last commit message
get_last_commit_message() {
    git log -1 --pretty=%B 2>/dev/null || echo "No previous commits"
}

# Add all changes to staging
echo "Adding changes to staging..."
git add .

# Check if there are any changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Get and display the last commit message
last_commit=$(get_last_commit_message)
echo "Last commit message: $last_commit"
echo ""

# Prompt for new commit message
read -p "Enter your commit message: " commit_message

# Check if commit message is empty
if [ -z "$commit_message" ]; then
    echo "Commit message cannot be empty. Aborting."
    exit 1
fi

# Commit with the provided message
echo "Committing changes..."
git commit -m "$commit_message"

# Check if commit was successful
if [ $? -eq 0 ]; then
    echo "Commit successful!"
    
    # Push to remote repository
    echo "Pushing to origin/main..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "Push successful!"
    else
        echo "Push failed!"
        exit 1
    fi
else
    echo "Commit failed!"
    exit 1
fi


clear