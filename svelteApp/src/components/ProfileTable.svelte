<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';
	import {
		getAllUserHomeworks,
		getProfile,
		getTeacherProblems,
		getUserClasses,
		getUserSolutions
	} from '$lib/users_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import { getProblemById, type ProblemSchema } from '$lib/problems_api';
	import type { ClassResponse } from '$lib/classes_api';
	import { type HomeworkDetail, type Solution } from '$lib/homeworks_api';
	import CodeEditorViewSolution from './CodeEditorViewSolution.svelte';

	const difficultyLabels: Record<string, string> = {
		'easy': 'Ușor',
		'medium': 'Mediu',
		'hard': 'Dificil'
	};
	export let activeTab: string;
	type DataType = (Solution & { problemTitle: string; difficulty: string }) | ProblemSchema | (ClassResponse & {
		teacherName: string
	}) | HomeworkDetail;

	function isSolution(data: DataType): data is Solution & { problemTitle: string; difficulty: string } {
		return 'percentage_passed' in data;
	}

	function isProblem(data: DataType): data is ProblemSchema {
		return 'title' in data && 'difficulty' in data;
	}

	function isClass(data: DataType): data is ClassResponse & { teacherName: string } {
		return 'teacherName' in data;
	}

	function isHomework(data: DataType): data is HomeworkDetail {
		return 'problem_title' in data && 'class_instance_name' in data;
	}

	const classesStore = writable<(ClassResponse & { teacherName: string })[]>([]);
	const problemsStore = writable<ProblemSchema[]>([]);
	const solutionsStore = writable<(Solution & { problemTitle: string, difficulty: string })[]>([]);
	const homeworksStore = writable<HomeworkDetail[]>([]);

	let classes: (ClassResponse & { teacherName: string })[] = [];
	let problems: ProblemSchema[] = [];
	let solutions: (Solution & { problemTitle: string, difficulty: string })[] = [];
	let homeworks: HomeworkDetail[] = [];
	let isLoading: boolean = true;
	let error: string | null = null;

	let paginationSettings: PaginationSettings = {
		page: 0,
		limit: 5,
		size: 0,
		amounts: [5, 10, 25, 50]
	};

	onMount(async () => {
		await fetchTabData(activeTab);
	});

	async function fetchTabData(tab: string) {
		isLoading = true;
		error = null;
		try {
			let access_token = getCookie('access');
			const userId = getUserIDFromJWT(access_token);

			switch (tab) {
				case 'sentSolutions':
					solutionsStore.subscribe(value => solutions = value);
					if (solutions.length === 0) {
						const rawSolutions = await getUserSolutions(userId);
						solutions = await Promise.all(rawSolutions.map(async (solution) => {
							const problem = await getProblemById(solution.problem_id);
							return {
								...solution,
								problemTitle: problem.title,
								difficulty: problem.difficulty
							};
						}));
						solutionsStore.set(solutions);
					}
					break;
				case 'problemsProposed':
					problemsStore.subscribe(value => problems = value);
					if (problems.length === 0) {
						problems = await getTeacherProblems(userId);
						problemsStore.set(problems);
					}
					break;
				case 'myClasses':
					classesStore.subscribe(value => classes = value);
					if (classes.length === 0) {
						const rawClasses = await getUserClasses(userId);
						classes = await Promise.all(rawClasses.map(async (classItem) => {
							const teacherProfile = await getProfile(classItem.teacher_id);
							return {
								...classItem,
								teacherName: `${teacherProfile.first_name} ${teacherProfile.last_name}`
							};
						}));
						classesStore.set(classes);
					}
					break;
				case 'myHomeworks':
					homeworksStore.subscribe(value => homeworks = value);
					if (homeworks.length === 0) {
						homeworks = await getAllUserHomeworks(userId);
						homeworksStore.set(homeworks);
					}
					break;
			}
			paginationSettings.page = 0;
		} catch (err: any) {
			console.error(err);
			error = err.message || 'An unexpected error occurred';
		} finally {
			isLoading = false;
		}
	}

	$: {
		if (activeTab) {
			fetchTabData(activeTab);
		}
	}

	$: currentData = (() => {
		switch (activeTab) {
			case 'sentSolutions':
				return solutions;
			case 'problemsProposed':
				return problems;
			case 'myClasses':
				return classes;
			case 'myHomeworks':
				return homeworks;
			default:
				return [];
		}
	})();

	$: paginationSettings.size = currentData.length;

	$: paginatedData = currentData.slice(
		paginationSettings.page * paginationSettings.limit,
		paginationSettings.page * paginationSettings.limit + paginationSettings.limit
	);

	let showSolutionModal = false;
	let currentSolution: Solution & { problemTitle: string; difficulty: string } | null = null;

	function isSolutionWithDetails(data: any): data is Solution & { problemTitle: string; difficulty: string } {
		return 'percentage_passed' in data && 'problemTitle' in data && 'difficulty' in data;
	}

	function openSolutionModal(row: any) {
		if (isSolutionWithDetails(row)) {
			currentSolution = row;
			showSolutionModal = true;
		} else {
			console.error('Attempted to open solution modal with invalid data type');
		}
	}

	function closeSolutionModal() {
		showSolutionModal = false;
		currentSolution = null;
	}


	function getDifficultyColor(difficulty: string): string {
		switch (difficulty) {
			case 'Easy':
				return 'text-green-600';
			case 'Medium':
				return 'text-yellow-600';
			case 'Hard':
				return 'text-blue-600';
			default:
				return '';
		}
	}

	function getScoreColor(score: number): string {
		if (score < 40) {
			return 'font-bold text-red-500';
		} else if (score < 80) {
			return 'font-bold text-yellow-500';
		} else {
			return 'font-bold text-green-500';
		}
	}

	function getEmptyMessage(tab: string): string {
		switch (tab) {
			case 'sentSolutions':
				return 'Nu ai trimis incă nicio soluție.';
			case 'problemsProposed':
				return 'Nu ai propus încă nicio problemă.';
			case 'myClasses':
				return 'Nu te-ai înscris încă în nicio clasă.';
			case 'myHomeworks':
				return 'Nu ai primit încă nicio temă.';
			default:
				return 'Nicio informație disponibilă';
		}
	}
