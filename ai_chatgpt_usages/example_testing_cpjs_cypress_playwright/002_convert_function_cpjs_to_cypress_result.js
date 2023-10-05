// 002_convert_function_cpjs_to_cypress_result.js
// result for GPT query convert_function_cpjs_to_cypress_3.js
// Convert function written in Codeceptjs to Cypress.


// FUNCTION_1

function CrawAddWireImage() {
  cy.log('--- CrawAddWireImage :: CSS_WIRE_IMAGE:: ' + globalValues.CSS_WIRE_IMAGE + '');

  // Add a media
  cy.log('--- Add a media image ' + globalVariables.RandomImageInsert + ' ');
  cy.get('#media-image div:nth-child(2) button:nth-child(5)').click();

  // remove time scope for image
  Functions.RemoveTimeScopeForImage();

  // select random image
  cy.get(
    `#${globalValues.CSS_WIRE_IMAGE} div div:nth-child(2) div div:nth-child(2) div:nth-child(3) div:nth-child(2) a:nth-child(${globalVariables.RandomImageInsert}) img`
  ).click();

  
  // medium_title
  cy.get('#medium_title').should('be.visible').type(
    globalValues.MEDIUM_TITLE + globalVariables.RandomString
  );

  // medium_caption
  cy.get('#medium_caption').should('be.visible').type(
    globalValues.MEDIUM_CAPTION + ' ' + globalVariables.RandomString
  );

  // medium_copyright
  cy.get('#medium_copyright').should('be.visible').type(
    globalValues.MEDIUM_COPYRIGHT + ' ' + globalVariables.RandomString
  );

  // medium_copyrightUrl
  cy.get('#medium_copyrightUrl').should('be.visible').type(
    globalValues.MEDIUM_COPYRIGHTURL + ' ' + globalVariables.RandomString
  );

  cy.get(`#${globalValues.CSS_WIRE_IMAGE} div div:nth-child(1) div:nth-child(2) div form div:nth-child(2) button:first`).click();
}

/*

GPT is even given me some advice... and best practices. Great ! 
 
Note that in Cypress, the cy.waitForElement and I.waitForElement commands are not necessary, as Cypress automatically waits for elements to become visible. Also, instead of using XPath selectors, I used CSS selectors for simplicity and better performance.

 */

// FUNCTION_2

function RemoveTimeScopeForImage () {
    // remove time scope for image
    cy.log('--- Remove time scope for image selection')
    cy.get('#media_search_pubDateStart').clear().type(globalValues.IMAGES_DIRECTORY_PUB_DATE_START);
    cy.get('#media_search_pubDateEnd').clear().type(globalValues.IMAGES_DIRECTORY_PUB_DATE_END);
    cy.get('#media_search_submit').click();
    cy.wait(30);
}


