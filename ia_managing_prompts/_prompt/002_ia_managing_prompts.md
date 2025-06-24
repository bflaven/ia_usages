

## PROMPT_1

As a python developer, can you add in the file "registry.html" the ability to edit the prompt in a column "Action", at the end of the columns "System", "User", "Keywords", "Connector".




## PROMPT_2
For the field id="user" in edit_prompt.html can you detect if some values are written in Jinja2 format and then convert below the fields in fields in a section namled "Input Variable Sets" e.g {{content}}, {{lang}}... etc


## PROMPT_3
Extract from the following code :
1. put the h3 outside the div input-vars-section
2. For each input-vars-list, create a specific field e.g for {{content}}, on the right, the title is "content" and at the right of the title, you have a field where the user can type a value then the same; for {{lang}}, on the right, the title is "lang" and at the right of the title, you have a field where the user can type a value then the same for {{lang}} do the same pattern of any pseudo variables that can be inserted.

```html
<!-- Input Variable Sets Section -->
            <div class="input-vars-section" id="input-vars-section" style="display:none;">
                <h3>Input Variable Sets</h3>
                <ul class="input-vars-list" id="input-vars-list"></ul>
            </div>
```

## PROMPT_3
Extract from the following code :
1. put the h3 outside the div input-vars-section
2. For each input-vars-list, create a specific field e.g for {{content}}, on the right, the title is "content" and at the right of the title, you have a field where the user can type a value then the same; for {{lang}}, on the right, the title is "lang" and at the right of the title, you have a field where the user can type a value then the same for {{lang}} do the same pattern of any pseudo variables that can be inserted.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Prompt</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        .input-vars-section {
            margin-top: 0;
            background: #f9fafb;
            border-radius: 8px;
            padding: 14px 18px;
            border: 1px solid #e5e7eb;
        }
        .input-vars-title {
            margin-top: 18px;
            margin-bottom: 0.5em;
            color: #f97316;
            font-size: 1.1em;
            display: none;
        }
        .input-var-row {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            gap: 12px;
        }
        .input-var-label {
            min-width: 80px;
            font-weight: 500;
            color: #f97316;
        }
        .input-var-input {
            flex: 1;
            padding: 7px 10px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            font-size: 1em;
            background: #f9fafb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Edit Prompt</h2>
        <form method="post" class="form-block">
            <div class="form-group">
                <label for="system">System Prompt:</label>
                <textarea id="system" name="system" required>{{ prompt.system }}</textarea>
            </div>
            <div class="form-group">
                <label for="user">User Prompt:</label>
                <textarea id="user" name="user" required oninput="updateInputVars()">{{ prompt.user }}</textarea>
            </div>
            <!-- Input Variable Sets Title and Section -->
            <h3 class="input-vars-title" id="input-vars-title">Input Variable Sets</h3>
            <div class="input-vars-section" id="input-vars-section" style="display:none;">
                <form id="input-vars-form"></form>
            </div>
            <div class="form-group">
                <label for="keywords">Keywords (comma-separated):</label>
                <input type="text" id="keywords" name="keywords" value="{{ prompt.keywords }}" required>
            </div>
            <div class="form-group">
                <label for="connector_id">Connector:</label>
                <select id="connector_id" name="connector_id" required>
                    {% for connector in connectors %}
                        <option value="{{ connector.id }}"
                            {% if connector.id == prompt.connector_id %}selected{% endif %}>
                            {{ connector.llm_provider }} / {{ connector.model }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-actions">
                <button type="submit">Save Changes</button>
                <a href="/"><button type="button">Cancel</button></a>
            </div>
        </form>
    </div>
    {% raw %}
    <script>
        function extractJinjaVars(text) {
            // Match {{variable}} or {{ variable }}
            const regex = /{{\s*([\w\.]+)\s*}}/g;
            let match;
            const vars = new Set();
            while ((match = regex.exec(text)) !== null) {
                vars.add(match[1]);
            }
            return Array.from(vars);
        }

        function updateInputVars() {
            const userField = document.getElementById('user');
            const inputVarsSection = document.getElementById('input-vars-section');
            const inputVarsForm = document.getElementById('input-vars-form');
            const inputVarsTitle = document.getElementById('input-vars-title');
            const text = userField.value;
            const vars = extractJinjaVars(text);

            if (vars.length > 0) {
                inputVarsSection.style.display = '';
                inputVarsTitle.style.display = '';
                inputVarsForm.innerHTML = '';
                vars.forEach(v => {
                    const row = document.createElement('div');
                    row.className = 'input-var-row';

                    const label = document.createElement('span');
                    label.className = 'input-var-label';
                    label.textContent = v;

                    const input = document.createElement('input');
                    input.className = 'input-var-input';
                    input.type = 'text';
                    input.name = v;
                    input.placeholder = `Enter value for ${v}`;

                    row.appendChild(label);
                    row.appendChild(input);
                    inputVarsForm.appendChild(row);
                });
            } else {
                inputVarsSection.style.display = 'none';
                inputVarsTitle.style.display = 'none';
                inputVarsForm.innerHTML = '';
            }
        }

        // Run on page load
        document.addEventListener('DOMContentLoaded', updateInputVars);
    </script>
    {% endraw %}
</body>
</html>

```

## PROMPT_3
From the user field "Rédigez un article en {{lang}} de blog avec 3 à 5 titres et 3 à 5 paragraphes sur le {{topic}} donné." The div is empty. Can you fix the problem. I would like to see this output where the user can type whatever he wants.
```html
lang : <input type="text" id="lang" name="lang" value=""> 
topic : <input type="text" id="topic" name="topic" value="">
``` 
```html
<div class="input-vars-section" id="input-vars-section">
<!-- Example fields will be dynamically generated here -->
</div>
