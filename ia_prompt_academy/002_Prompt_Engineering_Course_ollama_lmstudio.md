# 002_Prompt_Engineering_Course_ollama.md

## OLLAMA PROMPTS EXAMPLES with codellama


## OLLAMA PROMPTS EXAMPLES with codellama
Some examples given by ollama with `codellama`. A large language model that can use text prompts to generate and discuss code.

**Using codellama**
Code Llama is a model for generating and discussing code, built on top of Llama 2. It’s designed to make workflows faster and efficient for developers and make it easier for people to learn how to code. It can generate both code and natural language about code. Code Llama supports many of the most popular programming languages used today, including Python, C++, Java, PHP, Typescript (Javascript), C#, Bash and more.

*Most of the time, I test the code produced in Pyhton in a Jupyter Notebook, see 001_prompt_engineering_course.ipynb*

- Check the LLM  [https://ollama.ai/library/codellama](https://ollama.ai/library/codellama)
- Read How to prompt Code Llama [https://ollama.ai/blog/how-to-prompt-code-llama](https://ollama.ai/blog/how-to-prompt-code-llama)

**Ollama commands reminder**

```bash
# To run and chat with Llama 2
ollama run llama2
ollama run codellama:7b



# To run and chat with orca-mini
ollama run orca-mini
ollama pull orca-mini
ollama run codellama:7b

# remove a model
ollama rm llama2
ollama rm orca-mini
ollama rm codellama:7b
ollama rm codellama:7b-python


# list the model
ollama list


# when you are in the model you can use
>>> /?
>>> /list
>>> /set verbose

# to get out from the model
/exit
```

**Instruct**
```bash
# if you are already in the codallama LLM
# Prompt:
Write me a function that outputs the fibonacci sequence

# by default is writting in javascript
# Output:
function fibonacci(n) {
  if (n <= 1) {
    return n;
  } else {
    return fibonacci(n-1) + fibonacci(n-2);
  }
}

// Test the function with different values of n
console.log(fibonacci(0)); // 0
console.log(fibonacci(1)); // 1
console.log(fibonacci(2)); // 1
console.log(fibonacci(3)); // 2
console.log(fibonacci(4)); // 3
console.log(fibonacci(5)); // 5
console.log(fibonacci(6)); // 8
console.log(fibonacci(7)); // 13
console.log(fibonacci(8)); // 21
console.log(fibonacci(9)); // 34
console.log(fibonacci(10)); // 55

// Time complexity of the function: O(n)
// The time complexity of the recursive solution for the Fibonacci sequence is O(n), because each call to 
the function requires a constant amount of time to calculate, regardless of the value of n.
```


**Prompt**
You are an expert programmer that writes simple, concise code and explanations. Write a python function to show randomly a single quote from a list of 10 random quotes. Took a sample of the most common quotes about topics like Luck, Achievement and Work in general.

**Output**

Here is a Python function that takes in a list of 10 random quotes and randomly selects and 
returns one quote:
```
import random

def get_random_quote(quotes):
    return random.choice(quotes)
```
This function uses the `random` module to select a random element from the `quotes` list, which is
passed in as an argument. The `random.choice()` function returns a randomly selected element from 
the list, so this function will always return a different quote each time it is called.

Here is an example of how you could use this function:
```
# Create a list of 10 random quotes
quotes = ['Luck is what happens when preparation meets opportunity.', 'The greatest glory in 
living lies not in never falling, but in rising every time we fall.', 'The best way to predict the
future is to invent it.']

# Call the get_random_quote function and print the result
print(get_random_quote(quotes))
```
This will randomly select one of the three quotes from the `quotes` list and print it to the 
console.



**Prompt**
Write in PHP, a Wordpress plugin with comments, named "MySocialBuddy". This Plugin "MySocialBuddy" will add a new entry in the main administration menu in "Settings". The name of the entrance will be "MySocialBuddy". The purpose of this plugin is to manipulate 1 custom fields for social network accounts: mysocialbuddy_linkedin. You can you write also tips for this field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.
 

Here is an example of how you could create a WordPress plugin with comments, named "MySocialBuddy", that adds a new entry in the main administration menu in "Settings" and allows users to manipulate 1 custom field for social network accounts:

``` php
<?php
/*
Plugin Name: MySocialBuddy
Description: A plugin to manipulate custom fields for social network accounts.
Version: 1.0
Author: Your Name
*/

// Register the menu item in the settings menu
function mysocialbuddy_add_menu() {
    add_options_page('MySocialBuddy', 'My Social Buddy', 'manage_options', 'mysocialbuddy', 
'mysocialbuddy_settings');
}
add_action('admin_menu', 'mysocialbuddy_add_menu');

// Function to render the settings page for MySocialBuddy
function mysocialbuddy_settings() {
    ?>
    <div class="wrap">
        <h1>My Social Buddy Settings</h1>
        <?php if (isset($_GET['saved'])) : ?>
            <div id="message" class="updated notice is-dismissible">
                <p><strong>Settings saved.</strong></p>
            </div>
        <?php endif; ?>
        <form method="post" action="<?php echo admin_url('admin.php?page=mysocialbuddy'); ?>">
            <?php settings_fields('mysocialbuddy_options'); ?>
            <?php do_settings_sections('mysocialbuddy'); ?>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Register the setting for MySocialBuddy
function mysocialbuddy_register_setting() {
    register_setting('mysocialbuddy_options', 'mysocialbuddy_linkedin');
}
add_action('admin_init', 'mysocialbuddy_register_setting');

// Add a section to the settings page for MySocialBuddy
function mysocialbuddy_add_section() {
    add_settings_section('mysocialbuddy_section', 'My Social Buddy', 
'mysocialbuddy_section_callback', 'mysocialbuddy');
}
add_action('admin_init', 'mysocialbuddy_add_section');

// Callback function to render the section for MySocialBuddy
function mysocialbuddy_section_callback() {
    ?>
    <p>This plugin allows you to manipulate custom fields for social network accounts.</p>
    <?php
}

// Add a field to the settings page for MySocialBuddy
function mysocialbuddy_add_field() {
    add_settings_field('mysocialbuddy_linkedin', 'LinkedIn URL', 
'mysocialbuddy_render_linkedin_field', 'mysocialbuddy', 'mysocialbuddy_section');
}
add_action('admin_init', 'mysocialbuddy_add_field');

// Callback function to render the field for MySocialBuddy
function mysocialbuddy_render_linkedin_field() {
    $option = get_option('mysocialbuddy_linkedin');
    ?>
    <input type="text" id="<?php echo esc_attr( $option ); ?>" name="mysocialbuddy_linkedin" 
value="<?php echo esc_attr( $option ); ?>">
    <?php
}
```
This plugin will add a new entry in the main administration menu in "Settings" called "MySocialBuddy". When you click on this link, it will take you to the settings page for MySocialBuddy, where you can manipulate 1 custom field for social network accounts:  mysocialbuddy_linkedin. This field will be rendered as a text input, and you can enter the URL of your LinkedIn profile in this field.

The plugin will also display a message at the top of the settings page if the settings have been saved successfully.

This is just an example code and you should modify it according to your needs. Also, please note that you should replace "Your Name" with your name and "mysocialbuddy_linkedin" with the actual name of the custom field you want to use.





