<script lang="ts">
	import { getUserHomeworks, type HomeworkDetail } from '$lib/homeworks_api';
	import { getProblemById, type ProblemSchema } from '$lib/problems_api';
	import {
		type CodeSubmissionResult,
		type CodeSubmissionSchema,
		fetchLanguages,
		submitCode
	} from '$lib/code_submission_api';
	import { writable } from 'svelte/store';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import CodeEditor from '../../../components/CodeEditor.svelte';
	import Waves_4 from '../../../components/Waves_4.svelte';

	const difficultyLabels: Record<string, string> = { 'easy': 'Ușor', 'medium': 'Mediu', 'hard': 'Dificil' };
	const gradeLabels: Record<number, string> = {
		9: 'a 9-a',
		10: 'a 10-a',
		11: 'a 11-a',
		12: 'a 12-a'
	};
	const categoryLabels: Record<string, string> = {
		'arrays': 'Vectori',
		'linked_lists': 'Liste Înlănțuite',
		'sorting': 'Sortare',
		'searching': 'Căutare',
		'trees': 'Arbori',
		'graphs': 'Grafuri',
		'dynamic_programming': 'Programare Dinamică',
		'recursion': 'Recursivitate',
		'backtracking': 'Backtracking',
		'bit_manipulation': 'Manipulare de Biți',
		'greedy': 'Algoritmi Greedy',
		'math': 'Matematică',
		'geometry': 'Geometrie',
		'combinatorics': 'Combinatorică',
		'probability': 'Probabilitate',
		'game_theory': 'Teoria Jocurilor',
		'puzzles': 'Puzzle-uri',
		'miscellaneous': 'Diverse'
	};

	const problem = writable<ProblemSchema | null>(null);
	const error = writable<string | null>(null);
	const slug = $page.params.slug;
	let source_code = ``;
	let language_id = writable(54);
	let result = writable<CodeSubmissionResult[]>([]);
	let loading = writable(false);
	let passedCount = writable(0);
	let languages = writable<{ id: number; name: string }[]>([]);
	let homeworks = writable<HomeworkDetail[]>([]);
	let selectedHomeworkId = writable<number | null>(null);
	let activeTestCase = writable<number | null>(null);
	let submissionError = writable<string | null>(null);


	const fetchProblem = async () => {
		try {
			const data = await getProblemById(Number(slug));
			problem.set(data);
		} catch (err) {
			console.error('Failed to load problem:', err);
			error.set('Failed to load problem');
		}
	};

	const fetchHomeworks = async (user_id: number) => {
		try {
			const data = await getUserHomeworks(user_id, Number(slug));
			homeworks.set(data);
		} catch (err) {
			console.error('Failed to load homeworks:', err);
			error.set('Failed to load homeworks');
		}
	};

	onMount(() => {
		let access_token = getCookie('access');
		if (!access_token) {
			return;
		}
		let user_id = getUserIDFromJWT(access_token);
		fetchProblem();
		fetchLanguagesData();
		fetchHomeworks(user_id);
	});

	const fetchLanguagesData = async () => {
		try {
			const data = await fetchLanguages();
			languages.set(data);
		} catch (err) {
			console.error('Failed to load languages:', err);
			error.set('Failed to load languages');
		}
	};

	async function submitCodeHandler() {
		submissionError.set(null);

		if (!source_code.trim()) {
			submissionError.set('Codul sursă nu poate fi gol');
			return;
		}

		loading.set(true);

		const submission: CodeSubmissionSchema = {
			source_code,
			language_id: $language_id,
			problem_id: Number(slug),
			homework_id: $selectedHomeworkId
		};

		try {
			const results = await submitCode(submission);
			let passed = 0;
			results.forEach(testCase => {
				if (testCase.passed) {
					passed += 1;
				}
			});

			passedCount.set(passed);
			result.set(results);
			console.log('Results:', results);
		} catch (err) {
			console.error('Failed to submit code:', err);
			error.set('Failed to submit code');
		} finally {
			loading.set(false);
		}
	}

	function getDifficultyColor(difficulty: string): string {
		switch (difficulty.toLowerCase()) {
			case 'easy':
				return 'bg-green-600';
			case 'medium':
				return 'bg-yellow-600';
			case 'hard':
				return 'bg-blue-600';
			default:
				return 'bg-gray-600';
		}
	}

	function getTestCaseColor(passed: boolean): string {
		return passed
			? 'bg-green-200 text-green-800'
			: 'bg-red-200 text-red-800';
	}

	function toggleTestCase(index: number) {
		activeTestCase.update(current => current === index ? null : index);
	}
</script>

