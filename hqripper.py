#!/usr/bin/env python3

import os
import sys
import requests
import argparse
from typing import List

# Set your LM Studio API endpoint
LM_STUDIO_API_URL = os.getenv('LM_STUDIO_API_URL', 'http://localhost:8080/api/chat')

def generate_tasks(goal: str, context: str = "") -> List[str]:
    """
    Generate a list of tasks to achieve the given goal.
    """
    prompt = f"""
You are an AI assistant tasked with achieving the following goal:

Goal: {goal}

Based on the current context, generate a list of tasks to achieve this goal. Provide the tasks as a numbered list.

Context:
{context}
"""
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates tasks to achieve goals."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    response = requests.post(LM_STUDIO_API_URL, json=payload)
    response.raise_for_status()
    tasks_text = response.json().get('choices', [{}])[0].get('message', {}).get('content', "").strip()
    tasks = tasks_text.split('\n')
    return [task.strip() for task in tasks if task.strip()]

def execute_task(task: str, context: str = "") -> str:
    """
    Execute a given task and return the result.
    """
    prompt = f"""
You are an AI assistant executing the following task:

Task: {task}

Provide a detailed description of how you would execute this task and the expected outcome.

Context:
{context}
"""
    payload = {
        "messages": [
            {"role": "system", "content": "You are an assistant that executes tasks and provides results."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    response = requests.post(LM_STUDIO_API_URL, json=payload)
    response.raise_for_status()
    result = response.json().get('choices', [{}])[0].get('message', {}).get('content', "").strip()
    return result

def main():
    parser = argparse.ArgumentParser(description='AutoGPT CLI Emulator with LM Studio')
    parser.add_argument('goal', type=str, nargs='*', help='The goal you want the AI to achieve.')
    parser.add_argument('--continuous', action='store_true', help='Run the AI in continuous mode.')
    parser.add_argument('--max_iterations', type=int, default=5, help='Maximum number of iterations in continuous mode.')
    args = parser.parse_args()

    # Provide a default goal if none is specified
    if not args.goal:
        default_goal = "Solve a simple AI-related problem"
        print(f"No goal provided. Using default goal: '{default_goal}'")
        goal = default_goal
    else:
        goal = ' '.join(args.goal)

    context = ""
    iteration = 0
    print(f"Goal: {goal}\n")

    while True:
        iteration += 1
        print(f"=== Iteration {iteration} ===\n")

        # Generate tasks
        tasks = generate_tasks(goal, context)
        if not tasks:
            print("No tasks generated. Stopping execution.")
            break

        print("Generated Tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")
        print("\nStarting task execution...\n")

        # Execute tasks
        for idx, task in enumerate(tasks, 1):
            print(f"Executing Task {idx}: {task}")
            result = execute_task(task, context)
            print(f"Result:\n{result}\n")
            # Update context with the result of the task
            context += f"\nTask {idx} Iteration {iteration}: {task}\nResult: {result}\n"

        # Check for completion in continuous mode
        if not args.continuous:
            break  # Exit after one iteration if not in continuous mode

        if iteration >= args.max_iterations:
            print("Maximum iterations reached. Exiting continuous mode.")
            break

        # Optional: Implement a condition to exit if the goal is achieved
        if "goal achieved" in result.lower() or "completed" in result.lower():
            print("Goal achieved. Exiting continuous mode.")
            break

if __name__ == "__main__":
    main()
