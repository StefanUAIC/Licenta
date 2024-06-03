<script>
  let title = "Welcome to My Home Page";
</script>

<main>
  <h1>{title}</h1>
  <p>This is a basic home page created in Svelte.</p>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
    background-color: #f5f5f5;
  }

  h1 {
    font-size: 2.5em;
    color: #333;
  }

  p {
    font-size: 1.2em;
    color: #666;
  }
</style>