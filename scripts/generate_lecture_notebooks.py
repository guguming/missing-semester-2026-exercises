from __future__ import annotations

import argparse
import copy
import json
import uuid
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_NOTEBOOK = ROOT / "1-course-shell" / "main.ipynb"
PLAYLIST_ID = "PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L"
BASH_NOTE = (
    "Note: Install `bash_kernel` and run `python -m bash_kernel.install --sys-prefix` "
    "(restart VS Code needed) for Jupyter notebooks to run bash code cells."
)
WORK_CELL = "# Work here.\n"


def md(text: str) -> str:
    return dedent(text).strip("\n")


LECTURES = [
    {
        "number": 2,
        "slug": "command-line-environment",
        "title": "Command-line Environment",
        "page_url": "https://missing.csail.mit.edu/2026/command-line-environment/",
        "video_id": "ccBGsPedE9Q",
        "sections": [
            {
                "title": "Arguments and Globs",
                "exercises": [
                    md(
                        """
                        You might see commands like `cmd --flag -- --notaflag`. The `--` is a special
                        argument that tells the program to stop parsing flags. Everything after `--` is
                        treated as a positional argument. Why might this be useful? Try running
                        `touch -- -myfile` and then removing it without `--`.
                        """
                    ),
                    md(
                        """
                        Read `man ls` and write an `ls` command that lists files in the following manner:

                        - Includes all files, including hidden files
                        - Sizes are listed in human readable format (e.g. `454M` instead of `454279954`)
                        - Files are ordered by recency
                        - Output is colorized

                        A sample output would look like this:

                        ```text
                        -rw-r--r--   1 user group 1.1M Jan 14 09:53 baz
                        drwxr-xr-x   5 user group  160 Jan 14 09:53 .
                        -rw-r--r--   1 user group  514 Jan 14 06:42 bar
                        -rw-r--r--   1 user group 106M Jan 13 12:12 foo
                        drwx------+ 47 user group 1.5K Jan 12 18:08 ..
                        ```
                        """
                    ),
                    md(
                        """
                        Process substitution `<(command)` lets you use a command's output as if it were a
                        file. Use `diff` with process substitution to compare the output of `printenv` and
                        `export`. Why are they different?

                        Hint: try `diff <(printenv | sort) <(export | sort)`.
                        """
                    ),
                ],
            },
            {
                "title": "Environment Variables",
                "exercises": [
                    md(
                        """
                        Write bash functions `marco` and `polo` that do the following: whenever you execute
                        `marco` the current working directory should be saved in some manner, then when you
                        execute `polo`, no matter what directory you are in, `polo` should `cd` you back to
                        the directory where you executed `marco`.

                        For ease of debugging you can write the code in a file `marco.sh` and (re)load the
                        definitions to your shell by executing `source marco.sh`.
                        """
                    )
                ],
            },
            {
                "title": "Return Codes",
                "exercises": [
                    md(
                        """
                        Say you have a command that fails rarely. In order to debug it you need to capture
                        its output but it can be time consuming to get a failure run. Write a bash script
                        that runs the following script until it fails and captures its standard output and
                        error streams to files and prints everything at the end. Bonus points if you can
                        also report how many runs it took for the script to fail.

                        ```bash
                        #!/usr/bin/env bash

                        n=$(( RANDOM % 100 ))
                        if [[ n -eq 42 ]]; then
                           echo "Something went wrong"
                           >&2 echo "The error was using magic numbers"
                           exit 1
                        fi

                        echo "Everything went according to plan"
                        ```
                        """
                    )
                ],
            },
            {
                "title": "Signals and Job Control",
                "exercises": [
                    md(
                        """
                        Start a `sleep 10000` job in a terminal, background it with `Ctrl-Z` and continue
                        its execution with `bg`. Now use `pgrep` to find its pid and `pkill` to kill it
                        without ever typing the pid itself.

                        Hint: use the `-af` flags.
                        """
                    ),
                    md(
                        """
                        Say you don't want to start a process until another completes. How would you go
                        about it? In this exercise, our limiting process will always be `sleep 60 &`. One
                        way to achieve this is to use the `wait` command. Try launching the sleep command
                        and having an `ls` wait until the background process finishes.

                        However, this strategy will fail if we start in a different bash session, since
                        `wait` only works for child processes. One feature we did not discuss in the notes
                        is that the `kill` command's exit status will be zero on success and nonzero
                        otherwise. `kill -0` does not send a signal but will give a nonzero exit status if
                        the process does not exist. Write a bash function called `pidwait` that takes a pid
                        and waits until the given process completes. You should use `sleep` to avoid
                        wasting CPU unnecessarily.
                        """
                    ),
                ],
            },
            {
                "title": "Files and Permissions",
                "exercises": [
                    md(
                        """
                        (Advanced) Write a command or script to recursively find the most recently modified
                        file in a directory. More generally, can you list all files by recency?
                        """
                    )
                ],
            },
            {
                "title": "Terminal Multiplexers",
                "exercises": [
                    md(
                        """
                        Follow a `tmux` tutorial and then learn how to do some basic customizations.
                        """
                    )
                ],
            },
            {
                "title": "Aliases and Dotfiles",
                "exercises": [
                    "Create an alias `dc` that resolves to `cd` for when you type it wrong.",
                    md(
                        """
                        Run
                        `history | awk '{$1=\"\";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10`
                        to get your top 10 most used commands and consider writing shorter aliases for them.

                        Note: this works for Bash; if you're using ZSH, use `history 1` instead of just
                        `history`.
                        """
                    ),
                    "Create a folder for your dotfiles and set up version control.",
                    md(
                        """
                        Add a configuration for at least one program, e.g. your shell, with some
                        customization. To start off, it can be something as simple as customizing your shell
                        prompt by setting `$PS1`.
                        """
                    ),
                    md(
                        """
                        Set up a method to install your dotfiles quickly (and without manual effort) on a
                        new machine. This can be as simple as a shell script that calls `ln -s` for each
                        file, or you could use a specialized utility.
                        """
                    ),
                    "Test your installation script on a fresh virtual machine.",
                    "Migrate all of your current tool configurations to your dotfiles repository.",
                    "Publish your dotfiles on GitHub.",
                ],
            },
            {
                "title": "Remote Machines (SSH)",
                "intro": md(
                    """
                    Install a Linux virtual machine (or use an already existing one) for these exercises.
                    If you are not familiar with virtual machines, check out a VM installation tutorial
                    first.
                    """
                ),
                "exercises": [
                    md(
                        """
                        Go to `~/.ssh/` and check if you have a pair of SSH keys there. If not, generate
                        them with `ssh-keygen -a 100 -t ed25519`. It is recommended that you use a password
                        and use `ssh-agent`.
                        """
                    ),
                    md(
                        """
                        Edit `.ssh/config` to have an entry like:

                        ```text
                        Host vm
                            User username_goes_here
                            HostName ip_goes_here
                            IdentityFile ~/.ssh/id_ed25519
                            LocalForward 9999 localhost:8888
                        ```
                        """
                    ),
                    "Use `ssh-copy-id vm` to copy your SSH key to the server.",
                    md(
                        """
                        Start a webserver in your VM by executing `python -m http.server 8888`. Access the
                        VM webserver by navigating to `http://localhost:9999` on your machine.
                        """
                    ),
                    md(
                        """
                        Edit your SSH server config by doing `sudo vim /etc/ssh/sshd_config` and disable
                        password authentication by editing the value of `PasswordAuthentication`. Disable
                        root login by editing the value of `PermitRootLogin`. Restart the `ssh` service
                        with `sudo service sshd restart`. Try SSHing in again.
                        """
                    ),
                    md(
                        """
                        (Challenge) Install `mosh` in the VM and establish a connection. Then disconnect
                        the network adapter of the server/VM. Can mosh properly recover from it?
                        """
                    ),
                    md(
                        """
                        (Challenge) Look into what the `-N` and `-f` flags do in `ssh` and figure out a
                        command to achieve background port forwarding.
                        """
                    ),
                ],
            },
        ],
    },
    {
        "number": 3,
        "slug": "development-environment",
        "title": "Development Environment and Tools",
        "page_url": "https://missing.csail.mit.edu/2026/development-environment/",
        "video_id": "QnM1nVzrkx8",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        Enable Vim mode in all the software you use that supports it, such as your editor
                        and your shell, and use Vim mode for all your text editing for the next month.
                        Whenever something seems inefficient, or when you think "there must be a better
                        way", try Googling it; there probably is a better way.
                        """
                    ),
                    "Complete a challenge from `VimGolf`.",
                    md(
                        """
                        Configure an IDE extension and language server for a project that you're working
                        on. Ensure that all the expected functionality, such as jump-to-definition for
                        library dependencies, works as expected. If you don't have code that you can use for
                        this exercise, you can use an open-source project from GitHub such as the Missing
                        Semester repo.
                        """
                    ),
                    "Browse a list of IDE extensions and install one that seems useful to you.",
                ]
            }
        ],
    },
    {
        "number": 4,
        "slug": "debugging-profiling",
        "title": "Debugging and Profiling",
        "page_url": "https://missing.csail.mit.edu/2026/debugging-profiling/",
        "video_id": "8VYT9TcUmKs",
        "sections": [
            {
                "title": "Debugging",
                "exercises": [
                    md(
                        """
                        Debug a sorting algorithm: the following pseudocode implements merge sort but
                        contains a bug. Implement it in a language of your choice, then use a debugger
                        (`gdb`, `lldb`, `pdb`, or your IDE's debugger) to find and fix the bug.

                        ```text
                        function merge_sort(arr):
                            if length(arr) <= 1:
                                return arr
                            mid = length(arr) / 2
                            left = merge_sort(arr[0..mid])
                            right = merge_sort(arr[mid..end])
                            return merge(left, right)

                        function merge(left, right):
                            result = []
                            i = 0, j = 0
                            while i < length(left) AND j < length(right):
                                if left[i] <= right[j]:
                                    append result, left[i]
                                    i = i + 1
                                else:
                                    append result, right[i]
                                    j = j + 1
                            append remaining elements from left and right
                            return result
                        ```

                        Test vector: `merge_sort([3, 1, 4, 1, 5, 9, 2, 6])` should return
                        `[1, 1, 2, 3, 4, 5, 6, 9]`. Use breakpoints and step through the merge function to
                        find where the incorrect element is being selected.
                        """
                    ),
                    md(
                        """
                        Install `rr` and use reverse debugging to find a corruption bug. Save this program
                        as `corruption.c`:

                        ```c
                        #include <stdio.h>

                        typedef struct {
                            int id;
                            int scores[3];
                        } Student;

                        Student students[2];

                        void init() {
                            students[0].id = 1001;
                            students[0].scores[0] = 85;
                            students[0].scores[1] = 92;
                            students[0].scores[2] = 78;

                            students[1].id = 1002;
                            students[1].scores[0] = 90;
                            students[1].scores[1] = 88;
                            students[1].scores[2] = 95;
                        }

                        void curve_scores(int student_idx, int curve) {
                            for (int i = 0; i < 4; i++) {
                                students[student_idx].scores[i] += curve;
                            }
                        }

                        int main() {
                            init();
                            printf("=== Initial state ===\\n");
                            printf("Student 0: id=%d\\n", students[0].id);
                            printf("Student 1: id=%d\\n", students[1].id);

                            curve_scores(0, 5);

                            printf("\\n=== After curving ===\\n");
                            printf("Student 0: id=%d\\n", students[0].id);
                            printf("Student 1: id=%d\\n", students[1].id);

                            if (students[1].id != 1002) {
                                printf("\\n ERROR: Student 1's ID was corrupted! Expected 1002, got %d\\n",
                                       students[1].id);
                                return 1;
                            }
                            return 0;
                        }
                        ```

                        Compile with `gcc -g corruption.c -o corruption` and run it. Student 1's ID gets
                        corrupted, but the corruption happens in a function that only touches student 0.
                        Use `rr record ./corruption` and `rr replay` to find the culprit. Set a watchpoint
                        on `students[1].id` and use `reverse-continue` after the corruption to find exactly
                        which line of code overwrote it.
                        """
                    ),
                    md(
                        """
                        Debug a memory error with AddressSanitizer. Save this as `uaf.c`:

                        ```c
                        #include <stdlib.h>
                        #include <string.h>
                        #include <stdio.h>

                        int main() {
                            char *greeting = malloc(32);
                            strcpy(greeting, "Hello, world!");
                            printf("%s\\n", greeting);

                            free(greeting);

                            greeting[0] = 'J';
                            printf("%s\\n", greeting);

                            return 0;
                        }
                        ```

                        First compile and run without sanitizers:
                        `gcc uaf.c -o uaf && ./uaf`. It may appear to work. Now compile with
                        AddressSanitizer: `gcc -fsanitize=address -g uaf.c -o uaf && ./uaf`. Read the error
                        report. What bug does ASan find? Fix the issue it identifies.
                        """
                    ),
                    md(
                        """
                        Use `strace` (Linux) or `dtruss` (macOS) to trace the system calls made by a
                        command like `ls -l`. What system calls is it making? Try tracing a more complex
                        program and see what files it opens.
                        """
                    ),
                    md(
                        """
                        Use an LLM to help debug a cryptic error message. Try copying a compiler error
                        (especially from C++ templates or Rust) and asking for an explanation and fix. Try
                        putting some of the output from `strace` or the address sanitizer into it.
                        """
                    ),
                ],
            },
            {
                "title": "Profiling",
                "exercises": [
                    "Use `perf stat` to get basic performance statistics for a program of your choice. What do the different counters mean?",
                    md(
                        """
                        Profile with `perf record`. Save this as `slow.c`:

                        ```c
                        #include <math.h>
                        #include <stdio.h>

                        double slow_computation(int n) {
                            double result = 0;
                            for (int i = 0; i < n; i++) {
                                for (int j = 0; j < 1000; j++) {
                                    result += sin(i * j) * cos(i + j);
                                }
                            }
                            return result;
                        }

                        int main() {
                            double r = 0;
                            for (int i = 0; i < 100; i++) {
                                r += slow_computation(1000);
                            }
                            printf("Result: %f\\n", r);
                            return 0;
                        }
                        ```

                        Compile with debug symbols: `gcc -g -O2 slow.c -o slow -lm`. Run
                        `perf record -g ./slow`, then `perf report` to see where time is spent. Try
                        generating a flame graph using the flamegraph scripts.
                        """
                    ),
                    md(
                        """
                        Use `hyperfine` to benchmark two different implementations of the same task (e.g.
                        `find` vs `fd`, `grep` vs `ripgrep`, or two versions of your own code).
                        """
                    ),
                    md(
                        """
                        Use `htop` to monitor your system while running a resource-intensive program. Try
                        using `taskset` to limit which CPUs a process can use:
                        `taskset --cpu-list 0,2 stress -c 3`. Why doesn't `stress` use three CPUs?
                        """
                    ),
                    md(
                        """
                        A common issue is that a port you want to listen on is already taken by another
                        process. Learn how to discover that process: first execute
                        `python -m http.server 4444` to start a minimal web server on port 4444. On a
                        separate terminal run `ss -tlnp | grep 4444` to find the process. Terminate it
                        with `kill <PID>`.
                        """
                    ),
                ],
            },
        ],
    },
    {
        "number": 5,
        "slug": "version-control",
        "title": "Version Control and Git",
        "page_url": "https://missing.csail.mit.edu/2026/version-control/",
        "video_id": "9K8lB61dl3Y",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        If you don't have any past experience with Git, either try reading the first couple
                        chapters of `Pro Git` or go through a tutorial like `Learn Git Branching`. As
                        you're working through it, relate Git commands to the data model.
                        """
                    ),
                    md(
                        """
                        Clone the repository for the class website.

                        1. Explore the version history by visualizing it as a graph.
                        2. Who was the last person to modify `README.md`?
                           Hint: use `git log` with an argument.
                        3. What was the commit message associated with the last modification to the
                           `collections:` line of `_config.yml`?
                           Hint: use `git blame` and `git show`.
                        """
                    ),
                    md(
                        """
                        One common mistake when learning Git is to commit large files that should not be
                        managed by Git or to add sensitive information. Try adding a file to a repository,
                        making some commits, and then deleting that file from history (not just the latest
                        commit).
                        """
                    ),
                    md(
                        """
                        Clone some repository from GitHub, and modify one of its existing files. What
                        happens when you do `git stash`? What do you see when running
                        `git log --all --oneline`? Run `git stash pop` to undo what you did with
                        `git stash`. In what scenario might this be useful?
                        """
                    ),
                    md(
                        """
                        Like many command line tools, Git provides a configuration file (or dotfile) called
                        `~/.gitconfig`. Create an alias in `~/.gitconfig` so that when you run `git graph`,
                        you get the output of `git log --all --graph --decorate --oneline`. You can do
                        this by directly editing the `~/.gitconfig` file, or you can use the `git config`
                        command to add the alias.
                        """
                    ),
                    md(
                        """
                        You can define global ignore patterns in `~/.gitignore_global` after running
                        `git config --global core.excludesfile ~/.gitignore_global`. This sets the location
                        of the global ignore file that Git will use, but you still need to manually create
                        the file at that path. Set up your global gitignore file to ignore OS-specific or
                        editor-specific temporary files, like `.DS_Store`.
                        """
                    ),
                    md(
                        """
                        Fork the repository for the class website, find a typo or some other improvement
                        you can make, and submit a pull request on GitHub. Please only submit PRs that are
                        useful. If you can't find an improvement to make, you can skip this exercise.
                        """
                    ),
                    md(
                        """
                        Practice resolving merge conflicts by simulating a collaborative scenario:

                        1. Create a new repository with `git init` and create a file called `recipe.txt`
                           with a few lines (e.g. a simple recipe).
                        2. Commit it, then create two branches: `git branch salty` and `git branch sweet`.
                        3. In the `salty` branch, modify a line (e.g. change "1 cup sugar" to
                           "1 cup salt") and commit.
                        4. In the `sweet` branch, modify the same line differently (e.g. change
                           "1 cup sugar" to "2 cups sugar") and commit.
                        5. Now switch to `master` and try `git merge salty`, then `git merge sweet`. What
                           happens? Look at the contents of `recipe.txt` - what do the `<<<<<<<`,
                           `=======`, and `>>>>>>>` markers mean?
                        6. Resolve the conflict by editing the file to keep the content you want, removing
                           the conflict markers, and completing the merge with `git add` and `git commit`
                           (or `git merge --continue`). Alternatively, try using `git mergetool` to
                           resolve the conflict with a graphical or terminal-based merge tool.
                        7. Use `git log --graph --oneline` to visualize the merge history you just
                           created.
                        """
                    ),
                ]
            }
        ],
    },
    {
        "number": 6,
        "slug": "shipping-code",
        "title": "Packaging and Shipping Code",
        "page_url": "https://missing.csail.mit.edu/2026/shipping-code/",
        "video_id": "KBMiB-8P4Ns",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        Save your environment with `printenv` to a file, create a venv, activate it,
                        `printenv` to another file and `diff before.txt after.txt`. What changed in the
                        environment? Why does the shell prefer the venv?

                        Hint: look at `$PATH` before and after activation. Run `which deactivate` and
                        reason about what the deactivate bash function is doing.
                        """
                    ),
                    "Create a Python package with a `pyproject.toml` and install it in a virtual environment. Create a lockfile and inspect it.",
                    "Install Docker and use it to build the Missing Semester class website locally using docker compose.",
                    "Write a Dockerfile for a simple Python application. Then write a `docker-compose.yml` that runs your application alongside a Redis cache.",
                    md(
                        """
                        Publish a Python package to TestPyPI (don't publish to the real PyPI unless it's
                        worth sharing). Then build a Docker image with said package and push it to
                        `ghcr.io`.
                        """
                    ),
                    "Make a website using GitHub Pages. Extra (non-)credit: configure it with a custom domain.",
                ]
            }
        ],
    },
    {
        "number": 7,
        "slug": "agentic-coding",
        "title": "Agentic Coding",
        "page_url": "https://missing.csail.mit.edu/2026/agentic-coding/",
        "video_id": "sTdz6PZoAnw",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        Compare the experience of coding by hand, using AI autocomplete, inline chat, and
                        agents by doing the same programming task four times. The best candidate is a
                        small-sized feature from a project you're already working on. If you're looking for
                        other ideas, you could consider completing "good first issue" style tasks in
                        open-source projects on GitHub, or Advent of Code / LeetCode problems.
                        """
                    ),
                    md(
                        """
                        Use an AI coding agent to navigate an unfamiliar codebase. This is best done in the
                        context of wanting to debug or add a new feature to a project you actually care
                        about. If you don't have any that come to mind, try using an AI agent to understand
                        how security-related features work in the `opencode` agent.
                        """
                    ),
                    "Vibe code a small app from scratch. Do not write a single line of code by hand.",
                    md(
                        """
                        For your coding agent of choice, create and test an `AGENTS.md` (or analogous file
                        for your agent of choice, such as `CLAUDE.md`), a skill, and a subagent. Think
                        about when you'd want to use one of these versus another.

                        Note that your coding agent of choice might not support some of these
                        functionalities; you can either skip them, or try a different coding agent that has
                        support.
                        """
                    ),
                    md(
                        """
                        Use a coding agent to accomplish the same goal as in the Markdown bullet points
                        regex exercise from the Code Quality lecture. Does it complete the task via direct
                        file edits? What are the downsides and limitations of an agent editing the file
                        directly to complete such a task? Figure out how to prompt the agent such that it
                        doesn't complete the task via direct file edits.

                        Hint: ask the agent to use one of the command-line tools mentioned in the first
                        lecture.
                        """
                    ),
                    md(
                        """
                        Most coding agents support a form of "yolo mode" (e.g. in Claude Code,
                        `--dangerously-skip-permissions`). It is not secure to use this mode directly, but
                        it may be acceptable to run a coding agent in an isolated environment like a
                        virtual machine or container and then enable autonomous operation. Get this setup
                        running on your machine. There is more than one way to set this up.
                        """
                    ),
                ]
            }
        ],
    },
    {
        "number": 8,
        "slug": "beyond-code",
        "title": "Beyond the Code",
        "page_url": "https://missing.csail.mit.edu/2026/beyond-code/",
        "video_id": "2DOEATfXT8k",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        Browse the source code of a well-known project (e.g. Redis or curl). Find examples
                        of some of the comment types mentioned in the lecture: a useful TODO, a reference
                        to external documentation, a "why not" comment explaining an avoided approach, or a
                        hard-learned lesson. What would be lost if that comment was not there?
                        """
                    ),
                    md(
                        """
                        Pick an open-source project you're interested in and look at its recent commit
                        history (`git log`). Find one commit with a good message that explains why the
                        change was made, and one with a weak message that only describes what changed. For
                        the weak one, look at the diff (`git show <hash>`) and try to write a better
                        commit message following the Problem -> Solution -> Implications structure. Notice
                        how much work is required to reassemble the necessary context after the fact.
                        """
                    ),
                ]
            }
        ],
    },
    {
        "number": 9,
        "slug": "code-quality",
        "title": "Code Quality",
        "page_url": "https://missing.csail.mit.edu/2026/code-quality/",
        "video_id": "XBiLUNx84CQ",
        "sections": [
            {
                "exercises": [
                    md(
                        """
                        Configure a formatter, linter, and pre-commit hooks for a project you're working
                        on. If you have lots of errors, autoformatting should take care of the format
                        errors. For the linter errors, try using an AI agent to fix all the linter errors.
                        Make sure the AI agent can run the linter and observe the results so that it can
                        run in an iterative loop to fix all the issues. Check the results carefully to
                        ensure the AI doesn't break your code.
                        """
                    ),
                    md(
                        """
                        Learn a testing library for a language you know and write a unit test for a project
                        you're working on. Run a code coverage tool, generate an HTML-formatted coverage
                        report, and observe the results. Can you find the lines that are covered? Your code
                        coverage will likely be very low. Try manually writing some tests to improve it.
                        Try using an AI agent to improve coverage; make sure the coding agent can run tests
                        with coverage and produce a line-by-line coverage report so it knows where to
                        focus.

                        Are the AI-generated tests actually good?
                        """
                    ),
                    "Set up continuous integration to run on every push for a project you're working on. Have CI run formatting, linting, and tests. Break your code on purpose (e.g. introduce a linter violation), and ensure that CI catches it.",
                    md(
                        """
                        Try writing a regex pattern and use the `grep` command-line tool to find
                        occurrences of `subprocess.Popen(..., shell=True)` in your code. Now, try to
                        "break" the regex pattern. Does `semgrep` still successfully match the dangerous
                        code that trips up your grep invocation?
                        """
                    ),
                    md(
                        """
                        Practice regex search-and-replace in your IDE or text editor by replacing the `-`
                        Markdown bullet markers with `*` bullet markers in the lecture notes. Note that
                        just replacing all the `-` characters in the file would be incorrect, as there are
                        many uses of that character that are not bullet markers.
                        """
                    ),
                    md(
                        """
                        Write a regex to capture from JSON structures of the form
                        `{"name": "Alyssa P. Hacker", "college": "MIT"}` the name (e.g.
                        `Alyssa P. Hacker`, in this example).

                        Hint: in your first attempt, you might end up writing a regex that extracts
                        `Alyssa P. Hacker", "college": "MIT`; read about greedy quantifiers in the Python
                        regex docs to figure out how to fix it.

                        1. Make the regex pattern work even in situations where the name has a `"` character
                           in it (double quotes can be escaped in JSON with `\\"`).
                        2. We do not recommend using regular expressions for sophisticated parsing problems
                           in practice. Figure out how to use your programming language's JSON parser for
                           this task. Write a command-line program that takes as input, on stdin, a JSON
                           structure of the form described above, and output, on stdout, the name. You
                           should only need a couple lines of code to do this. In Python, you can do it
                           easily in one line of code beyond `import json`.
                        """
                    ),
                ]
            }
        ],
    },
]


def load_template() -> dict:
    return json.loads(TEMPLATE_NOTEBOOK.read_text())


def source_lines(text: str) -> list[str]:
    return text.splitlines(keepends=True) or [text]


def new_cell_id() -> str:
    return uuid.uuid4().hex[:8]


def normalize_question_text(text: str) -> str:
    lines = text.splitlines()
    first_block: list[str] = []
    rest_start = len(lines)

    for idx, line in enumerate(lines):
        if line.strip() == "":
            rest_start = idx
            break
        first_block.append(line.strip())

    normalized = " ".join(part for part in first_block if part)
    if rest_start == len(lines):
        return normalized

    rest = "\n".join(lines[rest_start:])
    if not normalized:
        return rest
    return f"{normalized}\n{rest}"


def markdown_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": new_cell_id(),
        "metadata": {},
        "source": source_lines(text if text.endswith("\n") else f"{text}\n"),
    }


def code_cell(text: str = WORK_CELL, code_metadata: dict | None = None) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": new_cell_id(),
        "metadata": copy.deepcopy(code_metadata or {}),
        "outputs": [],
        "source": source_lines(text if text.endswith("\n") else f"{text}\n"),
    }


def notebook_header(lecture: dict) -> str:
    video_url = (
        f"https://www.youtube.com/watch?v={lecture['video_id']}"
        f"&list={PLAYLIST_ID}&index={lecture['number']}"
    )
    return md(
        f"""
        # {lecture['number']}. {lecture['title']}

        Links: [Video]({video_url}) | [Text]({lecture['page_url']})

        Resources:
        - Follow the lecture page's inline references for deeper reading on the tools mentioned below.

        {BASH_NOTE}

        This notebook mirrors `1-course-shell/main.ipynb` as an exercise workbook. The prompts are copied
        from the lecture page and the code cells are intentionally left open for your own notes,
        experiments, and solutions.
        """
    )


def build_notebook(lecture: dict, template: dict) -> dict:
    code_metadata = template["cells"][2]["metadata"]
    cells = [markdown_cell(notebook_header(lecture))]

    for section in lecture["sections"]:
        title = section.get("title")
        intro = section.get("intro")
        if title:
            if intro:
                cells.append(markdown_cell(md(f"## {title}\n\n{intro}")))
            else:
                cells.append(markdown_cell(f"## {title}\n"))
        elif intro:
            cells.append(markdown_cell(intro))

        for index, exercise in enumerate(section["exercises"], start=1):
            normalized_exercise = normalize_question_text(exercise)
            cells.append(markdown_cell(f"##### {index}. {normalized_exercise}\n"))
            cells.append(code_cell(code_metadata=code_metadata))

    return {
        "cells": cells,
        "metadata": copy.deepcopy(template["metadata"]),
        "nbformat": template["nbformat"],
        "nbformat_minor": template["nbformat_minor"],
    }


def validate_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text())
    assert notebook["nbformat"] == 4
    assert "metadata" in notebook
    assert notebook["cells"], f"{path} has no cells"
    for cell in notebook["cells"]:
        assert "id" in cell
        assert "source" in cell


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lecture exercise notebooks.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing generated notebooks",
    )
    args = parser.parse_args()

    template = load_template()
    targets = []
    for lecture in LECTURES:
        target = ROOT / f"{lecture['number']}-{lecture['slug']}" / "main.ipynb"
        if target.exists() and not args.force:
            raise SystemExit(
                f"Refusing to overwrite existing notebook without --force: {target}"
            )
        targets.append((lecture, target))

    for lecture, target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        notebook = build_notebook(lecture, template)
        target.write_text(json.dumps(notebook, indent=2, ensure_ascii=False) + "\n")
        validate_notebook(target)
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
