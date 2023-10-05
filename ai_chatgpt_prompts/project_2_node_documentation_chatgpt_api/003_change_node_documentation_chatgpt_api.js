/* 

003_change_node_documentation_chatgpt_api.js

cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_2_node_documentation_chatgpt_api/


node 003_change_node_documentation_chatgpt_api.js

+ GREAT EXAMPLE FROM OPENAI.COM
https://platform.openai.com/examples

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
        prompt: "Extract keywords from this text:\n\n I know the title sound like a clickbait, and I was about to use the F word in it, but I gave up! So, let’s start with some banalities: I am often bedeviled by an intense curiosity for a subject. This blog is living proof of that. Responding to this imperative to satisfy this curiosity always leaves me bewildered… What’s the point of investigate all this when in the end you can satisfy to be ignorant and claim it? Most of the topics below are explored for simplicity more than exhaustivity. So, I will certainly state the obvious on these subjects. It also gave a better understanding of Friedrich Nietzsche quote: Blessed are the sleepy ones: for they shall soon nod off. Anyway, my two last top-of-mind professional concerns were: The first concern was that I wanted to extend some Cypress tests to performance testing (Frontend performance or Backend performance) more than functional testing. The second was I wanted to test also some required Javascript files such Google Analytics or Google Tag Manager with Cypress preferably. The constrain was simple: “Can I do it with Cypress only and not with a tedious integration of new tool or framework for such performance testing?” As it is p… in the a… to manage several tool Ooops!Anyway, during this exploration, I had the chance to document. For instance, I always try to figure out the time spent to learn a dedicated tool (K6) vs the time spent to tinker an existing and well understood (Cypress) with no success guaranteed. You see the point?\ For sure, it’s when you begin to master a tool that you see its limits. As often, thanks to an event (bug, regression, error…), you cruelly realize limits and fragility for your hard-won knowledge!\ Thus, I master a little Cypress and I now see that this framework that I use for E2E tests is not really intended to do anything else! Choosing and investing in a new tool represents a tremendous cost for a team. In my case, the constraint that applies is once Cypress has been chosen, it must at least be kept. I know that the grass is always greener elsewhere and I know also that novelty is the modern bait. Of course, it would be tempting to choose another tool like K6 or to change the E2E framework once again and choose Playwright, for example, which is the latest test framework I have heard of. It is true that after reading a few articles;", 
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

/*
        // It seems obvious that what I was trying to do was obviously more like load testing or performance testing than functional testing!


        // All my knowledge come from this article! Load testing principle I have grabbed some explanations on K6 website, a very famous loading test framework and so a great source of information. The main question is What are the load testing approaches possible? written above, it is overall logical in terms of scheduling.
*/

    }// EOF


DoKeywordsFromText();
