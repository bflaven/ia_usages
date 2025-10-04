

## Security Note: API Keys Are Not Exported in n8n Workflows

Based on the search results, here's what happens with credentials when exporting workflows in n8n:

**No, n8n workflow exports do NOT include actual credentials like API keys.** 

However, there are some important details to know:

## What's Included in Workflow Exports:
- Credential **names** and **IDs**
- References to which credentials are used by which nodes

## What's NOT Included:
- Actual API keys, passwords, tokens, or other sensitive credential data
- The encrypted credential values themselves

## Important Security Notes:

1. **Credential names might be sensitive**: While IDs aren't sensitive, the credential names could be, depending on how you name your credentials. For example, if you name a credential "CompanyX_Production_API_Key", that reveals information.

2. **HTTP Request nodes exception**: HTTP Request nodes may contain authentication headers when imported from cURL, so you should check and remove those before sharing.

3. **When you import a workflow**: You'll need to reconnect it to credentials in your n8n instance (either existing ones or create new ones).

So your exported JSON file will be safe to share in terms of not exposing actual secrets, but you should still review it to ensure credential names don't reveal sensitive information about your setup.


## Security Warning: Google Docs Links Are Exposed in n8n Exports

**When working with Google Sheets or similar services, be aware that direct document links are included in exported workflow JSON files. To protect sensitive information, obfuscate these links before sharing.**

**Example of link obfuscation:**

**Before (original link in JSON):**
```
# I have already
https://docs.google.com/spreadsheets/d/1xK9mP2nQwRt5vL8aYdFj3cHzN7bG6eUoI4pWsX1vM2A/edit?usp=drivesdk
```

**After (obfuscated for sharing):**
```
https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE/edit?usp=drivesdk
```

**Or use environment variables approach:**
```
https://docs.google.com/spreadsheets/d/{{$env.SPREADSHEET_ID}}/edit?usp=drivesdk
```

**Recommended obfuscation methods:**
1. Replace the document ID with a placeholder like `YOUR_SPREADSHEET_ID_HERE` or `REPLACE_WITH_YOUR_ID`
2. Use n8n environment variables (e.g., `{{$env.SPREADSHEET_ID}}`) if sharing with others who will use the workflow
3. Replace with a dummy/example ID that clearly indicates it needs to be changed
4. Document which IDs need to be replaced in a separate README file

This prevents unauthorized access to your actual Google Sheets documents while allowing others to understand the workflow structure.


