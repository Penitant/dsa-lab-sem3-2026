---
title: Debug the GPU Scheduler
week: 5
category: Heaps
start: 2026-11-06
end: 2026-11-08
---

**File to Fix and Submit:** [scheduler.py](scheduler.py)  
**Language:** Python 3 (no imports)  
**Estimated time:** ~45 min

---

## Submission

1. Copy `scheduler.py` and the `tests` folder into your folder: `students/<registration-no>/week5/`.
2. Fix the bugs in `scheduler.py` so that every test passes.
3. Open a pull request from your fork to `main` on or before **8 Nov 2026**. Touch only your own folder.

> [!NOTE]
> Use of AI tools cannot be technically restricted. However, these exercises are designed to build algorithmic thinking, which develops only through working the problems yourself. You are strongly encouraged to attempt them without AI assistance.

---

## The Story

**OverfitAI** is a three-person startup that has raised ₹40 crore on a pitch deck containing the word "agentic" 31 times. Its founder, **Gradient Dissent**, has promised investors AGI "by next quarter, or the one after, definitely".

The entire company runs on **one** rented GPU. Everyone keeps submitting training jobs to it: a cat detector, a meme-tuned LLM, an RLHF run on Reddit comments. The GPU can run only one job at a time.

The CTO, **Ada Backprop**, set one rule: every job gets a **priority** from 1 to 9, and **1 is the most urgent**. Whenever the GPU is free, the most urgent job runs next. If two jobs have the same priority, the one **submitted first** runs first.

The scheduler was written by the intern, **Vibe Coder Vikram**, who mostly larps as a 10x engineer on LinkedIn. It uses the min-heap from the lab. It mostly runs. Sometimes it crashes. Once it ran a job that had already been cancelled, and the investor demo trained a dog-or-muffin classifier for six hours.

Vikram has left to "build in public" from a café in Goa. The demo is on Monday. Fix the scheduler.

---

## What the Program Does

The program reads a list of commands, one per line:

| Command | Meaning |
|---|---|
| `SUBMIT name priority` | A new job joins the queue. |
| `RUN` | The GPU is free. Print the **name** of the job that runs next, and remove it from the queue. If the queue is empty, print `GPU idle`. |
| `CANCEL name` | Someone gave up on their job. Remove it from the queue. If no waiting job has that name, print `name not found`. |

`CANCEL` is the new part. You already know how to remove the **root** of a heap (`delete_min`). Here a job can be removed from **anywhere** in the heap, and the heap must still be correct afterwards.

### Input Format

- Line 1: an integer `n`, the number of commands.
- Next `n` lines: one command each.

Job names are single words and unique. Priorities are integers from 1 to 9.

### Output Format

One line for every `RUN`, and one line for every `CANCEL` of a job that is not waiting.

### Sample

Input
```
8
SUBMIT train-cat-detector 3
SUBMIT finetune-meme-llm 1
SUBMIT rlhf-on-reddit 2
RUN
RUN
SUBMIT embed-all-of-wikipedia 5
RUN
RUN
```

Output
```
finetune-meme-llm
rlhf-on-reddit
train-cat-detector
embed-all-of-wikipedia
```

---

## How the Code Is Organised

- `Job`: holds `name`, `priority` and `submitted` (1 for the first job, 2 for the next, and so on). Its `__lt__` decides which job is "smaller", which means which job runs first.
- `parent`, `left`, `right`: the index formulas from the lab.
- `GPUQueue`: a min-heap of jobs in the list `self.h`.
  - `sift_up(i)` and `sift_down(i)`: the two repair operations from the lab.
  - `submit(job)`: insert.
  - `next_job()`: delete min.
  - `cancel(name)`: find the job, then remove it from the middle of the heap.
- `main()`: reads the commands and prints the output.

---

## Your Task

The code has **6 bugs**: **1 syntax error** and **5 logic bugs**. Each bug is on one line or a few lines. Find and fix all of them.

- Fix the given code. Don't rewrite it from scratch.
- Don't add any imports.
- The input and output format must stay exactly as described.

### Testing

There are 5 tests in the `tests` folder. Each `N.in` is an input and `N.out` is the expected output. Run them from your `week5` folder:

```bash
python scheduler.py < tests/1.in
```

Compare what is printed with `tests/1.out`. To compare automatically in Git Bash or a Linux/Mac terminal:

```bash
for i in 1 2 3 4 5; do python scheduler.py < tests/$i.in | diff -q - tests/$i.out > /dev/null && echo "test $i: pass" || echo "test $i: FAIL"; done
```

All 5 must print `pass`.

---

## Hints

Try on your own first. Open a hint only when you are stuck.

<details>
<summary>Hint 1: where to start</summary>

Fix the syntax error first, then run test 1. Read every crash message carefully: the line number and the error type usually point straight at the bug.
</details>

<details>
<summary>Hint 2: think about the edge cases</summary>

What happens when the GPU calls `RUN` and only **one** job is waiting? What happens when two jobs have the **same** priority?
</details>

<details>
<summary>Hint 3: removing from the middle</summary>

When a job is cancelled at position `i`, the last job in the list is moved into position `i`. Draw a small heap on paper. Can the moved job ever be **smaller than its new parent**? If so, what needs to happen?
</details>

---

## Before You Submit

In your pull request description, write **one or two lines for each bug**: what was wrong and how you fixed it.
