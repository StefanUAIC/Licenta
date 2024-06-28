<script lang="ts">
	import { writable } from 'svelte/store';
	import CodeEditor from '../../../components/CodeEditor.svelte';
	import type { CreateProblemPayload } from '$lib/problems_api';
	import { createProblem, createTestCase } from '$lib/problems_api';
	import { fetchLanguages, verifyTestCases } from '$lib/code_submission_api';
	import { goto } from '$app/navigation';
	import Waves_4 from '../../../components/Waves_4.svelte';
	import { onMount } from 'svelte';

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
	let memory_limit = 2048;
	let time_limit = 1;
	let restrictions = '';
	let activeTestCase = writable<number>(0);
	let selectedLanguageId: number = 54;
	let verificationResults = writable<{
		passed: boolean;
		expected_output: string;
		actual_output: string;
		status: string;
	}[]>([]);
	let languages = writable<{ id: number; name: string }[]>([]);
	let selectedTestCase = writable<number | null>(null);

	const difficultyOptions = ['easy', 'medium', 'hard'];
	const gradeOptions = [9, 10, 11, 12];
	const categoryOptions = [
		'arrays', 'linked_lists', 'sorting', 'searching', 'trees', 'graphs',
		'dynamic_programming', 'recursion', 'backtracking', 'bit_manipulation',
		'greedy', 'math', 'geometry', 'combinatorics', 'probability',
		'game_theory', 'puzzles', 'miscellaneous'
	];

	onMount(async () => {
		await fetchLanguagesData();
	});

	const fetchLanguagesData = async () => {
		try {
			const data = await fetchLanguages();
			languages.set(data);
			if (!selectedLanguageId && data.length > 0) {
				selectedLanguageId = data[0].id;
			}
		} catch (err) {
			console.error('Failed to load languages:', err);
			error.set('Failed to load languages');
		}
	};

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
			time_limit,
			restrictions
		};

		try {
			const createdProblem = await createProblem(problem);
			const problemId = createdProblem.id;

			for (const testCase of $testCases) {
				await createTestCase(problemId, testCase);
			}

			alert('Problemă creată cu succes! Acum așteaptă să fie verificată de administrator.');
			await goto(`/problems`);
		} catch (err) {
			error.set('Failed to create problem or test cases');
			console.error('Failed to create problem or test cases:', err);
		}
	}

	function addTestCase() {
		testCases.update(cases => {
			const newCases = [...cases, { stdin: '', expected_output: '' }];
			activeTestCase.set(newCases.length - 1);
			return newCases;
		});
	}

	function removeTestCase(index: number) {
		if ($testCases.length === 1) {
			alert('You must have at least one test case');
			return;
		}
		testCases.update(cases => cases.filter((_, i) => i !== index));
		if ($activeTestCase === index) {
			activeTestCase.set(Math.max(0, index - 1));
		} else if ($activeTestCase > index) {
			activeTestCase.update(current => current - 1);
		}
	}

	function toggleTestCase(index: number) {
		activeTestCase.set(index);
	}

	function getTestCaseColor(index: number): string {
		return index === $activeTestCase
			? 'bg-blue-200 text-blue-800'
			: 'bg-gray-200 text-gray-800';
	}

	async function handleVerifyTestCases() {
		try {
			const submission = {
				source_code: solution_code,
				language_id: selectedLanguageId,
				test_cases: $testCases.map(testCase => ({
					stdin: testCase.stdin,
					expected_output: testCase.expected_output
				})),
				memory_limit: memory_limit,
				time_limit: time_limit
			};
			const results = await verifyTestCases(submission);
			verificationResults.set(results.map(result => ({
				passed: result.passed,
				expected_output: result.expected_output,
				actual_output: result.actual_output,
				status: result.status
			})));
		} catch (err) {
			error.set('Failed to verify test cases');
			console.error('Failed to verify test cases:', err);
		}
	}

	function getVerificationColor(passed: boolean): string {
		return passed
			? 'bg-green-200 text-green-800'
			: 'bg-red-200 text-red-800';
	}

	function toggleTestCaseDetails(index: number) {
		selectedTestCase.update(current => current === index ? null : index);
	}