</script>

<div class="w-full space-y-4 text-token mt-4">
	{#if isLoading}
		<p>Loading...</p>
	{:else if error}
		<p class="text-red-500">{error}</p>
	{:else if paginatedData.length === 0}
		<p class="text-center text-gray-500 my-8">{getEmptyMessage(activeTab)}</p>
	{:else}
		<table class="min-w-full divide-y divide-gray-200 shadow-lg">
			<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white">
			<tr>
				{#if activeTab === 'sentSolutions'}
					<th class="px-6 py-3 text-center">Titlul Problemei</th>
					<th class="px-6 py-3 text-center">Dificultate</th>
					<th class="px-6 py-3 text-center">Data Rezolvării</th>
					<th class="px-6 py-3 text-center">Punctaj</th>
					<th class="px-6 py-3 text-center">Acțiuni</th>
				{:else if activeTab === 'problemsProposed'}
					<th class="px-6 py-3 text-center">Titlul Problemei</th>
					<th class="px-6 py-3 text-center">Dificultate</th>
					<th class="px-6 py-3 text-center">Data propunerii</th>
					<th class="px-6 py-3 text-center">Status</th>
				{:else if activeTab === 'myClasses'}
					<th class="px-6 py-3 text-center">Numele clasei</th>
					<th class="px-6 py-3 text-center">Etichetă</th>
					<th class="px-6 py-3 text-center">Nume Profesor</th>
					<th class="px-6 py-3 text-center">Acțiuni</th>
				{:else if activeTab === 'myHomeworks'}
					<th class="px-6 py-3 text-center">Titlul Problemei</th>
					<th class="px-6 py-3 text-center">Numele clasei</th>
					<th class="px-6 py-3 text-center">Dată limită</th>
					<th class="px-6 py-3 text-center">Acțiuni</th>
				{/if}
			</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
			{#each paginatedData as row}
				<tr class="rounded-md">
					{#if activeTab === 'sentSolutions' && isSolution(row)}
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a href="/problems/{row.problem_id}"
																					   class="text-indigo-600 hover:text-indigo-900">{row.problemTitle}</a>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><span
							class={getDifficultyColor(row.difficulty)}>{difficultyLabels[row.difficulty.toLowerCase()]}</span>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{new Date(row.created_at).toLocaleDateString()}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><span
							class={getScoreColor(row.percentage_passed)}>{row.percentage_passed}%</span></td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">
							<button on:click={() => openSolutionModal(row)}
									class="btn bg-solution-btn hover:bg-teal-700">
								Vizualizează Soluție
							</button>
						</td>
					{:else if activeTab === 'problemsProposed' && isProblem(row)}
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a href="/problems/{row.id}"
																					   class="text-indigo-600 hover:text-indigo-900">{row.title}</a>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><span
							class={getDifficultyColor(row.difficulty)}>{difficultyLabels[row.difficulty.toLowerCase()]}</span>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{new Date(row.created_at).toLocaleDateString()}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">
                    <span
						class={row.status === 'Pending' ? 'text-yellow-500 text-lg' : row.status === 'Approved' ? 'text-green-500 text-lg' : 'text-red-500 text-lg'}>
                        {row.status}
                    </span>
						</td>
					{:else if activeTab === 'myClasses' && isClass(row)}
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a href="/classes/{row.id}"
																					   class="text-indigo-600 hover:text-indigo-900">{row.name}</a>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{row.tag}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{row.teacherName}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a href="/classes/{row.id}"
																					   class="btn bg-solution-btn hover:bg-teal-700">Vizualizează Clasă</a></td>
					{:else if activeTab === 'myHomeworks' && isHomework(row)}
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a href="/problems/{row.problem_id}"
																					   class="text-indigo-600 hover:text-indigo-900">{row.problem_title}</a>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{row.class_instance_name}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg">{new Date(row.due_date).toLocaleDateString()}</td>
						<td class="px-6 py-4 whitespace-nowrap text-center text-lg"><a
							href="/classes/{row.class_instance_id}"
							class="btn bg-solution-btn hover:bg-teal-700">Vizualizează Temă</a></td>
					{/if}
				</tr>
			{/each}
			</tbody>
		</table>

		<Paginator
			bind:settings={paginationSettings}
			showFirstLastButtons={true}
			showPreviousNextButtons={true}
			controlVariant="variant-soft bg-white"
			select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
		/>
	{/if}
</div>

{#if showSolutionModal && currentSolution}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
		<div class="bg-white p-6 rounded-lg shadow-xl w-11/12 h-5/6 flex flex-col">
			<h2 class="text-2xl font-bold mb-4">Solution for {currentSolution.problemTitle}</h2>
			<div class="flex-grow overflow-hidden">
				<CodeEditorViewSolution code={currentSolution.code} languageId={currentSolution.language_id} />
			</div>
			<div class="mt-4 flex justify-end">
				<button on:click={closeSolutionModal}
						class="btn bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
					Close
				</button>
			</div>
		</div>
	</div>
{/if}

<style lang="postcss">
    .btn.bg-solution-btn {
        @apply bg-none border-x-2 border-y-2 text-black hover:bg-indigo-600 hover:text-white hover:border-transparent py-2 px-4 rounded-md;
    }
</style>