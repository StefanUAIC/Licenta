<script lang="ts">
    import { onMount } from 'svelte';
    import type { CreatePostData, Post } from '$lib/posts_api';
    import { createPost, fetchPosts, likePost, dislikePost } from '$lib/posts_api';
    import type { ProfileSchema } from '$lib/users_api';
    import { getProfile } from '$lib/users_api';
    import { getCookie, getUserIDFromJWT } from '$lib/utils';

    let posts: (Post & { profilePicture: string })[] = [];
    let newPost = {
        title: '',
        content: ''
    };
    let user_id: number;
    let profilePromise: Promise<ProfileSchema | null>;
    let loading = true;

    onMount(async () => {
        await loadPosts();
        let access_token = getCookie('access');
        if (access_token) {
            user_id = getUserIDFromJWT(access_token);
            profilePromise = fetchProfile(user_id);
        } else {
            profilePromise = Promise.resolve(null);
        }
    });

    const loadPosts = async () => {
        const fetchedPosts = await fetchPosts();
        posts = await Promise.all(fetchedPosts.map(async (post) => {
            const profile = await fetchProfile(post.author_id);
            return {
                ...post,
                profilePicture: profile?.profile_picture
                    ? `data:${profile.profile_picture.type};base64,${profile.profile_picture.data}`
                    : '/default-profile-picture.png'
            };
        }));
    };

    const fetchProfile = async (user_id: number): Promise<ProfileSchema | null> => {
        try {
            const data = await getProfile(user_id);
            return data;
        } catch (err) {
            console.error('Failed to load profile:', err);
            return null;
        } finally {
            loading = false;
        }
    };

    const addPost = async () => {
        if (newPost.title.trim() !== '' && newPost.content.trim() !== '') {
            try {
                const post: CreatePostData = {
                    title: newPost.title,
                    content: newPost.content
                };
                const createdPost = await createPost(post);
                alert('Postare creată cu succes! Acum așteaptă să o verifice administratorul.');
                newPost.title = '';
                newPost.content = '';
                await loadPosts();
            } catch (error) {
                console.error('Error creating post:', error);
                alert('Failed to create post. Only teachers can create posts.');
            }
        }
    };

    const handleLike = async (postId: number) => {
        try {
            await likePost(postId);
            await loadPosts();
        } catch (error) {
            console.error('Error liking post:', error);
            alert('Failed to like post.');
        }
    };

    const handleDislike = async (postId: number) => {
        try {
            await dislikePost(postId);
            await loadPosts();
        } catch (error) {
            console.error('Error disliking post:', error);
            alert('Failed to dislike post.');
        }
    };

    function formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toLocaleDateString('ro-RO', { year: 'numeric', month: 'long', day: 'numeric' });
    }
</script>

<style>
    .post-container {
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .profile-picture {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        object-fit: cover;
    }
    .likes-dislikes {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .divider {
        height: 24px;
        width: 1px;
        background-color: #D1D5DB;
    }
    .input-container {
        position: relative;
        margin-bottom: 1rem;
    }
    .input-container input,
    .input-container textarea {
        width: 100%;
        padding: 0.75rem;
        padding-left: 3rem;
        border: 1px solid #D1D5DB;
        border-radius: 0.25rem;
        font-size: 1.1rem;
    }
    .input-container label {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #6B7280;
        pointer-events: none;
        transition: 0.2s ease all;
        font-size: 1.1rem;
    }
    .input-container textarea + label {
        top: 1rem;
        transform: none;
    }
    .input-container input:focus + label,
    .input-container textarea:focus + label,
    .input-container input:not(:placeholder-shown) + label,
    .input-container textarea:not(:placeholder-shown) + label {
        top: -0.5rem;
        font-size: 0.875rem;
        background-color: white;
        padding: 0 0.25rem;
    }
    .post-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .post-content {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .post-date {
        color: #9CA3AF;
        font-size: 0.875rem;
        text-align: right;
    }
</style>

<div class="post-container">
    {#await profilePromise}
        <p>Loading profile...</p>
    {:then profile}
        {#if profile}
            <div class="flex items-center mb-4">
                {#if profile.profile_picture}
                    <img src={`data:${profile.profile_picture.type};base64,${profile.profile_picture.data}`} alt="Profile" class="profile-picture mr-4">
                {:else}
                    <img src="/default-profile-picture.png" alt="Profile" class="profile-picture mr-4">
                {/if}
                <div class="input-container flex-grow">
                    <input type="text" id="title" bind:value={newPost.title} placeholder=" ">
                    <label for="title">Title</label>
                </div>
            </div>
            <form on:submit|preventDefault={addPost}>
                <div class="input-container">
                    <textarea id="content" bind:value={newPost.content} placeholder=" " rows="4"></textarea>
                    <label for="content">Content</label>
                </div>
                <button type="submit" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 text-lg">Post</button>
            </form>
        {:else}
            <p>Profile not available. Please log in.</p>
        {/if}
    {:catch error}
        <p>Error loading profile: {error.message}</p>
    {/await}
</div>

<div class="mt-8">
    {#each posts as post (post.id)}
        <div class="post-container">
            <div class="flex items-center mb-4">
                <img src={post.profilePicture} alt="Author" class="profile-picture mr-4">
                <div>
                    <h3 class="post-title text-3xl">{post.title}</h3>
                    <span class="text-lg"> Postat de: {post.author}</span>
                </div>
            </div>

            <p class="post-content">{post.content}</p>
            <div class="flex justify-between items-end">
                <div class="likes-dislikes">
                    <button on:click={() => handleLike(post.id)} class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-1" viewBox="0 0 20 20" fill={"currentColor"} stroke="currentColor">
                            <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                        </svg>
                        <span class="text-lg">69</span>
                    </button>
                    <div class="divider"></div>
                    <button on:click={() => handleDislike(post.id)} class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-1" viewBox="0 0 20 20" fill={"none"} stroke="currentColor">
                            <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
                        </svg>
                        <span class="text-lg">69</span>
                    </button>
                </div>
                <div class="post-date">
                    {formatDate(post.created_at)}
                </div>
            </div>
        </div>
    {/each}
</div>
