<script lang="ts">
    import { onMount } from 'svelte';
	import { getProfile, getUserClasses, getUserRole } from '$lib/users_api';
    import { getCookie, getUserIDFromJWT } from '$lib/utils';
    import type { ClassResponse, CreateClassPayload, JoinClassPayload } from '$lib/classes_api';
    import { createClass, joinClass } from '$lib/classes_api';
    import { goto } from '$app/navigation';
    import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';

    let role: 'student' | 'teacher' | null = null;
    let error: string | null = null;
    let accessToken: string | null = null;
    let userClasses: ClassResponse[] = [];
    let teacherName: string | null = null;

    let classesPaginationSettings = {
        page: 0,
        limit: 3,
        size: userClasses.length,
        amounts: [1, 2, 3, 5, userClasses.length]
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
            error = 'User is not authenticated';
            return;
        }

        try {
            const user_id = getUserIDFromJWT(accessToken);
            const roleResponse = await getUserRole(user_id);
            role = roleResponse.role;

            if (role === 'teacher') {
                teacherName = 'Professor ' + ((await getProfile(user_id)).first_name); // Replace this with actual logic to get teacher's name
            }

            userClasses = await getUserClasses(user_id);
            classesPaginationSettings.size = userClasses.length; // Update pagination size
            console.log(userClasses);
            console.log(userClasses[0].name);

            console.log('User role:', role);
            console.log('User classes:', userClasses);
        } catch (err) {
            error = 'Failed to fetch user role or classes';
            console.error(err);
        }
    });

    const handleJoinClass = async () => {
        try {
            const joinCode = prompt('Enter the join code:');
            if (!joinCode) return;

            const payload: JoinClassPayload = { join_code: joinCode };
            const classResponse = await joinClass(payload);
            alert(`Joined class: ${classResponse.name}`);
            await goto(`/classes/${classResponse.id}`);
        } catch (err) {
            error = err.message;
            console.error(err);
        }
    };

    const handleCreateClass = async () => {
        try {
            const className = prompt('Enter the class name:');
            if (!className) return;

            const payload: CreateClassPayload = { name: className };
            const classResponse = await createClass(payload);
            alert(`Created class: ${classResponse.name}`);
            await goto(`/classes/${classResponse.id}`);
        } catch (err) {
            error = err.message;
            console.error(err);
        }
    };

    const goToClass = (classId: number) => {
        goto(`/classes/${classId}`);
    };

    const handleEditClass = async (classId: number) => {
        // Implement edit class functionality
        console.log('Edit class', classId);
    };

    // const handleDeleteClass = async (classId: number) => {
    //     try {
    //         await deleteClass(classId);
    //         alert('Class deleted');
    //         // Refresh the classes list or remove the class from userClasses array
    //         userClasses = userClasses.filter((classItem) => classItem.id !== classId);
    //     } catch (err) {
    //         error = err.message;
    //         console.error(err);
    //     }
    // };
</script>

<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 py-6">
        <div class="flex flex-col sm:flex-row w-full max-w-6xl space-y-6 sm:space-y-0 sm:space-x-6">
            <div class="w-full sm:w-1/2 flex flex-col items-center bg-white p-8 rounded-lg shadow-lg">
                {#if role === 'teacher'}
                    <img src="teacher_desk.png" alt="Teacher Desk" class="mb-4">
                    <button on:click={handleCreateClass} class="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 flex items-center justify-center space-x-2">
                        <i class="fa fa-plus"></i> <span>Create a class</span>
                    </button>
                {:else if role === 'student'}
                    <img src="student_desk.png" alt="Student Desk" class="mb-4">
                    <button on:click={handleJoinClass} class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 flex items-center justify-center space-x-2">
                        <img src="join_icon.png" alt="Join Icon" class="w-4 h-4"> <span>Join a class</span>
                    </button>
                {/if}
            </div>
            <div class="w-full sm:w-1/2 bg-white p-8 rounded-lg shadow-lg">
                <div class="w-full space-y-4 text-token mt-4">
                    <table class="min-w-full divide-y divide-gray-200 shadow-lg">
                        <thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white">
                        <tr>
                            <th class="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md">
                                {#if teacherName}{teacherName}'s classes{/if}
                            </th>
                        </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                        {#each classesBodySliced as classItem, index}
                            <tr class="rounded-md">
                                <td class="px-6 py-4 whitespace-nowrap rounded-l-md">
                                    <div class="w-8 h-8 bg-blue-500 text-white flex items-center justify-center rounded-full">
                                        {index + 1}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <a href="/classes/{classItem.id}"
                                       class="text-indigo-600 hover:text-indigo-900">{classItem.name}</a>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">27 students</td>
                                <td class="px-6 py-4 whitespace-nowrap rounded-r-md">
                                    <button class="text-blue-600 hover:text-blue-900">
                                        <i class="fa-thin fa-pen-to-square"></i>
                                    </button>
                                    <button class="text-red-600 hover:text-red-900 ml-4">
                                        <i class="fa-light fa-xmark"></i>
                                    </button>
                                </td>
                            </tr>
                        {/each}
                        </tbody>
                    </table>
                    <Paginator bind:settings={classesPaginationSettings} on:page={onPageChange}
                               on:amount={onAmountChange}
                               showFirstLastButtons={state.firstLast} showPreviousNextButtons={state.previousNext}
                               controlVariant="variant-soft bg-white"
                               select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
                </div>
            </div>
        </div>
    </div>
</template>
<style>
    .error {
        color: red;
    }
</style>
