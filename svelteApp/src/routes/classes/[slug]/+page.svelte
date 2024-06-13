<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { type ClassInfoResponse, getClassInfo, getClassStudents } from '$lib/classes_api';
	import { createHomework, deleteHomework, getClassHomeworks, type Homework } from '$lib/homeworks_api';
	import { getUserRole, type ProfileSchema } from '$lib/users_api';
	import { getAllProblems, type ProblemSchema } from '$lib/problems_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { format } from 'date-fns';
	import Modal from '../../../components/Modal.svelte';
	import flatpickr from 'flatpickr';
	import 'flatpickr/dist/flatpickr.css';

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
			console.log('Class info:', classInfo);
		} catch (err) {
			error = err.message;
			console.error(err);
		}
	});

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

	const goBack = () => {
		goto('/classes');
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

	const handleCreateHomework = async () =>
	{
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
		} catch (err) {
			console.error('Failed to create homework:', err);
		}
	}
;

	const handleDeleteHomework = async (homeworkId: number) => {
		try {
			await deleteHomework(homeworkId);
			homeworks = homeworks.filter(hw => hw.id !== homeworkId);
		} catch (err) {
			console.error('Failed to delete homework:', err);
		}
	};
</script>


<template>
	<div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 py-12">
		<div class="bg-white p-10 rounded-lg shadow-lg w-full max-w-2xl relative">
			{#if error}
				<p class="text-red-500 text-center text-xl">{error}</p>
			{:else if classInfo}
				<h1 class="text-4xl font-bold text-center mb-6">{classInfo.name}</h1>
				<div class="absolute top-4 right-4 text-gray-600">
					<p><strong>Teacher ID:</strong> {classInfo.teacher_id}</p>
				</div>
				<div class="mb-8 text-lg">
					<p class="mb-4"><strong>Created At:</strong> {formatDate(classInfo.created_at)}</p>
					<p class="flex items-center">
						<strong>Join Code:</strong>
						<button on:click={() => copyToClipboard(classInfo.join_code)}
								class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 ml-2">
							Copy
						</button>
					</p>
				</div>
				{#if role === 'teacher'}
					<button on:click={openModal}
							class="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 mb-4">
						Add Homework
					</button>
				{/if}
				<div class="mb-8">
					<h2 class="text-2xl font-semibold mb-4">Homeworks</h2>
					<ul>
						{#each homeworks as homework}
							<li class="mb-2">
								<p>
									<strong>Problem:</strong> {problems.find(problem => problem.id === homework.problem_id)?.title}
								</p>
								<p><strong>Due Date:</strong> {formatDate(homework.due_date)}</p>
								{#if role === 'teacher'}
									<button on:click={() => handleDeleteHomework(homework.id)}
											class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 mt-2">
										Delete
									</button>
								{/if}
							</li>
						{/each}
					</ul>
				</div>
				<div class="mb-8">
					<h2 class="text-2xl font-semibold mb-4">Students</h2>
					<ul>
						{#each students as student}
							<li class="mb-2">
								<p>{student.first_name} {student.last_name} ({student.email})</p>
							</li>
						{/each}
					</ul>
				</div>
				<button on:click={goBack}
						class="w-full bg-gray-300 text-gray-800 py-3 px-4 rounded hover:bg-gray-400 text-lg">
					Go Back
				</button>
			{:else}
				<p class="text-center text-xl">Loading...</p>
			{/if}
		</div>
	</div>
	<Modal show={showModal} onClose={closeModal}>
		<div>
			<h2 class="text-xl font-bold mb-4">Add Homework</h2>
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
				<label for="dueDate" class="block mb-2">Due Date</label>
				<input id="dueDate" type="text" class="w-full p-2 border rounded" bind:this={datepicker} />
				{#if dateError}
					<p class="text-red-500 mt-2">{dateError}</p>
				{/if}
			</div>
			<button on:click={handleCreateHomework}
					class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
				Add Homework
			</button>
		</div>
	</Modal>
</template>

<style>
    .error {
        color: red;
    }
</style>

