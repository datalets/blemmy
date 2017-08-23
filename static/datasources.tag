
<datasources>

  <ul>
    <li each={ items }>
      <a href={ homepage }>
        { title }
      </a>
    </li>
  </ul>

  <script>
    this.items = opts.items
  </script>

</datasources>
