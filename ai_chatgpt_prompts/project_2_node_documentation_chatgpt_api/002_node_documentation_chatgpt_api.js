/* 

002_node_documentation_chatgpt_api.js

cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_2_node_documentation_chatgpt_api/


node 002_node_documentation_chatgpt_api.js

*/
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
        prompt: "Extract keywords from this text:\n\nBlack-on-black ware is a 20th- and 21st-century pottery tradition developed by the Puebloan Native American ceramic artists in Northern New Mexico. Traditional reduction-fired blackware has been made for centuries by pueblo artists. Black-on-black ware of the past century is produced with a smooth surface, with the designs applied through selective burnishing or the application of refractory slip. Another style involves carving or incising designs and selectively polishing the raised areas. For generations several families from Kha'po Owingeh and P'ohwhóge Owingeh pueblos have been making black-on-black ware with the techniques passed down from matriarch potters. Artists from other pueblos have also produced black-on-black ware. Several contemporary artists have created works honoring the pottery of their ancestors.",
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


/* 
Keywords: Black-on-black ware, 20th century, 21st century, Puebloan Native American ceramic artists, Northern New Mexico, reduction-fired blackware, pueblo artists, selective burnishing, refractory slip, carving/incising designs, polishing
*/

/*
-Black-on-black ware 
-Puebloan Native American 
-Ceramic Artists 
-Northern New Mexico 
-Reduction Fired Blackware 
-Smooth Surface 
-Selective Burnishing/Refractory Slip  
-Car
*/

    }// EOF


DoKeywordsFromText();
