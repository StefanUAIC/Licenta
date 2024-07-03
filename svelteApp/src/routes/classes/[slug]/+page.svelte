<script lang="ts">
	import { onMount, tick } from 'svelte';
	import type { ClassInfoResponse } from '$lib/classes_api';
	import { getClassInfo, getClassStudents } from '$lib/classes_api';
	import {
		createHomework,
		deleteHomework,
		getClassHomeworks,
		getHomeworkSubmissions,
		type Homework,
		type Solution
	} from '$lib/homeworks_api';
	import { getProfile, getUserRole, type ProfileSchema } from '$lib/users_api';
	import { getAllProblems, type ProblemSchema } from '$lib/problems_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { format } from 'date-fns';
	import Modal from '../../../components/Modal.svelte';
	import flatpickr from 'flatpickr';
	import 'flatpickr/dist/flatpickr.css';
	import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';
	import CodeEditorViewSolution from '../../../components/CodeEditorViewSolution.svelte';

	let showCodeEditor = false;
	let currentSubmissionCode = '';
	let currentSubmissionLanguageId = 0;
	let classId: number;
	let classInfo: ClassInfoResponse | null = null;
	let homeworks: Homework[] = [];
	let students: ProfileSchema[] = [];
	let problems: ProblemSchema[] = [];
	let selectedProblemId: number | null = null;
	let selectedDueDate: string | null = null;
	let role: 'student' | 'teacher' | null = null;
	let error: string | null = null;
	let accessToken: string | null = null;
	let showModal = false;
	let datepicker: HTMLInputElement | null = null;
	let dateError: string | null = null;
	let submissions: { [key: number]: Solution[] } = {};
	let currentSubmissions: Solution[] = [];
	let currentStudentProfiles: { [key: number]: ProfileSchema } = {};
	let homeworksPaginationSettings: PaginationSettings = {
		page: 0,
		limit: 10,
		size: homeworks.length,
		amounts: [1, 2, 3, 5, 10, homeworks.length]
	};

	let studentsPaginationSettings: PaginationSettings = {
		page: 0,
		limit: 10,
		size: students.length,
		amounts: [1, 2, 3, 5, 10, students.length]
	};

	let state = {
		firstLast: false,
		previousNext: true
	};


	onMount(async () => {
		const urlParams = get(page).params;
		classId = Number(urlParams.slug);

		accessToken = getCookie('access');

		if (!accessToken) {
			error = 'User is not authenticated';
			return;
		}

		try {
			const user_id = getUserIDFromJWT(accessToken);
			const roleResponse = await getUserRole(user_id);
			role = roleResponse.role;

			classInfo = await getClassInfo(classId);
			homeworks = await getClassHomeworks(classId);
			students = await getClassStudents(classId);
			problems = await getAllProblems();
			homeworksPaginationSettings.size = homeworks.length;
			studentsPaginationSettings.size = students.length;
			console.log('Class info:', classInfo);
		} catch (err: any) {
			error = err.message;
			console.error(err);
		}
	});

	function onPageChangeHomeworks(e: CustomEvent): void {
		homeworksPaginationSettings.page = e.detail.page;
	}

	function onAmountChangeHomeworks(e: CustomEvent): void {
		homeworksPaginationSettings.limit = e.detail.limit;
	}

	function onPageChangeStudents(e: CustomEvent): void {
		studentsPaginationSettings.page = e.detail.page;
	}

	function onAmountChangeStudents(e: CustomEvent): void {
		studentsPaginationSettings.limit = e.detail.limit;
	}

	const openModal = async () => {
		showModal = true;
		await tick();
		if (datepicker) {
			flatpickr(datepicker, {
				enableTime: true,
				dateFormat: 'Y-m-dTH:i:S',
				onChange: (selectedDates) => {
					if (selectedDates.length > 0) {
						selectedDueDate = selectedDates[0].toISOString();
					}
				}
			});
		}
	};

	const closeModal = () => {
		showModal = false;
		dateError = null;
	};

	const copyToClipboard = async (text: string) => {
		try {
			await navigator.clipboard.writeText(text);
			alert('Join code copied to clipboard!');
		} catch (err) {
			console.error('Failed to copy join code: ', err);
		}
	};

	const formatDate = (dateString: string) => {
		return format(new Date(dateString), 'MMMM d, yyyy h:mm a');
	};

	const handleCreateHomework = async () => {
		if (!selectedProblemId || !selectedDueDate) return;

		const now = new Date();
		const dueDate = new Date(selectedDueDate);

		if (dueDate <= now) {
			dateError = 'Due date must be in the future';
			return;
		}

		const payload = {
			problem_id: selectedProblemId,
			class_instance_id: classId,
			due_date: selectedDueDate
		};

		try {
			await createHomework(payload);
			homeworks = await getClassHomeworks(classId);
			showModal = false;
			selectedProblemId = null;
			selectedDueDate = null;
			dateError = null;
			homeworksPaginationSettings.size = homeworks.length;
		} catch (err) {
			console.error('Failed to create homework:', err);
		}
	};

	const handleDeleteHomework = async (homeworkId: number) => {
		try {
			await deleteHomework(homeworkId);
			homeworks = homeworks.filter(hw => hw.id !== homeworkId);
			delete submissions[homeworkId];
			homeworksPaginationSettings.size = homeworks.length;
		} catch (err) {
			console.error('Failed to delete homework:', err);
		}
	};

	const fetchSubmissions = async (homeworkId: number) => {
		try {
			const homeworkSubmissions = await getHomeworkSubmissions(homeworkId);
			currentSubmissions = homeworkSubmissions;

			for (let submission of homeworkSubmissions) {
				if (!currentStudentProfiles[submission.user_id]) {
					currentStudentProfiles[submission.user_id] = await getProfile(submission.user_id);
				}
			}
		} catch (err) {
			console.error('Failed to load submissions:', err);
		}
	};

	function getButtonColor(percentage: number): string {
		if (percentage > 80) {
			return 'bg-green-500';
		} else if (percentage > 40) {
			return 'bg-yellow-500';
		} else {
			return 'bg-red-500';
		}
	}

	let profilePicture = '../default-profile-picture.png';


	function openCodeEditor(submission: Solution) {
		if (role === 'teacher') {
			currentSubmissionCode = submission.code;
			currentSubmissionLanguageId = submission.language_id;
			showCodeEditor = true;
		}
	}

	function closeCodeEditor() {
		showCodeEditor = false;
	}
