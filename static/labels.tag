
<labels>

  <ul>
    <li each={ items }>
      <img src={ imageurl } />
      <a href={ homepage }>
        { title }
      </a>
    </li>
  </ul>

  <script>
    this.items = opts.items
  </script>

</labels>
