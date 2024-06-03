<script>
  import '../app.css';
  import { AppShell } from '@skeletonlabs/skeleton';
</script>

<AppShell slotSidebarLeft="bg-surface-500/5 w-56 p-4">
  <svelte:fragment slot="sidebarLeft">
    <nav class="list-nav fixed top-0 left-0 w-56 h-full bg-surface-500/5 z-50 p-4">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Register</a></li>
        <li><a href="/compiler">Compiler</a> </li>
      </ul>
    </nav>
  </svelte:fragment>

  <slot></slot>
</AppShell>
