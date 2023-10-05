/* 

# INSTALL
npm install
npm i openai


001_node_documentation_chatgpt_api.js

cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_2_node_documentation_chatgpt_api/


node 001_node_documentation_chatgpt_api.js

*/

const { globalValues } = require('./allValues');

const { Configuration, OpenAIApi } = require("openai");
require('dotenv').config()

const configuration = new Configuration({
  organization: globalValues.OPENAI_ORGANIZATION,
  apiKey:  globalValues.OPENAI_API_KEY,


});
const openai = new OpenAIApi(configuration);

async function runCompletion () {
const completion = await openai.createCompletion({
  model: "text-davinci-003",
  prompt: "How are you today?",
  // prompt: "Can you make programming for me sometimes?",

});
console.log('\n');
console.log('\n--- ChatGPT answer'+ completion.data.choices[0].text);
console.log('\n');

}

runCompletion();

