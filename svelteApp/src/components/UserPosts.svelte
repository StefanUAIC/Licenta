<script lang="ts">
	import { onMount } from 'svelte';
	import type { CreatePostData, Post } from '$lib/posts_api';
	import { createPost, fetchPosts } from '$lib/posts_api';
	import { writable } from 'svelte/store';

	let posts: Post[] = [];
	let newPost = {
		title: '',
		content: ''
	};
	let isTeacher = writable(false);

	export let userIsTeacher = false;

	onMount(async () => {
		posts = await fetchPosts();
		isTeacher.set(userIsTeacher);
	});

	const addPost = async () => {
		if (newPost.title.trim() !== '' && newPost.content.trim() !== '') {
			try {
				const post: CreatePostData = {
					title: newPost.title,
					content: newPost.content
				};
				const createdPost = await createPost(post);
				posts = [createdPost, ...posts];
				newPost.title = '';
				newPost.content = '';
			} catch (error) {
				console.error('Error creating post:', error.message);
				alert('Failed to create post. Only teachers can create posts.');
			}
		}
	};
</script>

<style>
    .bg-white {
        background-color: white;
    }

    .shadow-md {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .rounded-lg {
        border-radius: 0.5rem;
    }

    .p-6 {
        padding: 1.5rem;
    }

    .mb-4 {
        margin-bottom: 1rem;
    }

    .w-full {
        width: 100%;
    }

    .border {
        border-width: 1px;
    }

    .border-gray-300 {
        border-color: #D1D5DB;
    }

    .px-4 {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .py-2 {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }

    .bg-indigo-600 {
        background-color: #4F46E5;
    }

    .text-white {
        color: white;
    }

    .px-6 {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    .hover\:bg-indigo-700:hover {
        background-color: #4338CA;
    }

    .mt-8 {
        margin-top: 2rem;
    }
</style>

<div class="bg-white shadow-md rounded-lg p-6">
	<h3 class="text-xl font-bold mb-4">Add a new post</h3>
	{#if $isTeacher}
		<form on:submit|preventDefault={addPost}>
			<div class="mb-4">
				<label for="title" class="block mb-2">Title:</label>
				<input type="text" id="title" bind:value={newPost.title}
					   class="w-full border border-gray-300 rounded-lg px-4 py-2">
			</div>
			<div class="mb-4">
				<label for="content" class="block mb-2">Content:</label>
				<textarea id="content" bind:value={newPost.content}
						  class="w-full border border-gray-300 rounded-lg px-4 py-2"></textarea>
			</div>
			<button type="submit" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">Add post
			</button>
		</form>
	{/if}
</div>

<div class="mt-8">
	{#each posts as post (post.id)}
		<div class="bg-white shadow-md rounded-lg p-6 mb-4">
			<h3 class="text-xl font-bold mb-2">{post.title}</h3>
			<p>{post.content}</p>
		</div>
	{/each}
</div>
