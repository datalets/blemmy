<raw>
  <span></span>
  this.root.innerHTML = opts.content
</raw>

<farms>

  <div class="container">
  	<div class="row">
  		<section class="6u 12u(narrower)">
        <div class="box post" each={ items }>
          <a href={ meta.detail_url } target="_blank" class="image left">
            <img src={ image_thumb.url } alt="">
          </a>
          <div class="inner">
            <h3>{ title }</h3>
            <p><raw content={ about }></p>
          </div>
        </div>
      </section>
    </div>
  </div>

  <script>
    this.items = opts.items
  </script>

</farms>
