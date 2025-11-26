# Instructions to Protect the `main` Branch

To protect your `main` branch from force pushing or deletion, you need to configure branch protection rules in your repository settings. Here are the steps:

1.  **Navigate to your repository's settings:**
    Go to the main page of your repository on GitHub. Click on the "Settings" tab, which is usually located in the top navigation bar of the repository.

2.  **Go to the "Branches" settings:**
    In the left-hand navigation menu of the settings page, click on "Branches".

3.  **Add a new branch protection rule:**
    Click the "Add rule" button.

4.  **Specify the branch name pattern:**
    In the "Branch name pattern" field, type `main`.

5.  **Configure the protection settings:**
    - Check the box for **"Protect matching branches"**.
    - To prevent force pushes, select **"Do not allow force pushes"**.
    - To prevent deletions, select **"Do not allow deletions"**.
    - It is also recommended to **"Require status checks to pass before merging"**.

6.  **Save your changes:**
    Click the "Create" or "Save changes" button at the bottom of the page.

Once you have followed these steps, your `main` branch will be protected.
