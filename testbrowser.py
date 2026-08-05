import subprocess

def test_ego_browser():
    print("Testing Ego-browser...")
    
    # Ye script Google open kar ke us ka title bataye ga
    script = """
const task = await useOrCreateTaskSpace('test_google')
await openOrReuseTab('https://www.google.com', { wait: true })
const info = await pageInfo()
cliLog("Title is: " + info.title)
await completeTaskSpace(task.id, { keep: false })
"""

    try:
        process = subprocess.Popen(
            ["ego-browser", "nodejs"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=script)
        
        if process.returncode != 0:
            print("Browser Error:", stderr)
        else:
            print("Success! Output from browser:\n", stdout)
            
    except FileNotFoundError:
        print("ERROR: ego-browser is not installed or not in PATH.")

if __name__ == "__main__":
    test_ego_browser()