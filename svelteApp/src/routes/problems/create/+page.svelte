<script lang="ts">
	import { writable } from 'svelte/store';
	import CodeEditor from '../../../components/CodeEditor.svelte';
	import type { CreateProblemPayload } from '$lib/problems_api';
	import { createProblem, createTestCase } from '$lib/problems_api';
	import { goto } from '$app/navigation';

	let title = '';
	let description = '';
	let difficulty = 'easy';
	let example_input = '';
	let example_output = '';
	let solution_code = '';
	let grade = 9;
	let category = 'arrays';
	let error = writable<string | null>(null);
	let testCases = writable<{ stdin: string; expected_output: string }[]>([{ stdin: '', expected_output: '' }]);
	let memory_limit = 256;
	let time_limit = 1;

	const difficultyOptions = ['easy', 'medium', 'hard'];
	const gradeOptions = [9, 10, 11, 12];
	const categoryOptions = [
		'arrays', 'linked_lists', 'sorting', 'searching', 'trees', 'graphs',
		'dynamic_programming', 'recursion', 'backtracking', 'bit_manipulation',
		'greedy', 'math', 'geometry', 'combinatorics', 'probability',
		'game_theory', 'puzzles', 'miscellaneous'
	];

	async function handleSubmit() {
		const problem: CreateProblemPayload = {
			title,
			description,
			difficulty,
			example_input,
			example_output,
			solution_code,
			grade,
			category,
			memory_limit,
			time_limit
		};

		try {
			const createdProblem = await createProblem(problem);
			const problemId = createdProblem.id;

			for (const testCase of $testCases) {
				await createTestCase(problemId, testCase);
			}

			alert('Problem created successfully. Now wait for the admin to approve it');
			await goto(`/problems`);
		} catch (err) {
			error.set('Failed to create problem or test cases');
			console.error('Failed to create problem or test cases:', err);
		}
	}

	function addTestCase() {
		testCases.update(cases => [...cases, { stdin: '', expected_output: '' }]);
	}

	function removeTestCase(index: number) {
		if ($testCases.length === 1) {
			alert('You must have at least one test case');
			return;
		}
		testCases.update(cases => cases.filter((_, i) => i !== index));
	}
</script>

<main class="min-h-screen bg-gray-100 py-10 flex justify-center items-center">
	<div class="max-w-2xl w-full px-4">
		<form on:submit|preventDefault={handleSubmit} class="space-y-4">
			<h1 class="text-3xl font-bold mb-4 text-center">Create Problem</h1>

			{#if $error}
				<p class="text-red-500">{$error}</p>
			{/if}

			<div>
				<label class="block font-medium mb-1" for="title">Title</label>
				<input id="title" type="text" bind:value={title} required class="w-full px-3 py-2 border rounded-md" />
			</div>

			<div>
				<label class="block font-medium mb-1" for="description">Description</label>
				<textarea id="description" bind:value={description} required
									class="w-full px-3 py-2 border rounded-md"></textarea>
			</div>

			<div>
				<label class="block font-medium mb-1" for="difficulty">Difficulty</label>
				<select id="difficulty" bind:value={difficulty} required class="w-full px-3 py-2 border rounded-md">
					{#each difficultyOptions as option}
						<option value={option}>{option.charAt(0).toUpperCase() + option.slice(1)}</option>
					{/each}
				</select>
			</div>

			<div>
				<label class="block font-medium mb-1" for="grade">Grade</label>
				<select id="grade" bind:value={grade} required class="w-full px-3 py-2 border rounded-md">
					{#each gradeOptions as option}
						<option value={option}>{option}th</option>
					{/each}
				</select>
			</div>

			<div>
				<label class="block font-medium mb-1" for="category">Category</label>
				<select id="category" bind:value={category} required class="w-full px-3 py-2 border rounded-md">
					{#each categoryOptions as option}
						<option
							value={option}>{option.replace('_', ' ').charAt(0).toUpperCase() + option.replace('_', ' ').slice(1)}</option>
					{/each}
				</select>
			</div>

			<div>
				<label class="block font-medium mb-1" for="example_input">Example Input</label>
				<textarea id="example_input" bind:value={example_input} required
									class="w-full px-3 py-2 border rounded-md"></textarea>
			</div>

			<div>
				<label class="block font-medium mb-1" for="example_output">Example Output</label>
				<textarea id="example_output" bind:value={example_output} required
									class="w-full px-3 py-2 border rounded-md"></textarea>
			</div>
			<div>
				<label class="block font-medium mb-1" for="memory_limit">Memory Limit (KB)</label>
				<input id="memory_limit" type="number" bind:value={memory_limit} required
							 class="w-full px-3 py-2 border rounded-md" />
			</div>

			<div>
				<label class="block font-medium mb-1" for="time_limit">Time Limit (seconds)</label>
				<input id="time_limit" type="number" bind:value={time_limit} required
							 class="w-full px-3 py-2 border rounded-md" />
			</div>
			<div class="mb-4">
				<label class="block font-medium mb-1" for="solution_code">Solution Code</label>
				<CodeEditor bind:code={solution_code} />
			</div>

			<div>
				<h2 class="text-xl font-semibold mb-2">Test Cases</h2>
				{#each $testCases as testCase, index}
					<div class="mb-4 p-4 border rounded-md">
						<div class="mb-2">
							<label class="block font-medium mb-1" for="example_input">Input</label>
							<textarea id="example_input" bind:value={testCase.stdin} required
												class="w-full px-3 py-2 border rounded-md"></textarea>
						</div>
						<div>
							<label class="block font-medium mb-1" for="example_output">Expected Output</label>
							<textarea id="example_output" bind:value={testCase.expected_output} required
												class="w-full px-3 py-2 border rounded-md"></textarea>
						</div>
						<button type="button" class="text-red-500 mt-2" on:click={() => removeTestCase(index)}>Remove
						</button>
					</div>
				{/each}
				<button type="button" class="btn btn-secondary" on:click={addTestCase}>Add Test Case</button>
			</div>
			<button type="submit" class="btn btn-primary">Create Problem</button>
		</form>
	</div>
</main>

<style lang="postcss">
    .btn {
        @apply px-4 py-2 rounded-lg;
    }

    .btn-primary {
        @apply bg-blue-500 text-white;
    }

    .btn-secondary {
        @apply bg-gray-500 text-white;
    }

    main {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    @media (min-width: 1024px) {
        main {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
</style>
