<script lang="ts">
	import { onMount } from 'svelte';
	import { getProfile, getUserClasses, getUserRole } from '$lib/users_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import type { ClassResponse, CreateClassPayload, JoinClassPayload } from '$lib/classes_api';
	import { createClass, joinClass, getClassStudents } from '$lib/classes_api';
	import { goto } from '$app/navigation';
	import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';
	import '@fortawesome/fontawesome-free/js/all.min.js';

	let role: 'student' | 'teacher' | null = null;
	let accessToken: string | null = null;
	let userClasses: ClassResponse[] = [];
	let userName: string | null = null;
	let classStudentCounts: Record<number, number> = {};


	let classesPaginationSettings = {
		page: 0,
		limit: 10,
		size: userClasses.length,
		amounts: [1, 2, 3, 5, 10]
	} satisfies PaginationSettings;

	let state = {
		firstLast: false,
		previousNext: true
	};

	function onPageChange(e: CustomEvent): void {
		console.log('Paginator - event:page', e.detail);
	}

	function onAmountChange(e: CustomEvent): void {
		console.log('Paginator - event:amount', e.detail);
	}

	$: classesBodySliced = userClasses.slice(
		classesPaginationSettings.page * classesPaginationSettings.limit,
		classesPaginationSettings.page * classesPaginationSettings.limit + classesPaginationSettings.limit
	);

	onMount(async () => {
		accessToken = getCookie('access');

		if (!accessToken) {
			return;
		}

		try {
			const user_id = getUserIDFromJWT(accessToken);
			const roleResponse = await getUserRole(user_id);
			role = roleResponse.role;

			if (role === 'teacher') {
				userName = 'Profesorului ' + ((await getProfile(user_id)).first_name);
			} else if (role === 'student') {
				userName = 'Elevului ' + ((await getProfile(user_id)).first_name);
			}

			userClasses = await getUserClasses(user_id);
			classesPaginationSettings.size = userClasses.length;
			classesPaginationSettings.amounts = [1, 2, 3, 5, 10, userClasses.length];
			classesPaginationSettings.amounts = classesPaginationSettings.amounts.filter((item, index) => classesPaginationSettings.amounts.indexOf(item) === index);
			for (let classItem of userClasses) {
				const students = await getClassStudents(classItem.id);
				classStudentCounts[classItem.id] = students.length;
			}
		} catch (err) {
			console.error(err);
		}
	});

	const handleJoinClass = async () => {
		try {
			const joinCode = prompt('Enter the join code:');
			if (!joinCode) return;

			const payload: JoinClassPayload = { join_code: joinCode };
			const classResponse = await joinClass(payload);
			console.log(classResponse);
			alert(`Joined class: ${classResponse.name}`);
			await goto(`/classes/${classResponse.class_id}`);
		} catch (err: any) {
			alert(err.message);
			console.error(err);
		}
	};
	const handleCreateClass = async () => {
		try {
			const className = prompt('Enter the class name:');
			if (!className) return;

			const classTag = prompt('Enter the class tag (up to 3 characters):');
			if (!classTag) return;
			if (classTag.length > 3) {
				alert('Class tag must be 3 characters or less.');
				return;
			}

			const payload: CreateClassPayload = { name: className, tag: classTag };
			const classResponse = await createClass(payload);
			alert(`Created class: ${classResponse.name}`);
			await goto(`/classes/${classResponse.id}`);
		} catch (err: any) {
			console.error(err);
		}
	};

	const handleEditClass = async (classId: number) => {
		console.log('Edit class', classId);
	};

	const handleDeleteClass = async (classId: number) => {
		console.log('Delete class', classId);
	};

	const goToClass = (classId: number) => {
		goto(`/classes/${classId}`);
	};
</script>

<template>
	<div class="h-full flex flex-col items-center justify-center py-6">
		<div class="flex flex-col sm:flex-row space-y-6 sm:space-y-0 sm:space-x-6">
			<div class="max-w-screen-lg sm:w-1/2 flex flex-col items-center p-8 rounded-lg">
				{#if role === 'teacher'}
					<img src="teacher_desk.png" alt="Teacher Desk" class="mb-4">
					<button on:click={handleCreateClass}
									class="bg-indigo-500 text-white py-2 px-4 rounded hover:bg-indigo-600 flex items-center justify-center space-x-3">
						<i class="fa fa-plus"></i> <span>Creează o clasă</span>
					</button>
				{:else if role === 'student'}
					<img src="student_desk.png" alt="Student Desk" class="mb-4">
					<button on:click={handleJoinClass}
									class="bg-indigo-500 text-white py-2 px-4 rounded hover:bg-indigo-600 flex items-center justify-center space-x-3">
						<img src="join_icon.png" alt="Join Icon" class="w-auto h-8"> <span>Alătură-te unei clase</span>
					</button>
				{/if}
			</div>
			<div class="sm:w-1/2 p-8 rounded-lg shadow-2xl">
				<div class="w-full space-y-4 text-token mt-4">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white rounded-full">
						<tr>
							<th colspan="4"
									class="px-6 py-6 text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md text-center">
								{#if userName}Clasele {userName}{/if}
							</th>
						</tr>
						</thead>
						<tbody class="bg-transparent divide-y divide-gray-200 gap-y-px">
						{#each classesBodySliced as classItem}
							<tr>
								<td class="w-16 pr-2">
									<div
										class="w-16 h-16 bg-blue-500 text-white  flex items-center justify-center rounded-full text-2xl">
										{classItem.tag}
									</div>
								</td>

								<td
									class="px-6 py-1 whitespace-nowrap class-name bg-white rounded-l-full cursor-pointer hover:highlight"
									on:click={() => goToClass(classItem.id)}>
									{classItem.name}
								</td>

								<td
									class="px-6 py-4 whitespace-nowrap bg-white rounded-r-full text-right cursor-pointer hover:highlight"
									on:click={() => goToClass(classItem.id)}> Număr de studenți: {classStudentCounts[classItem.id]}
								</td>
								{#if role === 'teacher'}
									<td class="py-4 px-2 rounded-r-md class-actions flex justify-evenly ">
										<button on:click={() => handleEditClass(classItem.id)}
														class="text-blue-600 hover:text-blue-900 object-center">
											<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em"
													 viewBox="0 0 24 24">
												<g fill="none" stroke="gray" stroke-linecap="round"
													 stroke-linejoin="round" stroke-width="0.75">
													<path
														d="M19.09 14.441v4.44a2.37 2.37 0 0 1-2.369 2.369H5.12a2.37 2.37 0 0 1-2.369-2.383V7.279a2.356 2.356 0 0 1 2.37-2.37H9.56" />
													<path
														d="M6.835 15.803v-2.165c.002-.357.144-.7.395-.953l9.532-9.532a1.362 1.362 0 0 1 1.934 0l2.151 2.151a1.36 1.36 0 0 1 0 1.934l-9.532 9.532a1.361 1.361 0 0 1-.953.395H8.197a1.362 1.362 0 0 1-1.362-1.362M19.09 8.995l-4.085-4.086" />
												</g>
											</svg>
										</button>
										<button on:click={() => handleDeleteClass(classItem.id)}
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
					<Paginator bind:settings={classesPaginationSettings} on:page={onPageChange}
										 on:amount={onAmountChange} showFirstLastButtons={state.firstLast}
										 showPreviousNextButtons={state.previousNext} controlVariant="variant-soft bg-white"
										 select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
				</div>
			</div>
		</div>
	</div>
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

    table tbody tr:hover td:nth-child(2),
    table tbody tr:hover td:nth-child(3) {
        background-color: #e0e0e0;
    }
</style>