</script>

<main class="min-h-screen bg-gray-100 pb-10">
	<div class="inset-0 z-0">
		<Waves_4 />
	</div>
	<div class="max-w-7xl mx-auto px-4">
		<h1 class="text-5xl font-bold mb-14 text-center">Create Problem</h1>

		{#if $error}
			<p class="text-red-500 text-center mb-4">{$error}</p>
		{/if}

		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
				<div class="space-y-6 bg-white p-6 rounded-lg shadow">
					<div>
						<label class="block font-bold text-xl mb-2" for="title">Problem Title</label>
						<input id="title" type="text" bind:value={title} required
							   class="w-full px-3 py-2 border rounded-md" />
					</div>

					<div>
						<label class="block font-bold text-xl mb-2" for="description">Problem Description</label>
						<textarea id="description" bind:value={description} required
								  class="w-full px-3 py-2 border rounded-md" rows="8"></textarea>
					</div>
					<div class="grid grid-cols-3 gap-4">
						<div>
							<label class="block font-bold text-xl mb-2" for="difficulty">Difficulty</label>
							<select id="difficulty" bind:value={difficulty} required
									class="w-full px-3 py-2 border rounded-md">
								{#each difficultyOptions as option}
									<option value={option}>{option.charAt(0).toUpperCase() + option.slice(1)}</option>
								{/each}
							</select>
						</div>

						<div>
							<label class="block font-bold text-xl mb-2" for="grade">Grade</label>
							<select id="grade" bind:value={grade} required class="w-full px-3 py-2 border rounded-md">
								{#each gradeOptions as option}
									<option value={option}>{option}th</option>
								{/each}
							</select>
						</div>

						<div>
							<label class="block font-bold text-xl mb-2" for="category">Category</label>
							<select id="category" bind:value={category} required
									class="w-full px-3 py-2 border rounded-md">
								{#each categoryOptions as option}
									<option
										value={option}>{option.replace('_', ' ').charAt(0).toUpperCase() + option.replace('_', ' ').slice(1)}</option>
								{/each}
							</select>
						</div>
					</div>
					<div>
						<label class="block font-bold text-xl mb-2" for="restrictions">Restrictions</label>
						<textarea id="restrictions" bind:value={restrictions} required
								  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
					</div>

					<div>
						<label class="block font-bold text-xl mb-2" for="example_input">Example Input</label>
						<textarea id="example_input" bind:value={example_input} required
								  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
					</div>

					<div>
						<label class="block font-bold text-xl mb-2" for="example_output">Example Output</label>
						<textarea id="example_output" bind:value={example_output} required
								  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
					</div>
					<div>
						<label class="block font-bold text-xl mb-2" for="memory_limit">Memory Limit (KB)</label>
						<input id="memory_limit" type="number" bind:value={memory_limit} required
							   class="w-full px-3 py-2 border rounded-md" />
					</div>

					<div>
						<label class="block font-bold text-xl mb-2" for="time_limit">Time Limit (seconds)</label>
						<input id="time_limit" type="number" bind:value={time_limit} required
							   class="w-full px-3 py-2 border rounded-md" />
					</div>
				</div>

				<div class="space-y-6 bg-white p-6 rounded-lg shadow">
					<div>
						<label class="block font-bold text-xl mb-2" for="language">Language</label>
						<select id="language" bind:value={selectedLanguageId} required
								class="w-full px-3 py-2 border rounded-md">
							{#each $languages as language}
								<option value={language.id}>{language.name}</option>
							{/each}
						</select>
					</div>

					<div>
						<label class="block font-bold text-xl mb-2" for="solution_code">Solution Code</label>
						<CodeEditor
							bind:code={solution_code}
							languageId={selectedLanguageId}
						/>
					</div>

					<button
						type="button"
						class="w-full px-4 py-2 mb-4 text-lg rounded-md bg-blue-200 text-blue-800 hover:bg-blue-300 transition-colors border border-blue-400"
						on:click={handleVerifyTestCases}
					>
						Verify Test Cases
					</button>

					<div>
						<h2 class="text-2xl font-bold mb-4">Test Cases</h2>
						<button
							type="button"
							class="w-full px-4 py-2 mb-4 text-lg rounded-md bg-green-200 text-green-800 hover:bg-green-300 transition-colors border border-green-400"
							on:click={addTestCase}
						>
							+ Add Test Case
						</button>
						<div class="flex flex-wrap gap-2 mb-4">
							{#each $testCases as _, index}
								<button
									type="button"
									class={`px-4 py-2 text-lg rounded-md ${getTestCaseColor(index)} hover:opacity-80 transition-opacity`}
									on:click={() => toggleTestCase(index)}
								>
									Test {index + 1}
								</button>
							{/each}
						</div>

						{#if $activeTestCase !== null}
							<div class="mt-4 p-4 bg-gray-100 rounded-lg">
								<h3 class="text-xl font-semibold mb-2">Test Case {$activeTestCase + 1} Details</h3>
								<div class="mb-4">
									<label class="block font-medium mb-1" for="test_case_input">Input</label>
									<textarea
										id="test_case_input"
										bind:value={$testCases[$activeTestCase].stdin}
										class="w-full px-3 py-2 border rounded-md"
										rows="4"
									></textarea>
								</div>
								<div class="mb-4">
									<label class="block font-medium mb-1" for="test_case_output">Expected Output</label>
									<textarea
										id="test_case_output"
										bind:value={$testCases[$activeTestCase].expected_output}
										class="w-full px-3 py-2 border rounded-md"
										rows="4"
									></textarea>
								</div>
								<button
									type="button"
									class="px-4 py-2 bg-red-200 text-red-800 rounded hover:bg-red-300 transition-colors border border-red-400"
									on:click={() => removeTestCase($activeTestCase)}
								>
									Remove Test Case
								</button>
							</div>
						{/if}
					</div>

					{#if $verificationResults.length > 0}
						<div class="mt-4">
							<h3 class="text-xl font-semibold mb-2">Verification Results</h3>
							<div class="flex flex-wrap gap-2">
								{#each $verificationResults as result, index}
									<button
										type="button"
										class={`px-3 py-1 rounded-full ${getVerificationColor(result.passed)} hover:opacity-80 transition-opacity`}
										on:click={() => toggleTestCaseDetails(index)}
									>
										Test {index + 1}: {result.passed ? 'Passed' : 'Failed'}
									</button>
								{/each}
							</div>

							{#if $selectedTestCase !== null}
								<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
									<div class="bg-white p-6 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
										<h4 class="text-lg font-medium mb-2">
											Test {$selectedTestCase + 1}:
											<span
												class={$verificationResults[$selectedTestCase].passed ? "text-green-600" : "text-red-600"}>
							{$verificationResults[$selectedTestCase].passed ? 'Passed' : 'Failed'}
						</span>
										</h4>
										<p><strong>Status:</strong> {$verificationResults[$selectedTestCase].status}</p>
										<div class="mt-2">
											<p><strong>Expected Output:</strong></p>
											<pre
												class="bg-gray-100 p-2 rounded mt-1 mb-2 whitespace-pre-wrap">{$verificationResults[$selectedTestCase].expected_output}</pre>
										</div>
										<div class="mt-2">
											<p><strong>Actual Output:</strong></p>
											<pre
												class="bg-gray-100 p-2 rounded mt-1 whitespace-pre-wrap">{$verificationResults[$selectedTestCase].actual_output}</pre>
										</div>
										<button
											class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
											on:click={() => selectedTestCase.set(null)}
										>
											Close
										</button>
									</div>
								</div>
							{/if}
						</div>
					{/if}
				</div>
			</div>

			<div class="flex justify-center mt-8">
				<button type="submit" class="btn btn-primary px-10 py-4 text-xl bg-indigo-600 hover:bg-indigo-700">
					Create Problem
				</button>
			</div>
		</form>
	</div>
</main>

<style lang="postcss">
    .btn {
        @apply px-4 py-2 rounded-lg;
    }

    .btn-primary {
        @apply text-white transition-colors;
    }

    .btn-secondary {
        @apply bg-gray-500 text-white hover:bg-gray-600 transition-colors;
    }
</style>
