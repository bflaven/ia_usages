## PROMPT_1

As a PHP expert and a WordPress plugin expert, can you create a plugin that will enable in the WordPress API all types below e.g `https://flaven.fr/wp-json/wp/v2/types`. Here is the types that I want to see active in the API.

```text
posts: 657
pages: 15
categories: 103
tags: 2475

# custom post-type
bf_videos_manager: 106
bf_quotes_manager: 65
clients: 63
product_for_sale: 47

# custom taxonomies
bf_videos_manager_tag: 170
bf_videos_manager_cat: 17
bf_quotes_manager_author: 53
bf_quotes_manager_flavor: 261

product_for_sale_kw: 32
product_for_sale_author: 68
```



```php
add_action( 'init', function() {
    register_post_type( 'book', [
        'public' => true,
        'show_in_rest' => true,
        'label' => 'Books'
    ]);
});
```








