import subprocess
import ollama

def main():
    git_diff = subprocess.check_output("git diff", shell=True, encoding="utf-8" ).strip()

    target_code = f"""
The following is the result of git diff:

----
{git_diff}
----

Based on the changes, recommend 3 conventional commit messages in the following format:

[<type>]: <short description>

Use one of these types: feat, fix, docs, refactor, style, test, chore.

Output exactly 3 lines. No additional explanation.
"""

    response = ollama.generate(model="llama3.2", prompt=target_code)
    print(response["response"])
