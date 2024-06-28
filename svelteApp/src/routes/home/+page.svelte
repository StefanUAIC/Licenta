<script>
  import { onMount } from 'svelte';
  import { AppShell } from '@skeletonlabs/skeleton';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import Waves_2 from '../../components/Waves_3.svelte';

  import { getStudentCount, getTeacherCount } from '$lib/users_api';

  let studentCount = 0;
  let teacherCount = 0;

  const tweetedStudentCount = tweened(0, {
    duration: 2000,
    easing: cubicOut
  });

  const tweetedTeacherCount = tweened(0, {
    duration: 2000,
    easing: cubicOut
  });

  onMount(() => {
    studentCount = getStudentCount();
    teacherCount = getTeacherCount();

    tweetedStudentCount.set(studentCount);
    tweetedTeacherCount.set(teacherCount);
  });

  const pages = [
    { name: 'Postări', icon: 'fas fa-blog', href: '/posts' },
    { name: 'Probleme', icon: 'fas fa-tasks', href: '/problems' },
    { name: 'Clasament', icon: 'fas fa-trophy', href: '/leaderboards' },
    { name: 'Clasele tale', icon: 'fas fa-users', href: '/classes' },
    { name: 'Profil', icon: 'fas fa-user', href: '/profile' },
  ];
</script>

<AppShell>
  <div class="relative h-full bg-indigo-600">
    <div class="waves-container h-full absolute inset-0 z-0">
      <Waves_2 />
    </div>
    <div class="container mx-auto px-4 py-8 relative z-10">
      <div class="flex flex-col items-center mb-12">
        <div class="logo-container w-1/4 aspect-square rounded-full shadow-2xl mb-6 flex items-center justify-center bg-white bg-opacity-25">
          <img src="/logo.png" alt="Logo" class="w-full h-full object-contain p-2"/>
        </div>
        <div class="bg-white p-3 rounded-tr-3xl rounded-bl-3xl">
          <h1 class="text-5xl font-bold text-blue-600">CodeLegends</h1>
        </div>
      </div>

      <div class="flex justify-center items-center space-x-16 mb-16">
        <div class="text-center">
          <p class="text-6xl font-bold mb-2 text-white">{$tweetedStudentCount.toFixed(0)}</p>
          <p class="text-3xl text-white">Studenți</p>
        </div>
        <div class="h-24 w-px bg-white"></div>
        <div class="text-center">
          <p class="text-6xl font-bold mb-2 text-white">{$tweetedTeacherCount.toFixed(0)}</p>
          <p class="text-3xl text-white">Profesori</p>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {#each pages as page}
          <a href={page.href} class="flex flex-col items-center justify-center p-4 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition-colors duration-200 aspect-square">
            <i class="{page.icon} text-5xl mb-2 text-white"></i>
            <span class="text-center text-white text-2xl font-medium">{page.name}</span>
          </a>
        {/each}
      </div>
    </div>
  </div>
</AppShell>

<style>
  .waves-container {
    background-color: #4f46e5;
  }

  .logo-container {
    backdrop-filter: blur(7px);
  }

  /* Adăugați orice alte stiluri specifice aici */
</style>