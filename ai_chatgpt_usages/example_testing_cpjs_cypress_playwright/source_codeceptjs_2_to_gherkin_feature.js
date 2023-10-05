
// GPT query ::  Convert the following code from CodeceptJS to Gherkin syntax: 

I.say('\n--- CREATE WIRE');

    I.click('//*[@id="content--create"]');
    
    // Fill title
    I.fillField('//*[@id="wire_title"]', ''+globalVariables.startDateString+' Test Wire title CodeceptJS '+globalVariables.RandomString+' '); 

    
    // Save as draft
    I.click('//*[@id="wire_save"]');
    I.wait(20);
    // I.waitForElement('//*[@id="article_slug"]', 20);
    I.refreshPage();

    // Test
    I.say('\n--- '+globalValues.TOTEM_TEST_MAN+'', 'red');
    // I.say('--- Check if the save action has worked  see '+globalVariables.RandomString+' in title');
    // I.seeInField({xpath: '//*[@id="wire_title"]'}, ''+globalVariables.RandomString+'');
    I.say('--- Content saved');



            // Default Photo
            if (globalValues.IMAGES_DIRECTORY_STATUS == 'empty') {
 

                I.say('--- IMAGES_DIRECTORY_STATUS is EMPTY' , 'red');  


            } else if (globalValues.IMAGES_DIRECTORY_STATUS == 'old') {

                I.say('--- IMAGES_DIRECTORY_STATUS is OLD' , 'red');  

                    //Image
                    Functions.BachAddWireImage();

            } else {
                I.say('--- IMAGES_DIRECTORY_STATUS is OK' , 'red');  

                    //Image
                    Functions.BachAddWireImage();
    }


    // Save as draft
    I.click('//*[@id="wire_save"]');
    I.wait(10);



    // Back
    I.say('--- No test for URL', 'red');   
    // Create a slug with title and keywords      
    I.checkOption('//*[@id="radio-PUBLISHED"]');
    // I.fillField('//*[@id="wire_canonicalUri_location"]', 'Test slug CodeceptJS '+globalVariables.RandomString+' '+globalValues.KEYWORDS_LIST_SLUG+'');

    // Save as PUBLISHED
    I.waitForElement('//*[@id="wire_save"]', 20);
    I.click('//*[@id="wire_save"]');
    I.wait(10);
    I.waitForElement('//*[@id="radio-PUBLISHED"]', 20);