</script>

<template>
	<div class="h-full bg-gray-100 py-12 flex flex-col items-center">
		{#if error}
			<p class="text-red-500 text-center text-xl">{error}</p>
		{:else if classInfo}
			<h1 class="text-4xl font-bold text-center mb-6">{classInfo.name}</h1>
			<p class="mb-4"><strong>Clasă creată la data:</strong> {formatDate(classInfo.created_at)}</p>
			<div class="w-full max-w-screen-xl flex flex-col sm:flex-row space-y-6 sm:space-y-0 sm:space-x-6">
				<div class="w-full sm:w-1/2 p-8 rounded-lg shadow-2xl">
					<div class="flex justify-between items-center mb-1">
						{#if role === 'teacher'}
							<button on:click={openModal}
									class="bg-indigo-500 text-white py-2 px-4 rounded hover:bg-indigo-600 flex items-center justify-center space-x-3">
								<i class="fa fa-plus"></i> <span>Adaugă Temă</span>
							</button>
						{/if}
						<button on:click={() => copyToClipboard(classInfo.join_code)}
								class="bg-indigo-500 text-white py-2 px-4 rounded hover:bg-indigo-600 flex items-center justify-center space-x-3">
							<i class="fa fa-copy"></i> <span>Copiază Codul Clasei</span>
						</button>
					</div>
					<div class="w-full space-y-4 text-token mt-1">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white rounded-full">
							<tr>
								<th colspan="2"
									class="px-6 py-6 text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md text-center">
									Teme
								</th>
							</tr>
							</thead>
							<tbody class="bg-transparent divide-y divide-gray-200 gap-y-px">
							{#each homeworks.slice(homeworksPaginationSettings.page * homeworksPaginationSettings.limit, homeworksPaginationSettings.page * homeworksPaginationSettings.limit + homeworksPaginationSettings.limit) as homework}
								<tr on:click={() => fetchSubmissions(homework.id)} class="flex-column">
									<td class="px-6 py-5 whitespace-nowrap bg-white rounded-l-full cursor-pointer hover:bg-gray-100">
										{problems.find(problem => problem.id === homework.problem_id)?.title}
									</td>
									<td class="px-6 py-5 whitespace-nowrap bg-white rounded-r-full text-right text-gray-500 cursor-pointer hover:bg-gray-100">
										data limită {formatDate(homework.due_date)}
									</td>
									{#if role === 'teacher'}
										<td class="py-4 px-2 rounded-r-md flex justify-evenly">
											<button on:click={() => handleDeleteHomework(homework.id)}
													class="text-red-600 hover:text-red-900">
												<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em"
													 viewBox="0 0 40 40">
													<path fill="red"
														  d="M21.499 19.994L32.755 8.727a1.064 1.064 0 0 0-.001-1.502c-.398-.396-1.099-.398-1.501.002L20 18.494L8.743 7.224c-.4-.395-1.101-.393-1.499.002a1.05 1.05 0 0 0-.309.751c0 .284.11.55.309.747L18.5 19.993L7.245 31.263a1.064 1.064 0 0 0 .003 1.503c.193.191.466.301.748.301h.006c.283-.001.556-.112.745-.305L20 21.495l11.257 11.27c.199.198.465.308.747.308a1.058 1.058 0 0 0 1.061-1.061c0-.283-.11-.55-.31-.747z" />
												</svg>
											</button>
										</td>
									{/if}
								</tr>
							{/each}
							</tbody>
						</table>
						<Paginator bind:settings={homeworksPaginationSettings} on:page={onPageChangeHomeworks}
								   on:amount={onAmountChangeHomeworks} showFirstLastButtons={state.firstLast}
								   showPreviousNextButtons={state.previousNext} controlVariant="variant-soft bg-white"
								   select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
					</div>
				</div>
				<div class="w-full sm:w-1/2 p-8 rounded-lg shadow-2xl">
					<h2 class="text-2xl font-semibold mb-4">Studenți</h2>
					<div class="w-full space-y-4 text-token mt-4">
						<table class="min-w-full">
							<thead class="bg-transparent text-black">
							<tr>
								<th class="px-6 py-6 text-xs font-medium uppercase tracking-wider text-center border-black border-t-2 border-b-2">
								</th>
								<th class="px-6 py-6 text-xs font-medium uppercase tracking-wider text-center border-black border-t-2 border-b-2">
									Nume
								</th>
								<th class="px-6 py-6 text-xs font-medium uppercase tracking-wider text-center border-black border-t-2 border-b-2">
									Submisii
								</th>
							</tr>
							</thead>
							<tbody class="bg-transparent divide-y divide-gray-800 gap-y-px">
							{#each students as student}
								<tr>
									<td class="px-6 py-1 min-h-[50px] whitespace-nowrap text-center">
										<img src={profilePicture} alt={"Profile picture"}
											 class="w-16 h-16 rounded-full bg-white" />
									</td>
									<td class="px-6 py-1 min-h-[50px] whitespace-nowrap text-center">
										{student.first_name} {student.last_name}
									</td>
									<td class="px-6 py-1 min-h-[50px] whitespace-nowrap flex space-x-2 text-center">
										{#each currentSubmissions.filter(submission => submission.user_id) as submission}
											<button
												class={`py-1 px-3 rounded ${getButtonColor(submission.percentage_passed)} ${role !== 'teacher' ? 'cursor-not-allowed opacity-80' : ''}`}
												on:click={() => openCodeEditor(submission)}
												disabled={role !== 'teacher'}>
												{submission.percentage_passed}%
											</button>
										{/each}
									</td>
								</tr>
							{/each}
							</tbody>
						</table>
						<Paginator bind:settings={studentsPaginationSettings} on:page={onPageChangeStudents}
								   on:amount={onAmountChangeStudents} showFirstLastButtons={state.firstLast}
								   showPreviousNextButtons={state.previousNext} controlVariant="variant-soft bg-white"
								   select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
					</div>
				</div>
			</div>
		{:else}
			<p class="text-center text-xl">Loading...</p>
		{/if}
	</div>
	<Modal show={showModal} onClose={closeModal}>
		<div>
			<h2 class="text-xl font-bold mb-4">Adaugă Temă</h2>
			<div class="mb-4">
				<label for="problem" class="block mb-2">Problem</label>
				<select id="problem" class="w-full p-2 border rounded" bind:value={selectedProblemId}>
					<option value="" disabled selected>Select a problem</option>
					{#each problems as problem}
						<option value={problem.id}>{problem.title}</option>
					{/each}
				</select>
			</div>
			<div class="mb-4">
				<label for="dueDate" class="block mb-2">Data Limită</label>
				<input id="dueDate" type="text" class="w-full p-2 border rounded" bind:this={datepicker} />
				{#if dateError}
					<p class="text-red-500 mt-2">{dateError}</p>
				{/if}
			</div>
			<button on:click={handleCreateHomework}
					class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
				Adaugă Temă
			</button>
		</div>
	</Modal>

    {#if showCodeEditor}
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white p-6 rounded-lg shadow-xl w-3/4 h-3/4 flex flex-col">
                <h2 class="text-2xl font-bold mb-4">Solution Code</h2>
                <div class="flex-grow overflow-hidden">
                    <CodeEditorViewSolution code={currentSubmissionCode} languageId={currentSubmissionLanguageId} />
                </div>
                <div class="mt-4 flex justify-end">
                    <button on:click={closeCodeEditor}
                        class="btn bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                        Close
                    </button>
                </div>
            </div>
        </div>
    {/if}
</template>

<style>
    table {
        border-collapse: separate;
        border-spacing: 0 1rem;
    }

    table thead th:first-child {
        border-top-left-radius: 0.375rem;
        border-bottom-left-radius: 0.375rem;
    }

    table thead th:last-child {
        border-top-right-radius: 0.375rem;
        border-bottom-right-radius: 0.375rem;
    }

    .highlight {
        background-color: #e0e0e0;
    }

    table tbody tr:hover td:nth-child(1),
    table tbody tr:hover td:nth-child(2) {
        background-color: #e0e0e0;
    }

    td {
        min-height: 50px;
    }

    .second-table-header {
        background-color: transparent;
        border-top: 3px solid black !important;
        border-bottom: 3px solid black !important;
        color: black;
    }

    .second-table-body tr td {
        border-color: gray !important;
    }
</style>