<main class="min-h-screen bg-gray-100 pb-10">
	<div class="inset-0 z-0">
		<Waves_4 />
	</div>
	{#if $problem}
		<h1 class="text-5xl font-bold mb-14 text-center">{$problem.title}</h1>
	{/if}
	<div class="max-w-7xl mx-auto px-4">
		<div class="mb-6">
			{#if $error}
				<p class="text-red-500 text-center">{$error}</p>
			{/if}
		</div>

		{#if $problem}
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
				<div class="bg-white p-6 rounded-lg shadow-md">
					<div class="flex justify-center items-center space-x-6 mb-8 text-xl">
						<span
							class={`px-4 py-2 rounded-full text-white text-xl ${getDifficultyColor($problem.difficulty)}`}>
							{difficultyLabels[$problem.difficulty.toLowerCase()]}
						</span>
						<span class="font-bold">Clasă: <span
							class="text-2xl">{gradeLabels[$problem.grade]}</span></span>
						<span class="font-bold">Categorie: <span
							class="text-2xl">{categoryLabels[$problem.category]}</span></span>
					</div>

					<p class="text-gray-700 mb-10 text-xl">{$problem.description}</p>

					<div class="mb-10">
						<h2 class="text-2xl font-semibold mb-4">Restricții:</h2>
						<p class="text-lg">{$problem.restrictions}</p>
					</div>

					<div class="mb-10">
						<h2 class="text-2xl font-semibold mb-4">Exemplu de Intrare</h2>
						<pre class="bg-gray-200 p-4 rounded text-lg">{$problem.example_input}</pre>
					</div>

					<div class="mb-10">
						<h2 class="text-2xl font-semibold mb-4">Exemplu de Ieșire</h2>
						<pre class="bg-gray-200 p-4 rounded text-lg">{$problem.example_output}</pre>
					</div>

					<div class="flex justify-between text-lg">
						<span><strong>Limită de timp:</strong> {$problem.time_limit} secunde</span>
						<span><strong>Limită de memorie:</strong> {$problem.memory_limit} KB</span>
					</div>
				</div>

				<div>
					<div class="bg-white p-6 rounded-lg shadow-md mb-6">
						<div class="mb-4">
							<label for="language" class="block text-lg font-medium text-gray-700 mb-2">Selectează
								Limbajul</label>
							<select id="language" class="block w-full p-2 border border-gray-300 rounded-lg"
									bind:value={$language_id}>
								{#each $languages as language}
									<option value={language.id}>{language.name}</option>
								{/each}
							</select>
						</div>

						<div class="mb-4">
							<label for="homework" class="block text-lg font-medium text-gray-700 mb-2">Selectează
								Tema</label>
							<select id="homework" class="block w-full p-2 border border-gray-300 rounded-lg"
									bind:value={$selectedHomeworkId}>
								<option value={null}>Niciuna</option>
								{#each $homeworks as homework}
									<option value={homework.id}>{homework.problem_title}
										- {homework.class_instance_name}</option>
								{/each}
							</select>
						</div>
						{#if $submissionError}
							<p class="text-red-500 mt-2">{$submissionError}</p>
						{/if}
						<CodeEditor bind:code={source_code} bind:languageId={$language_id} />
						<button class="btn bg-indigo-600 bg-opacity-80 mt-4 w-full text-white"
								on:click={submitCodeHandler}>
							Trimite Codul
						</button>
						{#if $loading}
							<p class="text-blue-500 mt-4">Se încarcă...</p>
						{/if}
					</div>

					{#if $result && $result.length > 0}
						<div class="bg-white p-6 rounded-lg shadow-md">
							<h2 class="text-2xl font-semibold mb-4">Rezultatele Testelor</h2>
							<p class="mb-4 text-lg">Teste Trecute: {$passedCount} / {$result.length}</p>

							<div class="flex flex-wrap gap-2 mb-4">
								{#each $result as testCase, index}
									<button
										class={`px-4 py-2 text-lg rounded-md ${getTestCaseColor(testCase.passed)} hover:opacity-80 transition-opacity`}
										on:click={() => toggleTestCase(index)}>
										Test {index + 1}
									</button>
								{/each}
							</div>

							{#if $activeTestCase !== null}
								<div class="mt-4 p-4 bg-gray-100 rounded-lg">
									<h3 class="text-xl font-semibold mb-2">Detalii Test {$activeTestCase + 1}</h3>
									<p><strong>Status:</strong> {$result[$activeTestCase].passed ? 'Trecut' : 'Eșuat'}
									</p>
									<p><strong>Ieșirea ta:</strong></p>
									<pre
										class="bg-white p-2 rounded mt-1 mb-2 whitespace-pre-wrap">{$result[$activeTestCase].actual_output || 'Nu există ieșire disponibilă'}</pre>
									{#if !$result[$activeTestCase].passed}
										<p><strong>Mesaj de eroare:</strong></p>
										<pre
											class="bg-red-100 text-red-800 p-2 rounded mt-1 whitespace-pre-wrap">{$result[$activeTestCase].status || 'Nu există mesaj de eroare disponibil'}</pre>
									{/if}
								</div>
							{/if}
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</div>
</main>

<style lang="postcss">
    .btn {
        @apply px-4 py-2 rounded-lg;
    }

    .btn-primary {
        @apply bg-blue-500 text-white hover:bg-blue-600 transition-colors;
    }
</style>