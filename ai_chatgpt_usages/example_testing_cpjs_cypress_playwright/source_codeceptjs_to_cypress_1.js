// 001_convert_function_cpjs_to_cypress.js
// source for GPT query
// Convert function written in Codeceptjs to Cypress:



describe('03 :: Check CRAW Backoffice :: ARTICLE :: SCHEDULED', () => {
  it('schedules an article', () => {
    cy.log('--- going to schedule article with ' + globalVariables.RandomString)

    if (globalValues.TITLE_LABEL_WEBSITE === 'Go to the site in EN') {
      cy.log('\n--- EN')
      
      cy.get('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
        .then(resultItem => {
          cy.log('--- listing should contain ' + globalVariables.RandomString + ' in ' + resultItem)
          cy.log('\n--- Edit content', 'red')
          cy.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
          cy.wait(5)
        })
    } else if (globalValues.TITLE_LABEL_WEBSITE === 'Go to the site in AR') {
      cy.log('\n--- AR')
      cy.get('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
        .then(resultItem => {
          cy.log('--- listing should contain ' + globalVariables.RandomString + ' in ' + resultItem)
          cy.log('\n--- Edit content', 'red')
          cy.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
          cy.wait(5)
        })
    } else if (globalValues.TITLE_LABEL_WEBSITE === 'Go to the site in FR') {
      cy.log('\n--- FR')
      cy.get('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
        .then(resultItem => {
          cy.log('--- listing should contain ' + globalVariables.RandomString + ' in ' + resultItem)
          cy.log('\n--- Edit content', 'red')
          cy.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
          cy.wait(5)
        })
    } else if (globalValues.TITLE_LABEL_WEBSITE === 'Go to the site in ES') {
      cy.log('\n--- ES')
      cy.log('--- xpath specific', 'red')
      cy.get('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
        .then(resultItem => {
          cy.log('--- listing should contain ' + globalVariables.RandomString + ' in ' + resultItem)
          cy.log('\n--- Edit content', 'red')
          cy.click('#DataTables_Table_1 tbody tr td.text-center.text-nowrap #edit-content-btn--0')
          cy.wait(5)
        })
      } else {
            cy.log('\n--- OTHER LNG')
            // to be continued
      
      } 

            // GPT stop here, lazy bitch


// THE MOST DIFFICULT PART OF THE TESTING SCRIPT
Cypress.Commands.add('fillArticleTitle', () => {
  cy.get('#article_title').type('SCHEDULED ' + new Date().toLocaleDateString() + ' Test Article title CodeceptJS');
});

Cypress.Commands.add('clickScheduledRadioButton', () => {
  cy.get('#radio-SCHEDULED').click();
});

Cypress.Commands.add('fillScheduledDate', () => {
  cy.get('#scheduledDateInput').type(new Date().toLocaleDateString());
});

Cypress.Commands.add('fillScheduledHour', () => {
  let currentHour = new Date().getHours();
  let currentMinutes = new Date().getMinutes();
  let nextMinutes = currentMinutes + 5;
  if (nextMinutes >= 60) {
  nextMinutes = nextMinutes % 60;
  currentHour += 1;
}
cy.get('#scheduledHourInput').type(currentHour + ':' + nextMinutes);
});

Cypress.Commands.add('fillArticleTitle', () => {
  cy.fillArticleTitle();
  cy.clickScheduledRadioButton();
  cy.wait(5);
  cy.fillScheduledDate();
  cy.fillScheduledHour();
});