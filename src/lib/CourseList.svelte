<script>
  export let university = null;
</script>

{#if university}
  <div class="course-list">
    <div class="header">
      <strong>{university.University}</strong><br />
      <span>{university.City}, {university.Country}</span><br />
      <small>Ranking mundial: {university.world_rank}</small><br />
      Cursos:
    </div>
    <ul>
      {#each university.Courses_Info as course}
        <li>
          <strong>{course.Program}</strong> ({course.Level})<br />
          {course.Duration_Years} anos - ${course.Tuition_USD}<br />
          <small>{course.course_category}</small><br />
        </li>
      {/each}
    </ul>
  </div>
{:else}
  <p class="no-selection">Clique em um pin para ver os cursos disponíveis.</p>
{/if}

<style>
  .course-list {
    font-size: 13px;
    color: #333;
    position: relative;
    z-index: 1;
  }

  .header {
    margin-bottom: 8px;
  }

  .course-list ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .course-list li {
    margin-bottom: 10px;
    border-bottom: 1px solid #eee;
    padding-bottom: 6px;
  }

  .no-selection {
    color: #777;
    font-size: 12px;
    font-style: italic;
  }
</style>
