import os
import subprocess
from datetime import datetime, timedelta

# Configuration variables
REPO_PATH = r'C:\Users\alexm\Desktop\py'
COMMIT_MESSAGE = 'Hack the contribution graph'  
START_DATE = '2023-11-01'  
DAYS = 200
DAYS_TO_SKIP = 0
TEMP_FILE_NAME = 'temp.txt'  
BRANCH_NAME = 'main'

def run_command(command, env=None):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    return result.stdout.strip()

def change_date_and_commit(date, counter):
    """Change the date, modify a file, and commit the changes."""
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date
    env['GIT_COMMITTER_DATE'] = date
    
    with open(TEMP_FILE_NAME, 'a') as temp_file:
        temp_file.write(f'Commit {counter}\n')
    
    run_command('git add .')
    run_command(f'git commit -m "{COMMIT_MESSAGE} {counter}"', env=env)

def main():
    
    os.chdir(REPO_PATH)
    
    # Parse start date
    start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
    commit_counter = 1
    
    # Iterate through days and create commits
    for i in range(DAYS):
        commit_date = start_date + timedelta(days=i * (DAYS_TO_SKIP + 1))
        commit_date_str = commit_date.strftime('%Y-%m-%dT%H:%M:%S')
        print(f"Creating commit for {commit_date_str}")
        change_date_and_commit(commit_date_str, commit_counter)
        commit_counter += 1
    
    # Push changes to remote repository
    push_output = run_command(f'git push origin {BRANCH_NAME}')
    print(push_output)

if __name__ == "__main__":
    main()
