<script>
  let posts = [
    { id: 1, title: 'Post Title 1', content: 'Post content 1' },
    { id: 2, title: 'Post Title 2', content: 'Post content 2' },
  ];

  let newPost = {
    title: '',
    content: ''
  };

  function addPost() {
    if (newPost.title.trim() !== '' && newPost.content.trim() !== '') {
      const post = {
        id: posts.length + 1,
        title: newPost.title,
        content: newPost.content
      };
      posts = [...posts, post];
      newPost.title = '';
      newPost.content = '';
    }
  }
</script>

<div class="bg-white shadow-md rounded-lg p-6">
  <h3 class="text-xl font-bold mb-4">Add a new post</h3>
  <form on:submit|preventDefault={addPost}>
    <div class="mb-4">
      <label for="title" class="block mb-2">Title:</label>
      <input type="text" id="title" bind:value={newPost.title} class="w-full border border-gray-300 rounded-lg px-4 py-2">
    </div>
    <div class="mb-4">
      <label for="content" class="block mb-2">Content:</label>
      <textarea id="content" bind:value={newPost.content} class="w-full border border-gray-300 rounded-lg px-4 py-2"></textarea>
    </div>
    <button type="submit" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">Add post</button>
  </form>
</div>

<div class="mt-8">
  {#each posts as post (post.id)}
    <div class="bg-white shadow-md rounded-lg p-6 mb-4">
      <h3 class="text-xl font-bold mb-2">{post.title}</h3>
      <p>{post.content}</p>
    </div>
  {/each}
</div>