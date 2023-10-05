/* 

001_node_documentation_chatgpt_api.js

cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_2_node_documentation_chatgpt_api/


node 001_async_function.js

*/

const { globalValues } = require('./allValues');


async function myfunction() {
  console.log('Inside of myfunction');
}

// Here we wait for the myfunction to finish
// and then returns a promise that'll be waited for aswell
// It's useless to wait the myfunction to finish before to return
// we can simply returns a promise that will be resolved later

// Also point that we don't use async keyword on the function because
// we can simply returns the promise returned by myfunction
function start() {
  return myfunction();
}

// Call start
(async() => {
  console.log('before start');

  await start();
  
  console.log('after start');

  // Debug
  console.log (globalValues.TOTEM_SHRUG_MAN_SIMPLE_CHAT_GPT)
  console.log (globalValues.OPENAI_ORGANIZATION)
  console.log (globalValues.OPENAI_API_KEY)



})();




