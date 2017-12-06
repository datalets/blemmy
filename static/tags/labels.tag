
<labels>

  <ul>
    <li each={ items }>
      <span class="icon" style="background-image:url({ imageurl })"></span>
      <a href={ homepage }>
        { title }
      </a>
    </li>
  </ul>

  <script>
    this.items = opts.items
  </script>

</labels>
