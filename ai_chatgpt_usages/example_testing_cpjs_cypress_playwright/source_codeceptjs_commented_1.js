// source_codeceptjs_commented_1.js
// source for GPT query
// Convert function written in Codeceptjs to Cypress. Source codeceptjs commented by GPT

// Importing constants, functions, and classes needed for the scenario
const { globalVariables, globalValues, Login, Edition, Article, Functions, AdvancedLogin } = inject();

// Defining the scenario to check the back office of BACH and schedule an article
Scenario('03 :: Check CRAW Backoffice :: ARTICLE :: SCHEDULED', async (I, Functions) => {
// Indicating that the scenario is about to schedule an article with a specified string
I.say('--- going to schedule article with '+globalVariables.RandomString+'');

// Checking the website title to determine the appropriate action to take
if( globalValues.TITLE_LABEL_WEBSITE == 'Go to the site in EN') {
    I.say('\n--- EN');

    // Grabbing the first item in the listing and checking if it contains the specified string
    const resultItem = await I.grabTextFrom('//*[@id="DataTables_Table_0"]/tbody/tr[1]');
    I.say('--- listing should contain '+globalVariables.RandomString+' in '+resultItem+'');

    // Clicking the "edit content" button
    I.say('\n--- Edit content', 'red');
    I.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0');
    I.wait(5);

// Repeat the same actions for each website title
} else if ( globalValues.TITLE_LABEL_WEBSITE == 'Aller sur le site in AR') {
    I.say('\n--- AR');
    const resultItem = await I.grabTextFrom('//*[@id="DataTables_Table_0"]/tbody/tr[1]');
    I.say('--- listing should contain '+globalVariables.RandomString+' in '+resultItem+'');
    I.say('\n--- Edit content', 'red');
    I.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0');
    I.wait(5);

} else if ( globalValues.TITLE_LABEL_WEBSITE == 'Aller sur le site in FR') {
    I.say('\n--- FR');
    const resultItem = await I.grabTextFrom('//*[@id="DataTables_Table_0"]/tbody/tr[1]');
    I.say('--- listing should contain '+globalVariables.RandomString+' in '+resultItem+'');
    I.say('\n--- Edit content', 'red');
    I.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0');
    I.wait(5);
    
} else if ( globalValues.TITLE_LABEL_WEBSITE == 'Go to the site ES') {
    I.say('\n--- ES');
    I.say('--- xpath specific ', 'red');
    const resultItem = await


    // GPT stop here, lazy bitch
    
    } else if ( globalValues.TITLE_LABEL_WEBSITE == 'Go to the site RU') {

        I.say('\n--- RU');
        I.say('--- xpath specific', 'red');
        const resultItem = await I.grabTextFrom('//*[@id="DataTables_Table_1"]/tbody/tr[1]');
            I.say('--- listing should contain '+globalVariables.RandomString+' in '+resultItem+'');
            // Edit_1
            // I.click('//*[@id="edit-content-btn-0"]/i');
            I.say('\n--- Edit content', 'red');
            I.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0');
            I.wait(5);

        } else {
             I.say('\n--- OTHER LNG');
             const resultItem = await I.grabTextFrom('//*[@id="DataTables_Table_0"]/tbody/tr[1]');
                I.say('--- listing should contain '+globalVariables.RandomString+' in '+resultItem+'');
                // Edit_1
            // I.click('//*[@id="edit-content-btn-0"]/i');
            I.say('\n--- Edit content', 'red');
            I.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0');
            I.wait(5);

        }

    // Fill title
    // I.fillField('//*[@id="article_title"]', 'SCHEDULED '+globalVariables.startDateString+' Test Article title CodeceptJS '+globalVariables.RandomString+'');

    I.fillField('//*[@id="article_title"]', 'SCHEDULED '+globalVariables.startDateString+' Test Article title CodeceptJS');
    // Scheduled
    I.click('//*[@id="radio-SCHEDULED"]');
    I.wait(5);

// DATE YYYY/MM/DD e.g 2020/12/03
let monthNumbers = ["01", "02", "03", "04", "05", "06","07", "08", "09", "10", "11", "12"];
let dayNumbers = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"];
// HOUR 
let hoursNumbers = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12","13", "14", "15", "16", "17", "18","19", "20", "21", "22", "23"];
let minutesNumbers = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"];



let yearReal = (new Date()).getFullYear();
let monthReal = (new Date().getMonth());
let dayReal = (new Date().getDate());



let year = (new Date()).getFullYear();
let month = (monthNumbers[new Date().getMonth()]);
let day = (dayNumbers[(dayReal-1)]);
// console.log(''+year+'/'+month+'/'+day+'');




let hoursReal = (new Date()).getHours();
let minutesReal = (new Date()).getMinutes();
let hours = (hoursNumbers[new Date().getHours()]);
let minutes = (minutesNumbers[new Date().getMinutes()]);


let hourPlus = (((new Date().getHours())).toString());
let minPlus = (((new Date().getMinutes()+5)).toString());
let hourPlusPlus = (((new Date().getHours()+2)).toString());


if ((minPlus=="57")) {

    // 60 - 57 = 3 + 0 => 3
    let minPlusPlus = (((60-minPlus)+3)).toString();

} else if ((minPlus=="58")) {
    
    // 60 - 58 = 2 + 1 => 3
    let minPlusPlus = (((60-minPlus)+1)).toString();

} else if ((minPlus=="59")) {

    // 60 - 59 = 1 + 2 => 3
    let minPlusPlus = (((60-minPlus)+2)).toString();

} else {

    // no need minPlusPlus
    let minPlusPlus = (((new Date().getMinutes()+5)).toString());
}



if ( (minPlus=="57") || (minPlus=="58") || (minPlus=="59") ) {

    // Scheduled date e.g. 2020/12/03
    I.say('--- Scheduled date e.g. '+yearReal+'/'+month+'/'+day+' ', 'red');
    I.fillField('//*[@id="scheduledDateInput"]', ''+yearReal+'/'+month+'/'+day+'');
    I.wait(3);

    // Scheduled hour 08:15
    I.say('--- Scheduled real hour + 5 min e.g. '+hourPlusPlus+':0'+minPlusPlus+' ', 'red');
    // I.fillField('//*[@id="scheduledHourInput"]', ''+hours+':'+minPlusPlus+'');
    // I.wait(3);

    I.click('//*[@id="scheduledHourInput"]');
    I.wait(3);

    // Hours
    I.fillField('body > div.bootstrap-timepicker-widget.dropdown-menu.timepicker-orient-left.timepicker-orient-bottom.open > table > tbody > tr:nth-child(2) > td:nth-child(1) > input', ''+hourPlusPlus+'');
    I.wait(10);


    // I.say('--- Get out ', 'red');
    // I.click('//*[@id="article_slug"]');

    // Minutes
    I.fillField('body > div.bootstrap-timepicker-widget.dropdown-menu.timepicker-orient-left.timepicker-orient-bottom.open > table > tbody > tr:nth-child(2) > td:nth-child(3) > input', '0'+minPlusPlus+'');
    I.wait(10);
    
    // Save as draft
    I.click('//*[@id="article_save"]');    
    I.wait(15);

    I.say('--- Refresh and Save as draft');
    I.click('//*[@id="btn-refresh-content"]'); 
    // Save as draft
    I.click('//*[@id="article_save"]'); 
    I.wait(15);

    I.refreshPage();
    I.wait(3);

    // Planifié le 04/12/2020 à 13:40
    I.say('--- Check Planifié label e.g. '+yearReal+'/'+month+'/'+day+' '+hourPlusPlus+':0'+minPlusPlus+' ', 'red');
    // I.see(''+yearReal+'/'+month+'/'+day+' '+hourPlusPlus+':'+minPlusPlus+'', '//*[@id="editScheduledAt"]'); 
           


    // Testing
    I.say('\n--- '+globalValues.TOTEM_TEST_MAN+'', 'red');
    // Check if the save action worked
    I.say('--- Check if the publication is made');
    I.wait(160);
    I.refreshPage();
    I.wait(3);
    // I.waitForElement('//*[@id="editScheduledAt"]', 5); // wait for 5 secs', 5);
    // I.seeCheckboxIsChecked('//*[@id="radio-PUBLISHED"]'); // I suppose //*[@id="radio-PUBLISHED"] is OK
    I.see(''+globalValues.LABEL_CONTENT_STATUS_PUBLISHED+'', '//*[@id="article_status"]'); // I suppose //*[@id="radio-PUBLISHED"] is OK



    } else {

            // Scheduled date e.g. 2020/12/03
            I.say('--- Scheduled date e.g. '+yearReal+'/'+month+'/'+day+' ', 'red');
            I.fillField('//*[@id="scheduledDateInput"]', ''+yearReal+'/'+month+'/'+day+'');
            I.wait(3);

            // Scheduled hour 08:15
            I.say('--- Scheduled real hour + 2 min e.g. '+hourPlus+':'+minPlus+' ', 'red');
            // I.fillField('//*[@id="scheduledHourInput"]', ''+hours+':'+minPlus+'');
            // I.wait(3);

            I.click('//*[@id="scheduledHourInput"]');
            I.wait(3);

            // Hours
            I.fillField('body > div.bootstrap-timepicker-widget.dropdown-menu.timepicker-orient-left.timepicker-orient-bottom.open > table > tbody > tr:nth-child(2) > td:nth-child(1) > input', ''+hourPlus+'');
            I.wait(10);


            // I.say('--- Get out ', 'red');
            // I.click('//*[@id="article_slug"]');

            // Minutes
            I.fillField('body > div.bootstrap-timepicker-widget.dropdown-menu.timepicker-orient-left.timepicker-orient-bottom.open > table > tbody > tr:nth-child(2) > td:nth-child(3) > input', ''+minPlus+'');
            I.wait(10);


            // Save as draft
            I.click('//*[@id="article_save"]');    
            I.wait(15);

            I.say('--- Refresh and Save as draft');
            I.click('//*[@id="btn-refresh-content"]'); 
            // Save as draft
            I.click('//*[@id="article_save"]'); 
            I.wait(15);

            I.refreshPage();
            I.wait(3);

            // Planifié le 04/12/2020 à 13:40
            I.say('--- Check Planifié label e.g. '+yearReal+'/'+month+'/'+day+' '+hourPlus+':'+minPlus+' ', 'red');
            // I.see(''+yearReal+'/'+month+'/'+day+' '+hourPlus+':'+minPlus+'', '//*[@id="editScheduledAt"]'); 
                   


            // Testing
            I.say('\n--- '+globalValues.TOTEM_TEST_MAN+'', 'red');
            // Check if the save action worked
            I.say('--- Check if the publication is made');
            I.wait(160);
            I.refreshPage();
            I.wait(3);
            // I.waitForElement('//*[@id="editScheduledAt"]', 5); // wait for 5 secs', 5);
            // I.seeCheckboxIsChecked('//*[@id="radio-PUBLISHED"]'); // I suppose //*[@id="radio-PUBLISHED"] is OK
            I.see(''+globalValues.LABEL_CONTENT_STATUS_PUBLISHED+'', '//*[@id="article_status"]'); // I suppose //*[@id="radio-PUBLISHED"] is OK


    }
    
    

});
