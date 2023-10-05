/* 

004_change_node_documentation_chatgpt_api.js

cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_2_node_documentation_chatgpt_api/


node 004_change_node_documentation_chatgpt_api.js

+ GREAT EXAMPLE FROM OPENAI.COM
https://platform.openai.com/examples




*/
//
const { globalValues } = require('./allValues');
const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  organization: globalValues.OPENAI_ORGANIZATION,
  apiKey:  globalValues.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

    async function DoKeywordsFromText () {

      const response = await openai.createCompletion({
        model: "text-davinci-003",
        prompt: "Extract keywords from this text:\n\nZumbi (1655 – November 20, 1695), also known as Zumbi dos Palmares, was a Brazilian quilombola leader, being one of the pioneers of resistance to slavery of Africans by the Portuguese in colonial Brazil. He was also the last of the kings of the Quilombo dos Palmares, a settlement of Afro-Brazilian people who had liberated themselves from enslavement, in the present-day state of Alagoas, Brazil. Zumbi today is revered in Afro-Brazilian culture as a powerful symbol of resistance against the enslavement of Africans in the colony of Brazil.", 
        temperature: 0.5,
        max_tokens: 60,
        top_p: 1.0,
        frequency_penalty: 0.8,
        presence_penalty: 0.0,
      });

      // debug
      // console.log(response)
      
      console.log('\n');
      console.log('\n--- ChatGPT');
      console.log(response.data.choices[0].text);
      console.log('\n');

    }// EOF


DoKeywordsFromText();
