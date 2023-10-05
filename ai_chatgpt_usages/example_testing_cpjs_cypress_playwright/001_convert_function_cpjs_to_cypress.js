// 001_convert_function_cpjs_to_cypress.js
// source for GPT query
// Convert function written in Codeceptjs to Cypress:

// FUNCTION_1

CrawAddWireImage () {

    I.say('--- CrawAddWireImage :: CSS_WIRE_IMAGE:: '+globalValues.CSS_WIRE_IMAGE+'');

        // Add a media
    I.say('--- Add a media image '+globalVariables.RandomImageInsert+' ');
    // I.click('//*[@id="media-image"]/div[2]/button[4]');
    I.click('//*[@id="media-image"]/div[2]/button[5]');

    // remove time scope for image
    Functions.RemoveTimeScopeForImage();
        
    // pause();

    // select random image
    I.click('//*[@id="'+globalValues.CSS_WIRE_IMAGE+'"]/div/div[2]/div/div[2]/div[3]/div[2]/a['+globalVariables.RandomImageInsert+']/img');


    // medium_title
    I.waitForElement('//*[@id="medium_title"]', 5);
    I.fillField('//*[@id="medium_title"]', ''+globalValues.MEDIUM_TITLE+''+globalVariables.RandomString+'');


    // medium_caption
    I.waitForElement('//*[@id="medium_caption"]', 5);
    I.fillField('//*[@id="medium_caption"]', ''+globalValues.MEDIUM_CAPTION+' '+globalVariables.RandomString+'');


    // medium_copyright
    I.waitForElement('//*[@id="medium_copyright"]', 5);
    I.fillField('//*[@id="medium_copyright"]', ''+globalValues.MEDIUM_COPYRIGHT+' '+globalVariables.RandomString+'');



    // medium_copyrightUrl
    I.waitForElement('//*[@id="medium_copyrightUrl"]', 5);
    I.fillField('//*[@id="medium_copyrightUrl"]', ''+globalValues.MEDIUM_COPYRIGHTURL+' '+globalVariables.RandomString+'');

    I.click('//*[@id="'+globalValues.CSS_WIRE_IMAGE+'"]/div/div[1]/div[2]/div/form/div[2]/button[1]');

    
   },

// FUNCTION_2

   RemoveTimeScopeForImage () {

    // remove time scope for image
    I.say('--- Remove time scope for image selection', 'red');
    I.fillField('//*[@id="media_search_pubDateStart"]', ''+globalValues.IMAGES_DIRECTORY_PUB_DATE_START+'');
    I.pressKey("Enter");
    I.fillField('//*[@id="media_search_pubDateEnd"]', ''+globalValues.IMAGES_DIRECTORY_PUB_DATE_END+'');
    I.pressKey("Enter");
    I.click('//*[@id="media_search_submit"]');
    I.wait(30);

    },

